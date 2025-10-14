"""
Grades Management View - Quản lý điểm số
"""

import tkinter as tk
from tkinter import ttk, messagebox
from .base_view import BaseContentView
from config.constants import COLORS
from models import api_client


class GradesManagementView(BaseContentView):
    """View cho quản lý điểm số"""
    
    def __init__(self, parent_frame: ttk.Frame):
        # Khởi tạo dữ liệu trước khi gọi super().__init__()
        self.grades_data = []
        # self._load_sample_data()
        self.load_students()
        
        super().__init__(parent_frame, "📝 Quản lý điểm số")
        self._setup_white_background()
    
    def _create_content(self):
        """Tạo nội dung quản lý điểm"""
        # Cấu hình grid weights cho content_frame
        self.content_frame.rowconfigure(0, weight=0)  # Toolbar - không expand
        self.content_frame.rowconfigure(1, weight=1)  # Table - expand toàn bộ
        self.content_frame.rowconfigure(2, weight=0)  # Status bar - không expand
        
        # Toolbar
        self._create_toolbar()
        
        # Grades table
        self._create_grades_table()
        
        # Status bar
        self._create_status_bar()
        
        # Cập nhật background sau khi tạo xong
        self._update_white_background()
    
    def _setup_white_background(self):
        """Thiết lập background màu trắng cho toàn bộ view"""
        self.main_frame.configure(style="White.TFrame")
        self.content_frame.configure(style="White.TFrame")
    
    def _update_white_background(self):
        """Cập nhật background màu trắng cho tất cả các frame con"""
        for widget in self.content_frame.winfo_children():
            if isinstance(widget, ttk.Frame):
                widget.configure(style="White.TFrame")
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Frame):
                        child.configure(style="White.TFrame")
    
    def _load_sample_data(self):
        """Load dữ liệu mẫu cho điểm số"""
        self.grades_data = [
            {"student_id": 1, "student_name": "Nguyễn Văn An", "class": "10A1", 
             "subject": "Toán", "score": 8.5, "exam_type": "Giữa kỳ", "date": "2024-01-15"},
            {"student_id": 2, "student_name": "Trần Thị Bình", "class": "10A1", 
             "subject": "Toán", "score": 9.2, "exam_type": "Giữa kỳ", "date": "2024-01-15"},
            {"student_id": 3, "student_name": "Lê Văn Cường", "class": "10A2", 
             "subject": "Lý", "score": 7.8, "exam_type": "Cuối kỳ", "date": "2024-01-20"},
            {"student_id": 4, "student_name": "Phạm Thị Dung", "class": "10A2", 
             "subject": "Hóa", "score": 8.9, "exam_type": "Giữa kỳ", "date": "2024-01-18"},
            {"student_id": 5, "student_name": "Hoàng Văn Em", "class": "11A1", 
             "subject": "Sinh", "score": 8.1, "exam_type": "Cuối kỳ", "date": "2024-01-22"},
        ]

    def load_students(self):
        """Load danh sách học sinh"""
        try:
            response = api_client.get_students(page=1, page_size=1000, search="")
            # Lấy danh sách học sinh từ response
            if isinstance(response, dict) and "items" in response:
                self.grades_data = response["items"]
            else:
                self.grades_data = response if isinstance(response, list) else []
            print("Binh test grades_data 2", self.grades_data)
        except Exception as e:
            print(f"Error loading students: {e}")
            self.grades_data = []
    
    def _create_toolbar(self):
        """Tạo toolbar với các nút chức năng"""
        toolbar_frame = ttk.Frame(self.content_frame, style="White.TFrame")
        toolbar_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=(0, 5))
        toolbar_frame.columnconfigure(1, weight=1)
        
        # Nút thêm điểm
        add_btn = ttk.Button(toolbar_frame, text="➕ Thêm điểm", 
                           command=self._add_grade)
        add_btn.grid(row=0, column=0, padx=(0, 5))
        
        # Nút sửa điểm
        edit_btn = ttk.Button(toolbar_frame, text="✏️ Sửa điểm", 
                            command=self._edit_grade)
        edit_btn.grid(row=0, column=1, padx=(0, 5))
        
        # Nút xóa điểm
        delete_btn = ttk.Button(toolbar_frame, text="🗑️ Xóa điểm", 
                              command=self._delete_grade)
        delete_btn.grid(row=0, column=2, padx=(0, 5))
        
        # Nút refresh
        refresh_btn = ttk.Button(toolbar_frame, text="🔄 Refresh", 
                               command=self._refresh_data)
        refresh_btn.grid(row=0, column=3, padx=(0, 5))
        
        # Filter options
        filter_frame = ttk.Frame(toolbar_frame, style="White.TFrame")
        filter_frame.grid(row=0, column=4, sticky="e")
        
        ttk.Label(filter_frame, text="Lớp:", style="White.TLabel").grid(row=0, column=0, padx=(0, 3))
        self.class_var = tk.StringVar()
        class_combo = ttk.Combobox(filter_frame, textvariable=self.class_var, width=8)
        class_combo['values'] = ("Tất cả", "10A1", "10A2", "11A1", "11A2", "12A1")
        class_combo.set("Tất cả")
        class_combo.grid(row=0, column=1, padx=(0, 5))
        
        ttk.Label(filter_frame, text="Môn:", style="White.TLabel").grid(row=0, column=2, padx=(0, 3))
        self.subject_var = tk.StringVar()
        subject_combo = ttk.Combobox(filter_frame, textvariable=self.subject_var, width=8)
        subject_combo['values'] = ("Tất cả", "Toán", "Lý", "Hóa", "Sinh", "Văn")
        subject_combo.set("Tất cả")
        subject_combo.grid(row=0, column=3)
    
    def _create_grades_table(self):
        """Tạo bảng danh sách điểm"""
        # Frame cho table
        table_frame = ttk.Frame(self.content_frame, style="White.TFrame")
        table_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=(0, 5))
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        # Treeview cho table - sử dụng toàn bộ chiều cao có sẵn
        columns = ("ID", "Họ tên", "Toán", "Văn", "Anh", "GPA", "Sửa")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # Cấu hình columns
        for col in columns:
            self.tree.heading(col, text=col)
        
        # Cấu hình width
        self.tree.column("ID", width=50, minwidth=50)
        self.tree.column("Họ tên", width=150, minwidth=120)
        self.tree.column("Toán", width=80, minwidth=80)
        self.tree.column("Văn", width=80, minwidth=80)
        self.tree.column("Anh", width=60, minwidth=60)
        self.tree.column("GPA", width=100, minwidth=100)
        self.tree.column("Sửa", width=80, minwidth=80)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Bind events
        self.tree.bind('<Double-1>', self._on_double_click)
        self.tree.bind('<Button-1>', self._on_click)
        
        # Load data
        self._load_grades_to_table()
    
    def _create_status_bar(self):
        """Tạo status bar"""
        self.status_frame = ttk.Frame(self.content_frame, style="White.TFrame")
        self.status_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=(0, 5))
        self.status_frame.columnconfigure(0, weight=1)
        
        self.status_label = ttk.Label(self.status_frame, text="Sẵn sàng", 
                                    style="White.TLabel")
        self.status_label.grid(row=0, column=0, sticky="w")
        
        # Cập nhật status
        self._update_status()
    
    def _load_grades_to_table(self):
        """Load dữ liệu điểm vào table"""
        # Xóa dữ liệu cũ
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Thêm dữ liệu mới
        for grade in self.grades_data:
            # Tính GPA (trung bình cộng 3 môn)
            math_score = grade.get("math_score") or 0
            lit_score = grade.get("literature_score") or 0
            eng_score = grade.get("english_score") or 0
            
            # Chỉ tính GPA nếu có ít nhất 1 điểm
            if math_score or lit_score or eng_score:
                gpa = (math_score + lit_score + eng_score) / 3
            else:
                gpa = 0
                
            # Thêm dữ liệu vào tree với cột Sửa
            item = self.tree.insert("", "end", values=(
                grade.get("student_code", ""),
                f"{grade.get('first_name', '')} {grade.get('last_name', '')}".strip(),
                math_score if math_score else "",
                lit_score if lit_score else "",
                eng_score if eng_score else "",
                round(gpa, 2) if gpa else "",
                "✏️ Sửa"  # Cột Sửa trong bảng
            ))
            
            # Lưu grade data vào item để có thể truy cập sau
            self.tree.set(item, "Sửa", "✏️ Sửa")
    
    def _on_click(self, event):
        """Xử lý click vào table"""
        # Lấy item được click
        item = self.tree.identify('item', event.x, event.y)
        column = self.tree.identify('column', event.x, event.y)
        
        if item and column:
            # Kiểm tra xem có click vào cột "Sửa" không (cột cuối cùng)
            try:
                column_index = int(column[1:]) - 1  # Bỏ ký tự # ở đầu
                if column_index == 6:  # Cột "Sửa" là cột thứ 7 (index 6)
                    # Lấy dữ liệu học sinh từ item
                    values = self.tree.item(item)['values']
                    student_code = values[0]
                    
                    # Tìm grade data tương ứng
                    for grade in self.grades_data:
                        if grade.get("student_code") == student_code:
                            self._edit_grade_for_student(grade)
                            break
            except (ValueError, IndexError):
                pass
    
    def _on_double_click(self, event):
        """Xử lý double click"""
        self._edit_grade()
    
    def _on_select(self, event):
        """Xử lý khi chọn item"""
        pass
    
    def _add_grade(self):
        """Thêm điểm mới"""
        messagebox.showinfo("Thông báo", "Chức năng thêm điểm - Đang phát triển")
    
    def _edit_grade_for_student(self, grade_data):
        """Sửa điểm cho học sinh cụ thể"""
        student_code = grade_data.get("student_code", "")
        student_name = f"{grade_data.get('first_name', '')} {grade_data.get('last_name', '')}".strip()
        current_math = grade_data.get("math_score") or ""
        current_lit = grade_data.get("literature_score") or ""
        current_eng = grade_data.get("english_score") or ""
        
        # Tạo popup sửa điểm
        self._show_edit_grades_popup(student_code, student_name, current_math, current_lit, current_eng)
    
    def _edit_grade(self):
        """Sửa điểm (cho double click)"""
        # Lấy item được chọn
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn học sinh cần sửa điểm")
            return
        
        # Lấy thông tin học sinh
        item = self.tree.item(selected[0])
        values = item['values']
        student_code = values[0]
        student_name = values[1]
        current_math = values[2] if values[2] else ""
        current_lit = values[3] if values[3] else ""
        current_eng = values[4] if values[4] else ""
        
        # Tạo popup sửa điểm
        self._show_edit_grades_popup(student_code, student_name, current_math, current_lit, current_eng)
    
    def _show_edit_grades_popup(self, student_code, student_name, current_math, current_lit, current_eng):
        """Hiển thị popup sửa điểm"""
        # Tạo popup window - sử dụng parent_frame thay vì self
        popup = tk.Toplevel(self.parent_frame.winfo_toplevel())
        popup.title(f"Sửa điểm - {student_name}")
        popup.geometry("400x300")
        popup.resizable(False, False)
        
        # Căn giữa popup
        popup.transient(self.parent_frame.winfo_toplevel())
        popup.grab_set()
        
        # Main frame
        main_frame = ttk.Frame(popup, padding=20)
        main_frame.pack(fill="both", expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text=f"Sửa điểm cho {student_name}", 
                               font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Form frame
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill="x", pady=(0, 20))
        
        # Điểm Toán
        ttk.Label(form_frame, text="Điểm Toán:").grid(row=0, column=0, sticky="w", pady=5)
        math_var = tk.StringVar(value=str(current_math))
        math_entry = ttk.Entry(form_frame, textvariable=math_var, width=20)
        math_entry.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=5)
        
        # Điểm Văn
        ttk.Label(form_frame, text="Điểm Văn:").grid(row=1, column=0, sticky="w", pady=5)
        lit_var = tk.StringVar(value=str(current_lit))
        lit_entry = ttk.Entry(form_frame, textvariable=lit_var, width=20)
        lit_entry.grid(row=1, column=1, sticky="ew", padx=(10, 0), pady=5)
        
        # Điểm Anh
        ttk.Label(form_frame, text="Điểm Anh:").grid(row=2, column=0, sticky="w", pady=5)
        eng_var = tk.StringVar(value=str(current_eng))
        eng_entry = ttk.Entry(form_frame, textvariable=eng_var, width=20)
        eng_entry.grid(row=2, column=1, sticky="ew", padx=(10, 0), pady=5)
        
        # Cấu hình grid
        form_frame.columnconfigure(1, weight=1)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(0, 10))
        
        # Buttons
        def save_grades():
            try:
                # Validate input
                math_score = float(math_var.get()) if math_var.get().strip() else None
                lit_score = float(lit_var.get()) if lit_var.get().strip() else None
                eng_score = float(eng_var.get()) if eng_var.get().strip() else None
                
                # Validate range
                for score, name in [(math_score, "Toán"), (lit_score, "Văn"), (eng_score, "Anh")]:
                    if score is not None and (score < 0 or score > 10):
                        messagebox.showerror("Lỗi", f"Điểm {name} phải từ 0 đến 10")
                        return
                
                # Tạo payload
                grades = {}
                if math_score is not None:
                    grades["math_score"] = math_score
                if lit_score is not None:
                    grades["literature_score"] = lit_score
                if eng_score is not None:
                    grades["english_score"] = eng_score
                
                # Gọi API
                print(f"Updating grades for {student_code}: {grades}")
                updated_student = api_client.update_student_grades(student_code, grades)
                print(f"API response: {updated_student}")
                
                # Cập nhật local data
                found = False
                for i, student in enumerate(self.grades_data):
                    if student.get("student_code") == student_code:
                        # Cập nhật từng field riêng biệt
                        if "math_score" in updated_student:
                            self.grades_data[i]["math_score"] = updated_student["math_score"]
                        if "literature_score" in updated_student:
                            self.grades_data[i]["literature_score"] = updated_student["literature_score"]
                        if "english_score" in updated_student:
                            self.grades_data[i]["english_score"] = updated_student["english_score"]
                        found = True
                        print(f"Updated local data for {student_code}")
                        break
                
                if not found:
                    print(f"Warning: Student {student_code} not found in local data")
                
                # Refresh table
                print("Refreshing table...")
                self._load_grades_to_table()
                self._update_status()
                print("Table refreshed successfully")
                
                # Backup: Reload data from server để đảm bảo sync
                try:
                    print("Reloading data from server as backup...")
                    self.load_students()
                    self._load_grades_to_table()
                    self._update_status()
                    print("Server reload completed")
                except Exception as e:
                    print(f"Server reload failed: {e}")
                
                messagebox.showinfo("Thành công", "Đã cập nhật điểm thành công")
                popup.destroy()
                
            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập điểm hợp lệ (số từ 0 đến 10)")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể cập nhật điểm: {str(e)}")
        
        def cancel():
            popup.destroy()
        
        ttk.Button(button_frame, text="Hủy", command=cancel).pack(side="right", padx=(10, 0))
        ttk.Button(button_frame, text="Lưu", command=save_grades).pack(side="right")
        
        # Focus vào entry đầu tiên
        math_entry.focus()
        
        # Bind Enter key
        popup.bind('<Return>', lambda e: save_grades())
        popup.bind('<Escape>', lambda e: cancel())
    
    def _delete_grade(self):
        """Xóa điểm"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn điểm cần xóa")
            return
        
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa điểm này?"):
            # Xóa khỏi data
            item = self.tree.item(selected[0])
            student_code = item['values'][0]  # Lấy student_code thay vì student_id
            self.grades_data = [g for g in self.grades_data if g.get('student_code') != student_code]
            
            # Cập nhật table
            self._load_grades_to_table()
            self._update_status()
            messagebox.showinfo("Thành công", "Đã xóa điểm thành công")
    
    def _update_status(self):
        """Cập nhật status bar"""
        total_grades = len(self.grades_data)
        self.status_label.config(text=f"Tổng số điểm: {total_grades}")
    
    def refresh(self):
        """Refresh view"""
        self._load_grades_to_table()
        self._update_status()
    
    def _refresh_data(self):
        """Refresh dữ liệu từ server"""
        try:
            print("Refreshing data from server...")
            self.load_students()
            self._load_grades_to_table()
            self._update_status()
            messagebox.showinfo("Thành công", "Đã refresh dữ liệu từ server")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể refresh dữ liệu: {str(e)}")
    



