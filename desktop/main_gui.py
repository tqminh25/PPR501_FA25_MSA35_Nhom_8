import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import requests

API_BASE = "http://127.0.0.1:8000"

FIELDS = [
    ("student_code", "MSSV"),
    ("first_name", "Tên"),
    ("last_name", "Họ"),
    ("email", "Email"),
    ("dob", "Ngày sinh (yyyy-mm-dd)"),
    ("home_town", "Quê quán"),
    ("math_score", "Điểm Toán (0-10)"),
    ("literature_score", "Điểm Văn (0-10)"),
    ("english_score", "Điểm Anh (0-10)"),
]

CSV_HEADERS = [k for k, _ in FIELDS]  # dùng cho import/export

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Manager (Desktop)")
        self.geometry("1100x640")

        # --- Form bên trái ---
        form = ttk.LabelFrame(self, text="Thông tin sinh viên")
        form.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.vars = {}
        for key, label in FIELDS:
            ttk.Label(form, text=label).pack(anchor="w", pady=(6, 0))
            v = tk.StringVar()
            ttk.Entry(form, textvariable=v, width=28).pack(anchor="w", pady=2)
            self.vars[key] = v

        btn_frame = ttk.Frame(form)
        btn_frame.pack(pady=10, fill=tk.X)
        ttk.Button(btn_frame, text="Thêm mới", command=self.create_student).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text="Cập nhật", command=self.update_student).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text="Xóa", command=self.delete_student).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text="Xóa form", command=self.clear_form).pack(side=tk.LEFT, padx=4)

        # --- Import/Export CSV ---
        io_frame = ttk.LabelFrame(form, text="Nhập/Xuất CSV")
        io_frame.pack(fill=tk.X, pady=(10, 0))
        ttk.Button(io_frame, text="Import CSV", command=self.import_csv).pack(side=tk.LEFT, padx=4, pady=6)
        ttk.Button(io_frame, text="Export CSV", command=self.export_csv).pack(side=tk.LEFT, padx=4, pady=6)

        # --- Tìm kiếm ---
        search_frame = ttk.LabelFrame(self, text="Tìm kiếm")
        search_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(10, 0))
        self.search_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.search_var, width=40).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(search_frame, text="Tải danh sách", command=self.load_students).pack(side=tk.LEFT, padx=5)

        # --- Bảng danh sách ---
        table_frame = ttk.Frame(self)
        table_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        cols = ["id"] + [k for k, _ in FIELDS]
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=120, anchor="w")
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select_row)

        self.selected_id = None
        self.load_students()

    # ------------------- Helpers -------------------
    def _payload(self):
        """Lấy dữ liệu từ form, ép kiểu điểm -> float nếu có."""
        data = {k: v.get().strip() or None for k, v in self.vars.items()}
        for key in ["math_score", "literature_score", "english_score"]:
            if data[key] is not None:
                try:
                    data[key] = float(data[key])
                except:
                    data[key] = None
        return data

    def _row_to_payload(self, row_dict: dict):
        """
        Chuẩn hoá 1 dòng CSV thành payload gửi lên API.
        row_dict: dict của DictReader (keys chính là header).
        """
        # chỉ lấy các cột hợp lệ, bỏ qua cột lạ
        data = {}
        for k in CSV_HEADERS:
            val = (row_dict.get(k, "") or "").strip()
            data[k] = val if val != "" else None

        # ép kiểu điểm
        for key in ["math_score", "literature_score", "english_score"]:
            if data.get(key) is not None:
                try:
                    data[key] = float(data[key])
                except:
                    data[key] = None
        return data

    def load_students(self):
        try:
            q = self.search_var.get().strip()
            params = {"search": q} if q else {}
            # lấy nhiều hơn 100 nếu cần export hết
            params.setdefault("limit", 10000)
            r = requests.get(f"{API_BASE}/students", params=params, timeout=10)
            r.raise_for_status()
            data = r.json()
            # clear
            for i in self.tree.get_children():
                self.tree.delete(i)
            for row in data:
                self.tree.insert("", tk.END, values=[row.get("id")] + [row.get(k) for k, _ in FIELDS])
        except Exception as e:
            messagebox.showerror("Lỗi", f"Tải danh sách thất bại:\n{e}")

    def on_select_row(self, _evt):
        sel = self.tree.selection()
        if not sel:
            self.selected_id = None
            return
        values = self.tree.item(sel[0], "values")
        self.selected_id = int(values[0])
        for idx, (key, _label) in enumerate(FIELDS, start=1):
            self.vars[key].set(values[idx] if values[idx] is not None else "")

    def clear_form(self):
        self.selected_id = None
        for v in self.vars.values():
            v.set("")

    # ------------------- CRUD -------------------
    def create_student(self):
        try:
            payload = self._payload()
            if not payload["student_code"]:
                messagebox.showwarning("Thiếu dữ liệu", "MSSV (student_code) không được để trống")
                return
            r = requests.post(f"{API_BASE}/students", json=payload, timeout=10)
            if r.status_code == 201:
                messagebox.showinfo("Thành công", "Đã thêm sinh viên")
                self.clear_form()
                self.load_students()
            else:
                message = r.json().get("detail", r.text)
                messagebox.showerror("Thất bại", f"Không thêm được:\n{message}")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def update_student(self):
        if not self.selected_id:
            messagebox.showwarning("Chưa chọn", "Hãy chọn sinh viên trong bảng để cập nhật")
            return
        try:
            payload = self._payload()
            r = requests.put(f"{API_BASE}/students/{self.selected_id}", json=payload, timeout=10)
            if r.status_code == 200:
                messagebox.showinfo("Thành công", "Đã cập nhật")
                self.load_students()
            else:
                message = r.json().get("detail", r.text)
                messagebox.showerror("Thất bại", f"Không cập nhật được:\n{message}")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def delete_student(self):
        if not self.selected_id:
            messagebox.showwarning("Chưa chọn", "Hãy chọn sinh viên trong bảng để xóa")
            return
        if not messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa sinh viên này?"):
            return
        try:
            r = requests.delete(f"{API_BASE}/students/{self.selected_id}", timeout=10)
            if r.status_code in (200, 204):
                messagebox.showinfo("Thành công", "Đã xóa")
                self.clear_form()
                self.load_students()
            else:
                message = r.json().get("detail", r.text)
                messagebox.showerror("Thất bại", f"Không xóa được:\n{message}")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    # ------------------- Import/Export CSV -------------------
    def import_csv(self):
        """
        Chọn file CSV -> đọc từng dòng -> POST /students.
        Báo cáo tổng: thêm thành công / lỗi / trùng...
        """
        path = filedialog.askopenfilename(
            title="Chọn file CSV để Import",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not path:
            return

        total = ok = dup = bad = 0
        # Gợi ý: cho phép continue nếu gặp lỗi dòng
        try:
            with open(path, "r", newline="", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                # Kiểm tra header
                missing = [h for h in ["student_code"] if h not in reader.fieldnames]
                if missing:
                    messagebox.showerror(
                        "Lỗi định dạng",
                        f"CSV thiếu cột bắt buộc: {', '.join(missing)}"
                    )
                    return

                for row in reader:
                    total += 1
                    payload = self._row_to_payload(row)

                    if not payload.get("student_code"):
                        bad += 1
                        continue

                    try:
                        r = requests.post(f"{API_BASE}/students", json=payload, timeout=10)
                        if r.status_code == 201:
                            ok += 1
                        else:
                            # Xác định lỗi trùng lặp (BE trả 400 với chi tiết)
                            try:
                                detail = r.json().get("detail", "")
                            except:
                                detail = r.text
                            if "exists" in detail:
                                dup += 1
                            else:
                                bad += 1
                    except Exception:
                        bad += 1
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không đọc được CSV:\n{e}")
            return

        self.load_students()
        messagebox.showinfo(
            "Import CSV",
            f"Tổng dòng: {total}\n"
            f"Thêm thành công: {ok}\n"
            f"Trùng (bỏ qua): {dup}\n"
            f"Lỗi khác: {bad}"
        )

    def export_csv(self):
        """
        GET /students (limit lớn) -> ghi toàn bộ ra CSV với header chuẩn CSV_HEADERS.
        """
        path = filedialog.asksaveasfilename(
            title="Chọn nơi lưu file CSV",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not path:
            return

        try:
            # Lấy tất cả SV
            params = {"limit": 100000}
            r = requests.get(f"{API_BASE}/students", params=params, timeout=15)
            r.raise_for_status()
            data = r.json()

            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
                writer.writeheader()
                for row in data:
                    out = {k: row.get(k) for k in CSV_HEADERS}
                    writer.writerow(out)

            messagebox.showinfo("Export CSV", f"Đã xuất {len(data)} sinh viên ra:\n{path}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Xuất CSV thất bại:\n{e}")

if __name__ == "__main__":
    App().mainloop()