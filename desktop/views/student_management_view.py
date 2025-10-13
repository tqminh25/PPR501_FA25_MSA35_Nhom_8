#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Student Management — Themed Desktop App (Tkinter + ttk)
v4 changes:
- Removed header texts: "Students" and the welcome subline.
- Card actions: removed per-card "Delete" (kept only "View / Edit").
- Refined spacing, paddings, and alignment.
- Pager: right-aligned with order Prev → Next.
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import List, Dict, Optional
from .base_view import BaseContentView
from models import api_client
import csv

# API Configuration
API_BASE = "http://127.0.0.1:8000"


def to_float(x):
    if x is None: return None
    s = str(x).strip()
    if s == "": return None
    try: return float(s)
    except: return None


def compute_gpa_4(m, l, e):
    vals = [v for v in (m,l,e) if v is not None]
    if not vals: return None
    avg10 = sum(vals)/len(vals)
    return round(avg10*0.4, 1)


def status_badge(gpa):
    if gpa is None: return ("unknown", "#E5E7EB", "#111827")
    if gpa >= 3.6:  return ("active", "#DCFCE7", "#166534")
    if gpa >= 3.0:  return ("active", "#E7F8EC", "#166534")
    if gpa >= 2.5:  return ("warning", "#FEF3C7", "#92400E")
    return ("at risk", "#FEE2E2", "#991B1B")


# API Functions via centralized client
def api_get_students(page=1, page_size=12, search=""):
    """Lấy danh sách học sinh từ API qua api_client. Trả None nếu lỗi để dùng local fallback."""
    print("--------------------------------")
    print("Binh test api_get_students", page, page_size, search)
    try:
        return api_client.get_students(page=page, page_size=page_size, search=search)
    except Exception:
        return None


def api_create_student(payload):
    """Tạo học sinh mới qua API (api_client). Trả None nếu lỗi để fallback local."""
    try:
        return api_client.create_student(payload)
    except Exception:
        return None


def api_update_student(sid, payload):
    """Cập nhật học sinh qua API (api_client). Trả None nếu lỗi để fallback local."""
    try:
        return api_client.update_student(sid, payload)
    except Exception:
        return None


def api_delete_student(sid):
    """Xóa học sinh qua API (api_client). Trả None nếu lỗi để fallback local."""
    try:
        return api_client.delete_student(sid)
    except Exception:
        return None


