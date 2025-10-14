"""
Classes Management View - Quản lý lớp học
"""

import tkinter as tk
from tkinter import ttk, messagebox
from .base_view import BaseContentView
from config.constants import COLORS


class ClassesManagementView(BaseContentView):
    """View cho quản lý lớp học"""
    
    def __init__(self, parent_frame: ttk.Frame):
        # Khởi tạo dữ liệu trước khi gọi super().__init__()
        self.classes_data = []
        self._load_sample_data()
        
        super().__init__(parent_frame, "📚 Quản lý lớp học")
        self._setup_white_background()
    
    def _create_content(self):
        """Tạo nội dung quản lý lớp học"""
        # Toolbar
        self._create_toolbar()
        
        # Classes table
        self._create_classes_table()
        
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
        """Load dữ liệu mẫu cho lớp học"""
        self.classes_data = [
            {"class_id": "10A1", "class_name": "Lớp 10A1", "homeroom_teacher": "Nguyễn Văn A", 
             "student_count": 35, "room": "A101", "schedule": "Sáng"},
            {"class_id": "10A2", "class_name": "Lớp 10A2", "homeroom_teacher": "Trần Thị B", 
             "student_count": 32, "room": "A102", "schedule": "Sáng"},
            {"class_id": "11A1", "class_name": "Lớp 11A1", "homeroom_teacher": "Lê Văn C", 
             "student_count": 30, "room": "B101", "schedule": "Chiều"},
            {"class_id": "11A2", "class_name": "Lớp 11A2", "homeroom_teacher": "Phạm Thị D", 
             "student_count": 28, "room": "B102", "schedule": "Chiều"},
            {"class_id": "12A1", "class_name": "Lớp 12A1", "homeroom_teacher": "Hoàng Văn E", 
             "student_count": 33, "room": "C101", "schedule": "Sáng"},
        ]
    
    def _create_toolbar(self):
        """Tạo toolbar với các nút chức năng"""
        toolbar_frame = ttk.Frame(self.content_frame, style="White.TFrame")
        toolbar_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(0, 10))
        toolbar_frame.columnconfigure(1, weight=1)
        
        # Nút thêm lớp
        add_btn = ttk.Button(toolbar_frame, text="➕ Thêm lớp", 
                           command=self._add_class)
        add_btn.grid(row=0, column=0, padx=(0, 10))
        
        # Nút sửa lớp
        edit_btn = ttk.Button(toolbar_frame, text="✏️ Sửa lớp", 
                            command=self._edit_class)
        edit_btn.grid(row=0, column=1, padx=(0, 10))
        
        # Nút xóa lớp
        delete_btn = ttk.Button(toolbar_frame, text="🗑️ Xóa lớp", 
                              command=self._delete_class)
        delete_btn.grid(row=0, column=2, padx=(0, 10))
        
        # Search box
        search_frame = ttk.Frame(toolbar_frame, style="White.TFrame")
        search_frame.grid(row=0, column=3, sticky="e")
        
        ttk.Label(search_frame, text="Tìm kiếm:", style="White.TLabel").grid(row=0, column=0, padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=20)
        self.search_entry.grid(row=0, column=1)
        self.search_entry.bind('<KeyRelease>', self._on_search)
    
    def _create_classes_table(self):
        """Tạo bảng danh sách lớp học"""
        # Frame cho table
        table_frame = ttk.Frame(self.content_frame, style="White.TFrame")
        table_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        # Treeview cho table
        columns = ("Mã lớp", "Tên lớp", "GVCN", "Số HS", "Phòng", "Ca học")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # Cấu hình columns
        for col in columns:
            self.tree.heading(col, text=col)
        
        # Cấu hình width
        self.tree.column("Mã lớp", width=80, minwidth=80)
        self.tree.column("Tên lớp", width=120, minwidth=120)
        self.tree.column("GVCN", width=150, minwidth=120)
        self.tree.column("Số HS", width=80, minwidth=80)
        self.tree.column("Phòng", width=80, minwidth=80)
        self.tree.column("Ca học", width=80, minwidth=80)
        
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
        self._load_classes_to_table()
    
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
    
    def _load_classes_to_table(self):
        """Load dữ liệu lớp học vào table"""
        # Xóa dữ liệu cũ
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Thêm dữ liệu mới
        for class_item in self.classes_data:
            self.tree.insert("", "end", values=(
                class_item["class_id"],
                class_item["class_name"],
                class_item["homeroom_teacher"],
                class_item["student_count"],
                class_item["room"],
                class_item["schedule"]
            ))
    
    def _on_search(self, event=None):
        """Xử lý tìm kiếm"""
        search_term = self.search_var.get().lower()
        if not search_term:
            self._load_classes_to_table()
            return
        
        # Filter data
        filtered_data = [
            class_item for class_item in self.classes_data
            if search_term in class_item["class_name"].lower() or 
               search_term in class_item["homeroom_teacher"].lower() or
               search_term in class_item["class_id"].lower()
        ]
        
        # Update table
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for class_item in filtered_data:
            self.tree.insert("", "end", values=(
                class_item["class_id"],
                class_item["class_name"],
                class_item["homeroom_teacher"],
                class_item["student_count"],
                class_item["room"],
                class_item["schedule"]
            ))
    
    def _on_double_click(self, event):
        """Xử lý double click"""
        self._edit_class()
    
    def _on_select(self, event):
        """Xử lý khi chọn item"""
        pass
    
    def _add_class(self):
        """Thêm lớp mới"""
        messagebox.showinfo("Thông báo", "Chức năng thêm lớp - Đang phát triển")
    
    def _edit_class(self):
        """Sửa thông tin lớp"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn lớp cần sửa")
            return
        messagebox.showinfo("Thông báo", "Chức năng sửa lớp - Đang phát triển")
    
    def _delete_class(self):
        """Xóa lớp"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn lớp cần xóa")
            return
        
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa lớp này?"):
            # Xóa khỏi data
            item = self.tree.item(selected[0])
            class_id = item['values'][0]
            self.classes_data = [c for c in self.classes_data if c['class_id'] != class_id]
            
            # Cập nhật table
            self._load_classes_to_table()
            self._update_status()
            messagebox.showinfo("Thành công", "Đã xóa lớp thành công")
    
    def _update_status(self):
        """Cập nhật status bar"""
        total_classes = len(self.classes_data)
        self.status_label.config(text=f"Tổng số lớp: {total_classes}")
    
    def refresh(self):
        """Refresh view"""
        self._load_classes_to_table()
        self._update_status()



