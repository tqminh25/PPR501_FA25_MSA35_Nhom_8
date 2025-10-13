"""
Grades Management View - Quản lý điểm số
"""

import tkinter as tk
from tkinter import ttk, messagebox
from .base_view import BaseContentView
from config.constants import COLORS


class GradesManagementView(BaseContentView):
    """View cho quản lý điểm số"""
    
    def __init__(self, parent_frame: ttk.Frame):
        # Khởi tạo dữ liệu trước khi gọi super().__init__()
        self.grades_data = []
        self._load_sample_data()
        
        super().__init__(parent_frame, "📝 Quản lý điểm số")
        self._setup_white_background()
    
    def _create_content(self):
        """Tạo nội dung quản lý điểm"""
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
    
    def _create_toolbar(self):
        """Tạo toolbar với các nút chức năng"""
        toolbar_frame = ttk.Frame(self.content_frame, style="White.TFrame")
        toolbar_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(0, 10))
        toolbar_frame.columnconfigure(1, weight=1)
        
        # Nút thêm điểm
        add_btn = ttk.Button(toolbar_frame, text="➕ Thêm điểm", 
                           command=self._add_grade)
        add_btn.grid(row=0, column=0, padx=(0, 10))
        
        # Nút sửa điểm
        edit_btn = ttk.Button(toolbar_frame, text="✏️ Sửa điểm", 
                            command=self._edit_grade)
        edit_btn.grid(row=0, column=1, padx=(0, 10))
        
        # Nút xóa điểm
        delete_btn = ttk.Button(toolbar_frame, text="🗑️ Xóa điểm", 
                              command=self._delete_grade)
        delete_btn.grid(row=0, column=2, padx=(0, 10))
        
        # Filter options
        filter_frame = ttk.Frame(toolbar_frame, style="White.TFrame")
        filter_frame.grid(row=0, column=3, sticky="e")
        
        ttk.Label(filter_frame, text="Lớp:", style="White.TLabel").grid(row=0, column=0, padx=(0, 5))
        self.class_var = tk.StringVar()
        class_combo = ttk.Combobox(filter_frame, textvariable=self.class_var, width=10)
        class_combo['values'] = ("Tất cả", "10A1", "10A2", "11A1", "11A2", "12A1")
        class_combo.set("Tất cả")
        class_combo.grid(row=0, column=1, padx=(0, 10))
        
        ttk.Label(filter_frame, text="Môn:", style="White.TLabel").grid(row=0, column=2, padx=(0, 5))
        self.subject_var = tk.StringVar()
        subject_combo = ttk.Combobox(filter_frame, textvariable=self.subject_var, width=10)
        subject_combo['values'] = ("Tất cả", "Toán", "Lý", "Hóa", "Sinh", "Văn")
        subject_combo.set("Tất cả")
        subject_combo.grid(row=0, column=3)
    
    def _create_grades_table(self):
        """Tạo bảng danh sách điểm"""
        # Frame cho table
        table_frame = ttk.Frame(self.content_frame, style="White.TFrame")
        table_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        # Treeview cho table
        columns = ("ID", "Họ tên", "Lớp", "Môn", "Điểm", "Loại thi", "Ngày")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # Cấu hình columns
        for col in columns:
            self.tree.heading(col, text=col)
        
        # Cấu hình width
        self.tree.column("ID", width=50, minwidth=50)
        self.tree.column("Họ tên", width=150, minwidth=120)
        self.tree.column("Lớp", width=80, minwidth=80)
        self.tree.column("Môn", width=80, minwidth=80)
        self.tree.column("Điểm", width=60, minwidth=60)
        self.tree.column("Loại thi", width=100, minwidth=100)
        self.tree.column("Ngày", width=100, minwidth=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Bind events
        self.tree.bind('<Double-1>', self._on_double_click)
        self.tree.bind('<Button-1>', self._on_select)
        
        # Load data
        self._load_grades_to_table()
    
    def _create_status_bar(self):
        """Tạo status bar"""
        self.status_frame = ttk.Frame(self.content_frame, style="White.TFrame")
        self.status_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))
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
            self.tree.insert("", "end", values=(
                grade["student_id"],
                grade["student_name"],
                grade["class"],
                grade["subject"],
                grade["score"],
                grade["exam_type"],
                grade["date"]
            ))
    
    def _on_double_click(self, event):
        """Xử lý double click"""
        self._edit_grade()
    
    def _on_select(self, event):
        """Xử lý khi chọn item"""
        pass
    
    def _add_grade(self):
        """Thêm điểm mới"""
        messagebox.showinfo("Thông báo", "Chức năng thêm điểm - Đang phát triển")
    
    def _edit_grade(self):
        """Sửa điểm"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn điểm cần sửa")
            return
        messagebox.showinfo("Thông báo", "Chức năng sửa điểm - Đang phát triển")
    
    def _delete_grade(self):
        """Xóa điểm"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn điểm cần xóa")
            return
        
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa điểm này?"):
            # Xóa khỏi data
            item = self.tree.item(selected[0])
            student_id = item['values'][0]
            self.grades_data = [g for g in self.grades_data if g['student_id'] != student_id]
            
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