class StudentManagementView(BaseContentView):
    """View cho quản lý học sinh với giao diện card đẹp"""
    
    def __init__(self, parent_frame: ttk.Frame):
        # Khởi tạo dữ liệu trước khi gọi super().__init__()
        self.students_data = []
        self.page = 1
        self.page_size = 12
        self.search_var = tk.StringVar()
        self.selected = None
        self.vars = {}
        self._placeholder_text = "aaaaaaaaaa"
        
        super().__init__(parent_frame, "👥 Quản lý học sinh")
        self._setup_styles()
        self._load_sample_data()
        self.refresh()
    

    def _create_content(self):
        """Tạo nội dung quản lý học sinh"""
        # Search và tools
        self._create_tools()
        
        # Canvas cho scrollable content
        self._create_canvas()
        
        # Pager
        self._create_pager()
        
        # Form edit
        self._create_form()
    
    def _setup_styles(self):
        """Thiết lập styles cho view"""
        s = ttk.Style()
        s.configure("Page.TFrame", background="#F7F8FA")
        s.configure("Section.TFrame", background="#F7F8FA")
        s.configure("Card.TFrame", background="#FFFFFF", relief="flat")
        s.configure("Title.TLabel", background="#F7F8FA", font=("Inter",18,"bold"))
        s.configure("Sub.TLabel", background="#F7F8FA", foreground="#6B7280", font=("Inter",11))
        s.configure("CardTitle.TLabel", background="#FFFFFF", font=("Inter",12,"bold"))
        s.configure("Meta.TLabel", background="#FFFFFF", foreground="#6B7280", font=("Inter",10))
        s.configure("TButton", padding=(10,6))
        
        # Cấu hình background cho các frame
        self.main_frame.configure(style="Page.TFrame")
        self.content_frame.configure(style="Page.TFrame")
    
    def _create_tools(self):
        """Tạo toolbar với search và các nút chức năng"""
        tools = ttk.Frame(self.content_frame, style="Page.TFrame")
        tools.grid(row=0, column=0, sticky="ew", padx=20, pady=(6,10))
        
        # Search entry
        entry = ttk.Entry(tools, textvariable=self.search_var, width=54)
        entry.grid(row=0, column=0, padx=(0,8))
        entry.insert(0, self._placeholder_text)
        # Clear placeholder on focus
        entry.bind("<FocusIn>", lambda e: self.search_var.set("") if self.search_var.get() == self._placeholder_text else None)
        # Restore placeholder when empty on focus out
        def _on_focus_out(_e):
            val = self.search_var.get().strip()
            if val == "":
                self.search_var.set(self._placeholder_text)
        entry.bind("<FocusOut>", _on_focus_out)
        
        # Search button
        ttk.Button(tools, text="Search", command=lambda: self._go_page(1)).grid(row=0, column=1, padx=(0,6))
        
        # Clear button
        ttk.Button(tools, text="Clear", command=self._clear_search).grid(row=0, column=2, padx=(0,12))
        
        # Import/Export buttons
        ttk.Button(tools, text="Import CSV", command=self.import_csv).grid(row=0, column=3, padx=(0,8))
        ttk.Button(tools, text="Export CSV", command=self.export_csv).grid(row=0, column=4)
    
    def _create_canvas(self):
        """Tạo canvas cho scrollable content"""
        # Canvas frame
        canvas_frame = ttk.Frame(self.content_frame, style="Page.TFrame")
        canvas_frame.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0,6))
        canvas_frame.columnconfigure(0, weight=1)
        canvas_frame.rowconfigure(0, weight=1)
        
        # Canvas
        self.canvas = tk.Canvas(canvas_frame, bg="#F7F8FA", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbar
        self.scroll = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scroll.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=self.scroll.set)
        
        # Inner frame
        self.inner = ttk.Frame(self.canvas, style="Section.TFrame")
        self.win = self.canvas.create_window((14,0), window=self.inner, anchor="nw")
        
        # Bind events
        self.canvas.bind("<Configure>", lambda e: (
            self.canvas.itemconfig(self.win, width=self.canvas.winfo_width()-28),
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        ))
        self.inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
    
    def _create_pager(self):
        """Tạo pager"""
        pager = ttk.Frame(self.content_frame, style="Page.TFrame")
        pager.grid(row=2, column=0, sticky="ew", padx=20, pady=(4,12))
        
        # Page label
        self.page_label = ttk.Label(pager, text="", style="Sub.TLabel")
        self.page_label.grid(row=0, column=0, sticky="w")
        
        # Navigation buttons
        right_box = ttk.Frame(pager, style="Page.TFrame")
        right_box.grid(row=0, column=1, sticky="e")
        
        ttk.Button(right_box, text="Prev", command=self.prev_page).grid(row=0, column=0, padx=(0,6))
        ttk.Button(right_box, text="Next", command=self.next_page).grid(row=0, column=1)
    
    def _create_form(self):
        """Tạo form edit student"""
        form = ttk.LabelFrame(self.content_frame, text="Edit Student", style="Section.TFrame")
        form.grid(row=3, column=0, sticky="ew", padx=20, pady=(0,16))
        
        # Form grid
        grid = ttk.Frame(form, style="Section.TFrame")
        grid.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        
        # Form variables
        self.vars = {k: tk.StringVar() for k in [
            "student_code", "first_name", "last_name", "email", "dob", 
            "home_town", "math_score", "literature_score", "english_score"
        ]}
        
        # Form fields
        def row(r, label, key, col):
            ttk.Label(grid, text=label, width=16).grid(row=r, column=col, sticky="w", pady=4, padx=(0,6))
            ttk.Entry(grid, textvariable=self.vars[key], width=28).grid(row=r, column=col+1, sticky="w", pady=4)
        
        row(0, "Student Code", "student_code", 0)
        row(0, "First Name", "first_name", 2)
        row(1, "Last Name", "last_name", 0)
        row(1, "Email", "email", 2)
        row(2, "DOB (YYYY-MM-DD)", "dob", 0)
        row(2, "Home Town", "home_town", 2)
        row(3, "Math", "math_score", 0)
        row(3, "Literature", "literature_score", 2)
        row(4, "English", "english_score", 0)
        
        # Action buttons
        bar = ttk.Frame(form, style="Section.TFrame")
        bar.grid(row=1, column=0, sticky="ew", padx=8, pady=(4,4))
        
        ttk.Button(bar, text="Add New", command=self.on_add).grid(row=0, column=0, padx=(0,6))
        ttk.Button(bar, text="Update", command=self.on_update).grid(row=0, column=1, padx=(0,6))
        ttk.Button(bar, text="Delete", command=self.on_delete).grid(row=0, column=2, padx=(0,6))
        ttk.Button(bar, text="Clear Form", command=self.clear_form).grid(row=0, column=3)
    
    def _load_sample_data(self):
        """Load dữ liệu mẫu"""
        self.students_data = [
            {
                "id": 1, "student_code": "ST001", "first_name": "Nguyễn Văn", "last_name": "An",
                "email": "an.nguyen@email.com", "dob": "2005-01-15", "home_town": "Hà Nội",
                "math_score": 8.5, "literature_score": 9.0, "english_score": 8.0
            },
            {
                "id": 2, "student_code": "ST002", "first_name": "Trần Thị", "last_name": "Bình",
                "email": "binh.tran@email.com", "dob": "2005-03-22", "home_town": "TP.HCM",
                "math_score": 9.2, "literature_score": 8.8, "english_score": 9.5
            },
            {
                "id": 3, "student_code": "ST003", "first_name": "Lê Văn", "last_name": "Cường",
                "email": "cuong.le@email.com", "dob": "2005-07-10", "home_town": "Đà Nẵng",
                "math_score": 7.8, "literature_score": 7.5, "english_score": 8.2
            },
            {
                "id": 4, "student_code": "ST004", "first_name": "Phạm Thị", "last_name": "Dung",
                "email": "dung.pham@email.com", "dob": "2005-11-05", "home_town": "Hải Phòng",
                "math_score": 8.9, "literature_score": 9.1, "english_score": 8.7
            },
            {
                "id": 5, "student_code": "ST005", "first_name": "Hoàng Văn", "last_name": "Em",
                "email": "em.hoang@email.com", "dob": "2005-09-18", "home_town": "Cần Thơ",
                "math_score": 8.1, "literature_score": 7.9, "english_score": 8.3
            },
        ]
    
    def _go_page(self, p):
        """Chuyển đến trang"""
        self.page = max(1, p)
        self.refresh()
    
    def next_page(self):
        """Trang tiếp theo"""
        self.page += 1
        self.refresh()
    
    def prev_page(self):
        """Trang trước"""
        self.page = max(1, self.page - 1)
        self.refresh()
    
    def _clear_search(self):
        """Xóa search"""
        self.search_var.set(self._placeholder_text if hasattr(self, "_placeholder_text") else "")
        self._go_page(1)
    
    def refresh(self):
        print("Binh test Refresh")
        """Refresh view"""
        try:
            # Try to get data from API first
            search_term = self._get_search_term()
            data = api_get_students(self.page, self.page_size, search_term)
            
            if data is not None:
                # API data available
                meta = data.get("meta", {"total": len(data.get("items", [])), "page": self.page, "page_size": self.page_size})
                items = data.get("items", [])
                total_pages = max(1, (meta["total"] - 1) // meta["page_size"] + 1)
                if self.page > total_pages:
                    self.page = total_pages
                self.page_label.config(text=f"Page {meta['page']} / {total_pages} • Total {meta['total']}")
                self.render_cards(items)
            else:
                # Fallback to local data
                self._refresh_local()
                
        except Exception as e:
            messagebox.showerror("Load Error", str(e))
            # Fallback to local data
            self._refresh_local()
    
    def _refresh_local(self):
        """Refresh using local data as fallback"""
        # Filter data based on search
        search_value = self._get_search_term().lower()
        if search_value:
            filtered_data = [
                student for student in self.students_data
                if search_value in student.get("first_name", "").lower() or
                   search_value in student.get("last_name", "").lower() or
                   search_value in student.get("email", "").lower() or
                   search_value in student.get("student_code", "").lower()
            ]
        else:
            filtered_data = self.students_data
        
        # Pagination
        total = len(filtered_data)
        total_pages = max(1, (total - 1) // self.page_size + 1)
        if self.page > total_pages:
            self.page = total_pages
        
        start_idx = (self.page - 1) * self.page_size
        end_idx = start_idx + self.page_size
        page_data = filtered_data[start_idx:end_idx]
        
        # Update page label
        self.page_label.config(text=f"Page {self.page} / {total_pages} • Total {total} (Local)")
        
        # Render cards
        self.render_cards(page_data)
    
    def render_cards(self, items):
        """Render student cards"""
        # Clear existing cards
        for w in self.inner.winfo_children():
            w.destroy()
        
        cols = 3
        for i, it in enumerate(items):
            r, c = divmod(i, cols)
            card = ttk.Frame(self.inner, style="Card.TFrame")
            card.grid(row=r, column=c, padx=10, pady=10, sticky="nsew")
            self.inner.grid_columnconfigure(c, weight=1)
            
            wrap = ttk.Frame(card, style="Card.TFrame")
            wrap.pack(fill="both", expand=True, padx=14, pady=14)
            
            # Avatar
            first_name = it.get("first_name") or ""
            last_name = it.get("last_name") or ""
            initials = (first_name[:1] + last_name[:1]).upper() or "ST"
            avatar = tk.Canvas(wrap, width=44, height=44, highlightthickness=0, bg="white")
            avatar.create_oval(2, 2, 42, 42, fill="#111827", outline="#111827")
            avatar.create_text(22, 22, text=initials, fill="white", font=("Inter", 10, "bold"))
            avatar.grid(row=0, column=0, rowspan=2, sticky="w")
            
            # Name and code
            name = f"{it.get('first_name', '')} {it.get('last_name', '')}".strip() or "(No name)"
            ttk.Label(wrap, text=name, style="CardTitle.TLabel").grid(row=0, column=1, sticky="w", padx=(8, 0))
            ttk.Label(wrap, text=it.get("student_code", ""), style="Meta.TLabel").grid(row=1, column=1, sticky="w", padx=(8, 0), pady=(2, 6))
            
            # Email
            ttk.Label(wrap, text=f"📧 {it.get('email', '')}", style="Meta.TLabel").grid(row=2, column=0, columnspan=2, sticky="w")
            
            # Hometown
            hometown = it.get("home_town") or "-"
            ttk.Label(wrap, text=f"🏠 {hometown}", style="Meta.TLabel").grid(row=3, column=0, columnspan=2, sticky="w")
            
            # GPA
            m, l, e = it.get("math_score"), it.get("literature_score"), it.get("english_score")
            gpa = compute_gpa_4(m, l, e)
            ttk.Label(wrap, text="GPA", style="Meta.TLabel").grid(row=4, column=0, sticky="w", pady=(8, 0))
            ttk.Label(wrap, text=str(gpa) if gpa is not None else "-", style="CardTitle.TLabel").grid(row=4, column=1, sticky="w", pady=(8, 0))
            
            # Status badge
            text, bg, fg = status_badge(gpa)
            badge = tk.Label(wrap, text=text, bg=bg, fg=fg, font=("Inter", 9, "bold"), padx=8, pady=2)
            badge.grid(row=5, column=0, sticky="w", pady=(6, 0))
            
            # Actions
            actions = ttk.Frame(wrap, style="Card.TFrame")
            actions.grid(row=6, column=0, columnspan=2, sticky="we", pady=(10, 0))
            ttk.Button(actions, text="View / Edit", command=lambda it=it: self.load_form(it)).pack(side="left")
    
    def load_form(self, it):
        """Load student data vào form"""
        self.selected = it
        for k, v in self.vars.items():
            val = it.get(k, "")
            v.set("" if val is None else str(val))
        self.canvas.yview_moveto(1.0)
    
    def clear_form(self):
        """Clear form"""
        self.selected = None
        for v in self.vars.values():
            v.set("")
    
    def _payload_from_form(self):
        """Tạo payload từ form"""
        v = {k: s.get().strip() for k, s in self.vars.items()}
        for k in ("math_score", "literature_score", "english_score"):
            v[k] = to_float(v[k])
        for k, val in list(v.items()):
            if val == "":
                v[k] = None
        return v
    
    def on_add(self):
        """Thêm học sinh mới"""
        try:
            payload = self._payload_from_form()
            
            # Try API first
            result = api_create_student(payload)
            if result is not None:
                # API success
                self.clear_form()
                self._go_page(1)
                messagebox.showinfo("Success", "Student created via API.")
            else:
                # Fallback to local
                new_id = max([s.get("id", 0) for s in self.students_data], default=0) + 1
                payload["id"] = new_id
                self.students_data.append(payload)
                self.clear_form()
                self._go_page(1)
                messagebox.showinfo("Success", "Student created locally.")
        except Exception as e:
            messagebox.showerror("Create failed", str(e))
    
    def on_update(self):
        """Cập nhật học sinh"""
        if not self.selected:
            messagebox.showwarning("No selection", "Load a card first.")
            return
        try:
            payload = self._payload_from_form()
            
            # Try API first
            result = api_update_student(self.selected.get("id"), payload)
            if result is not None:
                # API success
                self.refresh()
                messagebox.showinfo("Success", "Student updated via API.")
            else:
                # Fallback to local
                for i, student in enumerate(self.students_data):
                    if student.get("id") == self.selected.get("id"):
                        self.students_data[i].update(payload)
                        break
                self.refresh()
                messagebox.showinfo("Success", "Student updated locally.")
        except Exception as e:
            messagebox.showerror("Update failed", str(e))
    
    def on_delete(self):
        """Xóa học sinh"""
        if not self.selected:
            messagebox.showwarning("No selection", "Load a card first.")
            return
        self.confirm_delete(self.selected)
    
    def confirm_delete(self, it):
        """Xác nhận xóa"""
        if messagebox.askyesno("Confirm", f"Delete {it.get('student_code', 'this student')}?"):
            try:
                # Try API first
                result = api_delete_student(it.get("id"))
                if result is not None:
                    # API success
                    self.clear_form()
                    self.refresh()
                    messagebox.showinfo("Success", "Student deleted via API.")
                else:
                    # Fallback to local
                    self.students_data = [s for s in self.students_data if s.get("id") != it.get("id")]
                    self.clear_form()
                    self.refresh()
                    messagebox.showinfo("Success", "Student deleted locally.")
            except Exception as e:
                messagebox.showerror("Delete failed", str(e))
    
    def import_csv(self):
        """Import CSV"""
        fp = filedialog.askopenfilename(title="Select CSV", filetypes=[("CSV", "*.csv")])
        if not fp:
            return
        ok = fail = 0
        try:
            with open(fp, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    payload = {
                        "student_code": row.get("student_code") or row.get("code") or row.get("id"),
                        "first_name": row.get("first_name") or row.get("fname"),
                        "last_name": row.get("last_name") or row.get("lname"),
                        "email": row.get("email"),
                        "dob": row.get("dob") or row.get("date_of_birth"),
                        "home_town": row.get("home_town") or row.get("hometown"),
                        "math_score": to_float(row.get("math_score") or row.get("math")),
                        "literature_score": to_float(row.get("literature_score") or row.get("literature")),
                        "english_score": to_float(row.get("english_score") or row.get("english")),
                    }
                    payload = {k: v for k, v in payload.items() if v not in (None, "")}
                    try:
                        # Try API first
                        result = api_create_student(payload)
                        if result is not None:
                            ok += 1
                        else:
                            # Fallback to local
                            new_id = max([s.get("id", 0) for s in self.students_data], default=0) + 1
                            payload["id"] = new_id
                            self.students_data.append(payload)
                            ok += 1
                    except Exception:
                        fail += 1
            self._go_page(1)
            messagebox.showinfo("Import CSV", f"Imported OK={ok}, FAIL={fail}")
        except Exception as e:
            messagebox.showerror("Import CSV", str(e))
    
    def export_csv(self):
        """Export CSV"""
        fp = filedialog.asksaveasfilename(
            title="Save CSV", 
            defaultextension=".csv", 
            filetypes=[("CSV", "*.csv")], 
            initialfile="export_students.csv"
        )
        if not fp:
            return
        try:
            # Try to get data from API first
            data = api_get_students(1, 100000, self._get_search_term())
            if data is not None:
                rows = data.get("items", [])
            else:
                # Fallback to local data
                search_value = self._get_search_term().lower()
                if search_value:
                    rows = [
                        student for student in self.students_data
                        if search_value in student.get("first_name", "").lower() or
                           search_value in student.get("last_name", "").lower() or
                           search_value in student.get("email", "").lower() or
                           search_value in student.get("student_code", "").lower()
                    ]
                else:
                    rows = self.students_data
            
            if not rows:
                with open(fp, "w", encoding="utf-8") as f:
                    f.write("")
                messagebox.showinfo("Export CSV", "No data to export.")
                return
            
            keys = sorted({k for r in rows for k in r.keys()})
            with open(fp, "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=keys)
                w.writeheader()
                for r in rows:
                    w.writerow(r)
            messagebox.showinfo("Export CSV", f"Wrote {len(rows)} rows.")
        except Exception as e:
            messagebox.showerror("Export CSV", str(e))

    def _get_search_term(self) -> str:
        """Lấy giá trị search hiện tại, coi placeholder như rỗng."""
        val = self.search_var.get().strip()
        if hasattr(self, "_placeholder_text") and val == self._placeholder_text:
            return ""
        return val