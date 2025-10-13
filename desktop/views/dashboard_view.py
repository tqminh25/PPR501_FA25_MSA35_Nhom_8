"""
Dashboard View - Trang chủ dashboard
"""

import tkinter as tk
from tkinter import ttk
from .base_view import BaseContentView
from config.constants import COLORS


class DashboardView(BaseContentView):
    """View cho dashboard chính"""
    
    def __init__(self, parent_frame: ttk.Frame):
        # Khởi tạo dữ liệu trước khi gọi super().__init__()
        self.dashboard_data = {}
        self._load_sample_data()
        
        super().__init__(parent_frame, "📊 Dashboard")
        self._setup_white_background()
    
    def _create_content(self):
        """Tạo nội dung dashboard"""
        # Welcome section
        self._create_welcome_section()
        
        # Statistics cards
        self._create_statistics_cards()
        
        # Recent activities
        self._create_recent_activities()
        
        # Cập nhật background sau khi tạo xong
        self._update_white_background()
    
    def _setup_white_background(self):
        """Thiết lập background màu trắng cho toàn bộ view"""
        # Cấu hình background cho frame chính
        self.main_frame.configure(style="White.TFrame")
        
        # Cấu hình background cho content frame
        self.content_frame.configure(style="White.TFrame")
    
    def _update_white_background(self):
        """Cập nhật background màu trắng cho tất cả các frame con"""
        # Cấu hình background cho các frame con
        for widget in self.content_frame.winfo_children():
            if isinstance(widget, ttk.Frame):
                widget.configure(style="White.TFrame")
                # Cập nhật cho các frame con bên trong
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Frame):
                        child.configure(style="White.TFrame")
    
    def _load_sample_data(self):
        """Load dữ liệu mẫu cho dashboard"""
        self.dashboard_data = {
            'total_students': 1500,
            'total_classes': 50,
            'avg_score': 8.2,
            'active_teachers': 25,
            'recent_activities': [
                "Học sinh Nguyễn Văn A đạt điểm cao môn Toán",
                "Lớp 10A1 có 95% học sinh đạt điểm khá giỏi",
                "Cập nhật thông tin học sinh mới",
                "Báo cáo tháng 12 đã được tạo",
                "Họp phụ huynh lớp 11A1"
            ]
        }
    
    def _create_welcome_section(self):
        """Tạo phần chào mừng"""
        welcome_frame = ttk.Frame(self.content_frame, style="White.TFrame")
        welcome_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        welcome_frame.columnconfigure(0, weight=1)
        
        welcome_label = ttk.Label(welcome_frame, 
                                text="Chào mừng đến với hệ thống quản lý trường học", 
                                style="White.TLabel", font=("Helvetica", 16, "bold"))
        welcome_label.grid(row=0, column=0, pady=10)
        
        subtitle_label = ttk.Label(welcome_frame, 
                                 text="Quản lý học sinh, điểm số và báo cáo một cách hiệu quả", 
                                 style="White.TLabel", font=("Helvetica", 12))
        subtitle_label.grid(row=1, column=0, pady=5)
    
    def _create_statistics_cards(self):
        """Tạo các thẻ thống kê"""
        stats_frame = ttk.Frame(self.content_frame, style="White.TFrame")
        stats_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        stats_frame.columnconfigure(0, weight=1)
        stats_frame.columnconfigure(1, weight=1)
        stats_frame.columnconfigure(2, weight=1)
        stats_frame.columnconfigure(3, weight=1)
        
        # Tạo 4 thẻ thống kê
        self._create_stat_card(stats_frame, "👥 Tổng học sinh", 
                             str(self.dashboard_data['total_students']), 
                             COLORS['primary'], 0, 0)
        
        self._create_stat_card(stats_frame, "📚 Tổng lớp học", 
                             str(self.dashboard_data['total_classes']), 
                             COLORS['secondary'], 0, 1)
        
        self._create_stat_card(stats_frame, "📊 Điểm TB", 
                             str(self.dashboard_data['avg_score']), 
                             COLORS['accent'], 0, 2)
        
        self._create_stat_card(stats_frame, "👨‍🏫 Giáo viên", 
                             str(self.dashboard_data['active_teachers']), 
                             COLORS['success'], 0, 3)
    
    def _create_stat_card(self, parent, title, value, color, row, col):
        """Tạo một thẻ thống kê"""
        card = ttk.Frame(parent, style="White.TFrame", relief="solid", borderwidth=1, padding=15)
        card.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        card.columnconfigure(0, weight=1)
        
        title_label = ttk.Label(card, text=title, font=("Helvetica", 12, "bold"), 
                              background="white", foreground=COLORS['text_secondary'])
        title_label.pack(pady=(0, 5))
        
        value_label = ttk.Label(card, text=value, font=("Helvetica", 24, "bold"), 
                              background="white", foreground=color)
        value_label.pack()
    
    def _create_recent_activities(self):
        """Tạo phần hoạt động gần đây"""
        activities_frame = ttk.Frame(self.content_frame, style="White.TFrame")
        activities_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        activities_frame.columnconfigure(0, weight=1)
        activities_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(activities_frame, text="🕒 Hoạt động gần đây", 
                              style="White.TLabel", font=("Helvetica", 14, "bold"))
        title_label.grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        # Activities list
        activities_list = tk.Text(activities_frame, wrap="word", height=8, 
                                font=("Helvetica", 11), bg="white", fg=COLORS['text_primary'])
        activities_list.grid(row=1, column=0, sticky="nsew")
        
        # Thêm dữ liệu hoạt động
        for activity in self.dashboard_data['recent_activities']:
            activities_list.insert("end", f"• {activity}\n")
        
        activities_list.config(state="disabled")  # Chỉ đọc
    
    def refresh(self):
        """Refresh dashboard data"""
        self._load_sample_data()
        # Có thể thêm logic refresh UI ở đây



