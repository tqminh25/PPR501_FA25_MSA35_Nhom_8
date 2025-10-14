"""
App View - UI cho màn hình ứng dụng chính
"""

import tkinter as tk
from tkinter import messagebox, ttk
from typing import TYPE_CHECKING

from config.styles import AppStyles
from config.constants import MENU_ITEMS, HEADER_HEIGHT, SIDEBAR_WIDTH_PERCENT, SIDEBAR_COLLAPSED_WIDTH, SIDEBAR_EXPANDED_WIDTH_PERCENT, CONTENT_PADDING
from utils.window_utils import WindowUtils
from .student_management_view import StudentManagementView
from .report_view import ReportView
from .dashboard_view import DashboardView
from .grades_management_view import GradesManagementView
from .classes_management_view import ClassesManagementView

if TYPE_CHECKING:
    from views.login_view import LoginView


class AppWindow(tk.Frame):
    """Màn hình App chính sau khi login"""
    
    def __init__(self, parent: 'LoginView', username: str, remember: str):
        super().__init__(parent)
        self.parent = parent
        self.username = username
        self.remember = remember
        self.current_page = "dashboard"
        
        # Sidebar state
        self.sidebar_collapsed = False
        
        # View instances
        self.views = {}
        self.current_view = None
        
        self._setup_window()
        self._initialize_style()
        self._create_layout()
    
    def _setup_window(self):
        """Thiết lập cửa sổ App"""
        # Pack để fill toàn bộ parent window
        self.pack(fill="both", expand=True)
    
    def _initialize_style(self):
        """Khởi tạo style cho App"""
        self.style = AppStyles.initialize_app_styles()
    
    def _create_layout(self):
        """Tạo bố cục chính"""
        # Main container
        self.main_container = ttk.Frame(self)
        self.main_container.grid(row=0, column=0, sticky="nsew")
        self.main_container.configure(style="TFrame")
        
        # Cấu hình responsive layout
        self._setup_responsive_layout()
        
        # Header
        self._create_header()
        
        # Sidebar
        self._create_sidebar()
        
        # Content area
        self._create_content_area()
        
        # Bind resize event
        WindowUtils.bind_resize_event(self.master, self._on_window_resize)
    
    def _setup_responsive_layout(self):
        """Thiết lập responsive layout"""
        # Cấu hình grid weights cho responsive
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        # Main container layout
        self.main_container.columnconfigure(0, weight=0)  # Sidebar
        self.main_container.columnconfigure(1, weight=1)  # Content
        self.main_container.rowconfigure(0, weight=0)     # Header
        self.main_container.rowconfigure(1, weight=1)     # Main content
    
    def _on_window_resize(self):
        """Xử lý khi window resize"""
        self.master.after(100, self._update_layout)
    
    def _update_layout(self):
        """Cập nhật layout khi resize"""
        try:
            window_width = self.winfo_width()
            
            if self.sidebar_collapsed:
                sidebar_width = SIDEBAR_COLLAPSED_WIDTH
            else:
                sidebar_width = int(window_width * SIDEBAR_EXPANDED_WIDTH_PERCENT)
            
            # Cập nhật minsize cho sidebar
            self.main_container.columnconfigure(0, weight=0, minsize=sidebar_width)
            
            # Cập nhật chiều cao header
            self.header_frame.configure(height=HEADER_HEIGHT)
            
        except tk.TclError:
            pass  # Window đã bị destroy
    
    def _create_header(self):
        """Tạo header bar"""
        self.header_frame = ttk.Frame(self.main_container, style="Header.TFrame")
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=0, pady=0)
        self.header_frame.columnconfigure(2, weight=1)
        
        # Thiết lập chiều cao header
        self.header_frame.configure(height=HEADER_HEIGHT)
        
        # Toggle button
        self.toggle_btn = ttk.Button(self.header_frame, text="☰", style="Toggle.TButton", 
                                   command=self._toggle_sidebar, width=3)
        self.toggle_btn.grid(row=0, column=0, padx=15, pady=15, sticky="w")
        
        # Logo và tên app
        logo_label = ttk.Label(self.header_frame, text="🎓 EduManager Pro", style="Header.TLabel")
        logo_label.grid(row=0, column=1, padx=20, pady=15, sticky="w")
        
        # Thông tin user và logout
        user_frame = ttk.Frame(self.header_frame, style="Header.TFrame")
        user_frame.grid(row=0, column=2, padx=20, pady=15, sticky="e")
        
        user_label = ttk.Label(user_frame, text=f"👤 {self.username}", style="Header.TLabel")
        user_label.grid(row=0, column=0, padx=(0, 10))
    
    def _create_sidebar(self):
        """Tạo menu trái với khả năng toggle"""
        self.sidebar_frame = ttk.Frame(self.main_container, style="Sidebar.TFrame")
        self.sidebar_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        self.sidebar_frame.columnconfigure(0, weight=1)
        
        # Tạo menu buttons container
        self.menu_container = ttk.Frame(self.sidebar_frame, style="Sidebar.TFrame")
        self.menu_container.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.menu_container.columnconfigure(0, weight=1)
        
        # Tạo menu buttons
        self.menu_buttons = []
        for i, (icon, text, page) in enumerate(MENU_ITEMS):
            btn = ttk.Button(self.menu_container, text=f"{icon} {text}", style="Sidebar.TButton", 
                           command=lambda p=page: self._navigate_to_page(p))
            btn.grid(row=i, column=0, sticky="ew", padx=10, pady=5)
            self.menu_buttons.append((btn, icon, text, page))
            
            # Thêm tooltip cho button
            self._create_tooltip(btn, text)
        
        # Thông tin user ở cuối sidebar
        self.user_info_frame = ttk.Frame(self.sidebar_frame, style="Sidebar.TFrame")
        self.user_info_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=20)
        self.user_info_frame.columnconfigure(0, weight=1)
        
        self.user_info_label = ttk.Label(self.user_info_frame, text=f"👤 {self.username}", style="Sidebar.TLabel")
        self.user_info_label.grid(row=0, column=0, pady=5)
        
        if self.remember:
            self.remember_label = ttk.Label(self.user_info_frame, text="💾 Đã ghi nhớ", style="Sidebar.TLabel")
            self.remember_label.grid(row=1, column=0, pady=2)
        
        # Cập nhật layout ban đầu
        self._update_sidebar_layout()
    
    def _toggle_sidebar(self):
        """Toggle sidebar giữa expanded và collapsed"""
        self.sidebar_collapsed = not self.sidebar_collapsed
        self._update_sidebar_layout()
        self._update_layout()
    
    def _update_sidebar_layout(self):
        """Cập nhật layout của sidebar dựa trên trạng thái"""
        if self.sidebar_collapsed:
            # Collapsed state - chỉ hiển thị icon
            for btn, icon, text, page in self.menu_buttons:
                btn.configure(text=icon, style="CollapsedSidebar.TButton", width=3)
            
            # Ẩn user info text, chỉ hiển thị icon
            self.user_info_label.configure(text="👤")
            if self.remember:
                self.remember_label.configure(text="💾")
            
            # Cập nhật toggle button
            self.toggle_btn.configure(text="☰")
            
        else:
            # Expanded state - hiển thị đầy đủ
            for btn, icon, text, page in self.menu_buttons:
                btn.configure(text=f"{icon} {text}", style="Sidebar.TButton", width=0)
            
            # Hiển thị đầy đủ user info
            self.user_info_label.configure(text=f"👤 {self.username}")
            if self.remember:
                self.remember_label.configure(text="💾 Đã ghi nhớ")
            
            # Cập nhật toggle button
            self.toggle_btn.configure(text="✕")
    
    def _create_tooltip(self, widget, text):
        """Tạo tooltip cho widget"""
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(tooltip, text=text, background="#ffffe0", 
                           relief="solid", borderwidth=1, font=("Helvetica", 9))
            label.pack()
            
            widget.tooltip = tooltip
        
        def hide_tooltip(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                delattr(widget, 'tooltip')
        
        widget.bind("<Enter>", show_tooltip)
        widget.bind("<Leave>", hide_tooltip)
    
    def _create_content_area(self):
        """Tạo vùng content chính"""
        self.content_frame = ttk.Frame(self.main_container, style="Content.TFrame")
        self.content_frame.grid(row=1, column=1, sticky="nsew", padx=CONTENT_PADDING, pady=CONTENT_PADDING)
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(0, weight=1)
        
        # Hiển thị trang mặc định
        self._show_dashboard()
    
    def _navigate_to_page(self, page: str):
        """Điều hướng đến trang"""
        self.current_page = page
        
        # Ẩn view hiện tại
        if self.current_view:
            self.current_view.hide()
        
        # Hiển thị view mới
        if page == "dashboard":
            self._show_dashboard()
        elif page == "students":
            self._show_students()
        elif page == "grades":
            self._show_grades()
        elif page == "classes":
            self._show_classes()
        elif page == "reports":
            self._show_reports()
        elif page == "logout":
            self._logout()
        
    
    def _show_dashboard(self):
        """Hiển thị trang Dashboard"""
        # Ẩn view hiện tại
        if self.current_view:
            self.current_view.hide()
        
        # Tạo hoặc lấy dashboard view
        if "dashboard" not in self.views:
            self.views["dashboard"] = DashboardView(self.content_frame)
        self.current_view = self.views["dashboard"]
        self.current_view.show()
    
    def _show_students(self):
        """Hiển thị trang Quản lý học sinh"""
        # Ẩn view hiện tại
        if self.current_view:
            self.current_view.hide()
        
        # Tạo hoặc lấy StudentManagementView
        if "students" not in self.views:
            self.views["students"] = StudentManagementView(self.content_frame)
        
        self.current_view = self.views["students"]
        self.current_view.show()
    
    def _show_grades(self):
        """Hiển thị trang Quản lý điểm"""
        # Ẩn view hiện tại
        if self.current_view:
            self.current_view.hide()
        
        # Tạo hoặc lấy grades view
        if "grades" not in self.views:
            self.views["grades"] = GradesManagementView(self.content_frame)
        self.current_view = self.views["grades"]
        self.current_view.show()
    
    def _show_classes(self):
        """Hiển thị trang Quản lý lớp học"""
        # Ẩn view hiện tại
        if self.current_view:
            self.current_view.hide()
        
        # Tạo hoặc lấy classes view
        if "classes" not in self.views:
            self.views["classes"] = ClassesManagementView(self.content_frame)
        self.current_view = self.views["classes"]
        self.current_view.show()
    
    def _show_reports(self):
        """Hiển thị trang Báo cáo"""
        # Ẩn view hiện tại
        if self.current_view:
            self.current_view.hide()
        
        # Tạo hoặc lấy ReportView
        if "reports" not in self.views:
            self.views["reports"] = ReportView(self.content_frame)
        
        self.current_view = self.views["reports"]
        self.current_view.show()
    
    
    def _logout(self):
        """Đăng xuất"""
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn đăng xuất?"):
            # Xóa AppWindow hiện tại
            self.destroy()
            
            # Quay lại màn hình login trong cùng cửa sổ
            self.parent._show_login_screen()
