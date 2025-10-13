import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sys
import time
from abc import ABC, abstractmethod
from typing import Tuple, Optional


# ==================== MODEL ====================
class LoginModel:
    """Model chứa business logic và API calls"""
    
    def __init__(self):
        self.api_base_url = "https://api.example.com"  # Giả lập API endpoint
    
    def authenticate(self, username: str, password: str) -> Tuple[bool, str]:
        """
        Giả lập API call để xác thực
        Returns: (success: bool, message: str)
        """
        # Giả lập network delay
        time.sleep(0.5)
        
        # API simulation: chỉ usertest/123455 thành công
        if username == "usertest" and password == "123456":
            return True, "Đăng nhập thành công"
        else:
            return False, "Tên đăng nhập hoặc mật khẩu không đúng"
    
    def validate_credentials(self, username: str, password: str) -> Tuple[bool, str]:
        """Validate input trước khi gọi API"""
        if not username.strip():
            return False, "Vui lòng nhập tên đăng nhập"
        if not password:
            return False, "Vui lòng nhập mật khẩu"
        if len(username) < 3:
            return False, "Tên đăng nhập phải có ít nhất 3 ký tự"
        if len(password) < 6:
            return False, "Mật khẩu phải có ít nhất 6 ký tự"
        return True, ""


# ==================== VIEW INTERFACE ====================
class ILoginView(ABC):
    """Interface cho Login View"""
    
    @abstractmethod
    def get_credentials(self) -> Tuple[str, str, bool]:
        """Lấy thông tin đăng nhập từ UI"""
        pass
    
    @abstractmethod
    def show_loading(self, loading: bool):
        """Hiển thị/ẩn loading state"""
        pass
    
    @abstractmethod
    def show_success(self, username: str, remember: bool):
        """Hiển thị màn hình thành công"""
        pass
    
    @abstractmethod
    def show_error(self, message: str):
        """Hiển thị lỗi"""
        pass
    
    @abstractmethod
    def clear_password(self):
        """Xóa password field"""
        pass


# ==================== VIEW IMPLEMENTATION ====================
class LoginView(tk.Tk, ILoginView):
    """View implementation cho Login UI"""
    
    def __init__(self, presenter):
        super().__init__()
        self.presenter = presenter
        
        self.title("Đăng nhập - MVP Architecture")
        self.configure(padx=24, pady=24)
        
        # Thiết lập full screen và responsive
        self._setup_window()
        self._initialize_style()
        self._build_ui()
    
    def _setup_window(self):
        """Thiết lập cửa sổ"""
        if sys.platform == "win32":
            self.state('zoomed')
        elif sys.platform == "darwin":
            self.update_idletasks()
            width = self.winfo_screenwidth()
            height = self.winfo_screenheight()
            self.geometry(f"{width}x{height}+0+0")
        else:
            self.state('zoomed')
        
        self.minsize(400, 300)
        self.resizable(True, True)
        self.configure(bg='white')
    
    def _initialize_style(self):
        """Khởi tạo style cho UI"""
        style = ttk.Style()
        preferred_theme_order = ("aqua", "vista", "clam", "default")
        for theme in preferred_theme_order:
            try:
                style.theme_use(theme)
                break
            except tk.TclError:
                continue

        style.configure("TLabel", font=("Helvetica", 12), background="white")
        style.configure("Title.TLabel", font=("Helvetica", 16, "bold"), background="white")
        style.configure("TButton", font=("Helvetica", 12))
        style.configure("TCheckbutton", font=("Helvetica", 11), background="white")
        style.configure("TEntry", padding=4)
        style.configure("TFrame", background="white")
        style.configure("Loading.TButton", foreground="gray")
    
    def _build_ui(self):
        """Xây dựng giao diện"""
        # Main container
        main_container = ttk.Frame(self)
        main_container.grid(row=0, column=0, sticky="nsew", padx=50, pady=50)
        main_container.configure(style="TFrame")
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        main_container.columnconfigure(0, weight=1)
        main_container.rowconfigure(1, weight=1)

        # Form container
        self.form_container = ttk.Frame(main_container)
        self.form_container.grid(row=1, column=0, sticky="")
        self.form_container.columnconfigure(0, weight=1)
        self.form_container.columnconfigure(1, weight=1)
        self.form_container.columnconfigure(2, weight=1)
        self.form_container.configure(style="TFrame")

        # Title
        title_label = ttk.Label(self.form_container, text="Chào mừng trở lại", style="Title.TLabel")
        subtitle_label = ttk.Label(self.form_container, text="Vui lòng đăng nhập để tiếp tục")
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 4))
        subtitle_label.grid(row=1, column=0, columnspan=3, pady=(0, 16))

        # Username
        username_label = ttk.Label(self.form_container, text="Tên đăng nhập")
        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(self.form_container, textvariable=self.username_var, width=30)
        username_label.grid(row=2, column=0, sticky="w")
        self.username_entry.grid(row=3, column=0, columnspan=3, sticky="ew", pady=(2, 12))

        # Password
        password_label = ttk.Label(self.form_container, text="Mật khẩu")
        self.password_var = tk.StringVar()
        self._password_hidden = True
        self.password_entry = ttk.Entry(self.form_container, textvariable=self.password_var, show="•", width=30)
        password_label.grid(row=4, column=0, sticky="w")
        self.password_entry.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(2, 0))

        # Show/Hide password button
        self.toggle_btn_text = tk.StringVar(value="Hiện")
        self.toggle_btn = ttk.Button(self.form_container, textvariable=self.toggle_btn_text, width=8, command=self._toggle_password)
        self.toggle_btn.grid(row=5, column=2, sticky="e", padx=(8, 0))

        # Remember me checkbox
        self.remember_var = tk.BooleanVar(value=False)
        self.remember_check = ttk.Checkbutton(self.form_container, text="Ghi nhớ tôi", variable=self.remember_var)
        self.remember_check.grid(row=6, column=0, columnspan=2, sticky="w", pady=(8, 0))

        # Buttons
        button_row = ttk.Frame(self.form_container)
        button_row.grid(row=7, column=0, columnspan=3, sticky="ew", pady=(16, 0))
        button_row.columnconfigure(0, weight=1)
        button_row.columnconfigure(1, weight=0)
        button_row.columnconfigure(2, weight=0)
        button_row.configure(style="TFrame")

        self.quit_btn = ttk.Button(button_row, text="Thoát", command=self.destroy)
        self.login_btn = ttk.Button(button_row, text="Đăng nhập", command=self._on_login_clicked)
        self.quit_btn.grid(row=0, column=1, padx=(0, 8))
        self.login_btn.grid(row=0, column=2)

        # Loading label (ẩn ban đầu)
        self.loading_label = ttk.Label(self.form_container, text="Đang xử lý...", foreground="blue")
        self.loading_label.grid(row=8, column=0, columnspan=3, pady=(8, 0))
        self.loading_label.grid_remove()  # Ẩn ban đầu

        # Keyboard bindings
        self.bind("<Return>", lambda _e: self._on_login_clicked())
        self.bind("<Escape>", lambda _e: self.destroy())

        # Focus
        self.after(100, lambda: self.focus_force() or self.username_entry.focus_set())
    
    def _toggle_password(self):
        """Toggle hiển thị password"""
        self._password_hidden = not self._password_hidden
        if self._password_hidden:
            self.password_entry.configure(show="•")
            self.toggle_btn_text.set("Hiện")
        else:
            self.password_entry.configure(show="")
            self.toggle_btn_text.set("Ẩn")
    
    def _on_login_clicked(self):
        """Event handler cho nút đăng nhập"""
        self.presenter.on_login_clicked()
    
    # ==================== VIEW INTERFACE IMPLEMENTATION ====================
    
    def get_credentials(self) -> Tuple[str, str, bool]:
        """Lấy thông tin đăng nhập từ UI"""
        username = self.username_var.get().strip()
        password = self.password_var.get()
        remember = self.remember_var.get()
        return username, password, remember
    
    def show_loading(self, loading: bool):
        """Hiển thị/ẩn loading state"""
        if loading:
            self.loading_label.grid()
            self.login_btn.configure(text="Đang xử lý...", state="disabled")
            self.quit_btn.configure(state="disabled")
        else:
            self.loading_label.grid_remove()
            self.login_btn.configure(text="Đăng nhập", state="normal")
            self.quit_btn.configure(state="normal")
    
    def show_success(self, username: str, remember: bool):
        """Hiển thị màn hình App chính"""
        # Xóa form hiện tại
        for child in list(self.children.values()):
            try:
                child.destroy()
            except Exception:
                pass

        # Tạo App screen
        self._create_app_screen(username, remember)
    
    def show_error(self, message: str):
        """Hiển thị lỗi"""
        messagebox.showerror("Lỗi đăng nhập", message)
        self.clear_password()
    
    def clear_password(self):
        """Xóa password field"""
        self.password_var.set("")
    
    def _create_app_screen(self, username: str, remember: bool):
        """Tạo màn hình App chính"""
        # Tạo App window mới
        app_window = AppWindow(self, username, remember)
        app_window.mainloop()


# ==================== APP WINDOW ====================
class AppWindow(tk.Tk):
    """Màn hình App chính sau khi login"""
    
    def __init__(self, parent, username: str, remember: bool):
        super().__init__()
        self.parent = parent
        self.username = username
        self.remember = remember
        self.current_page = "dashboard"
        
        self.title(f"EduManager Pro - Xin chào {username}")
        self._setup_window()
        self._initialize_style()
        self._create_layout()
    
    def _setup_window(self):
        """Thiết lập cửa sổ App"""
        if sys.platform == "win32":
            self.state('zoomed')
        elif sys.platform == "darwin":
            self.update_idletasks()
            width = self.winfo_screenwidth()
            height = self.winfo_screenheight()
            self.geometry(f"{width}x{height}+0+0")
        else:
            self.state('zoomed')
        
        self.minsize(800, 600)
        self.resizable(True, True)
        self.configure(bg='white')
    
    def _initialize_style(self):
        """Khởi tạo style cho App"""
        style = ttk.Style()
        preferred_theme_order = ("aqua", "vista", "clam", "default")
        for theme in preferred_theme_order:
            try:
                style.theme_use(theme)
                break
            except tk.TclError:
                continue
        
        # App styles
        style.configure("Header.TFrame", background="white")
        style.configure("Header.TLabel", background="white", foreground="#2c3e50", font=("Helvetica", 14, "bold"))
        style.configure("Sidebar.TFrame", background="white", relief="flat")
        style.configure("Sidebar.TLabel", background="white", foreground="#2c3e50", font=("Helvetica", 12))
        style.configure("Sidebar.TButton", background="white", foreground="#2c3e50", font=("Helvetica", 11), borderwidth=1)
        style.map("Sidebar.TButton", background=[('active', '#f0f0f0'), ('pressed', '#e0e0e0')])
        style.configure("Content.TFrame", background="white", relief="flat")
        style.configure("Content.TLabel", background="white", foreground="#2c3e50", font=("Helvetica", 16))
        style.configure("Logout.TButton", background="#e74c3c", foreground="white", font=("Helvetica", 10))
        style.map("Logout.TButton", background=[('active', '#c0392b'), ('pressed', '#a93226')])
    
    def _create_layout(self):
        """Tạo bố cục chính"""
        # Main container
        main_container = ttk.Frame(self)
        main_container.grid(row=0, column=0, sticky="nsew")
        main_container.configure(style="TFrame")
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        main_container.columnconfigure(1, weight=1)
        main_container.rowconfigure(1, weight=1)
        
        # Header
        self._create_header(main_container)
        
        # Sidebar
        self._create_sidebar(main_container)
        
        # Content area
        self._create_content_area(main_container)
    
    def _create_header(self, parent):
        """Tạo header bar"""
        header_frame = ttk.Frame(parent, style="Header.TFrame")
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=0, pady=0)
        header_frame.columnconfigure(1, weight=1)
        
        # Logo và tên app
        logo_label = ttk.Label(header_frame, text="🎓 EduManager Pro", style="Header.TLabel")
        logo_label.grid(row=0, column=0, padx=20, pady=15, sticky="w")
        
        # Thông tin user và logout
        user_frame = ttk.Frame(header_frame, style="Header.TFrame")
        user_frame.grid(row=0, column=1, padx=20, pady=15, sticky="e")
        
        user_label = ttk.Label(user_frame, text=f"👤 {self.username}", style="Header.TLabel")
        user_label.grid(row=0, column=0, padx=(0, 10))
        
        logout_btn = ttk.Button(user_frame, text="Đăng xuất", style="Logout.TButton", command=self._logout)
        logout_btn.grid(row=0, column=1)
    
    def _create_sidebar(self, parent):
        """Tạo menu trái"""
        sidebar_frame = ttk.Frame(parent, style="Sidebar.TFrame")
        sidebar_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        sidebar_frame.columnconfigure(0, weight=1)
        
        # Menu items
        menu_items = [
            ("📊", "Dashboard", "dashboard"),
            ("👥", "Quản lý học sinh", "students"),
            ("📝", "Quản lý điểm", "grades"),
            ("📚", "Quản lý lớp học", "classes"),
            ("📋", "Báo cáo", "reports"),
            ("⚙️", "Cài đặt", "settings"),
        ]
        
        # Tạo menu buttons
        for i, (icon, text, page) in enumerate(menu_items):
            btn = ttk.Button(sidebar_frame, text=f"{icon} {text}", style="Sidebar.TButton", 
                           command=lambda p=page: self._navigate_to_page(p))
            btn.grid(row=i, column=0, sticky="ew", padx=10, pady=5)
        
        # Thông tin user ở cuối sidebar
        user_info_frame = ttk.Frame(sidebar_frame, style="Sidebar.TFrame")
        user_info_frame.grid(row=len(menu_items) + 1, column=0, sticky="ew", padx=10, pady=20)
        user_info_frame.columnconfigure(0, weight=1)
        
        user_info_label = ttk.Label(user_info_frame, text=f"👤 {self.username}", style="Sidebar.TLabel")
        user_info_label.grid(row=0, column=0, pady=5)
        
        if self.remember:
            remember_label = ttk.Label(user_info_frame, text="💾 Đã ghi nhớ", style="Sidebar.TLabel")
            remember_label.grid(row=1, column=0, pady=2)
    
    def _create_content_area(self, parent):
        """Tạo vùng content chính"""
        self.content_frame = ttk.Frame(parent, style="Content.TFrame")
        self.content_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(0, weight=1)
        
        # Hiển thị trang mặc định
        self._show_dashboard()
    
    def _navigate_to_page(self, page: str):
        """Điều hướng đến trang"""
        self.current_page = page
        
        # Xóa content hiện tại
        for child in self.content_frame.winfo_children():
            child.destroy()
        
        # Hiển thị trang mới
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
        elif page == "settings":
            self._show_settings()
    
    def _show_dashboard(self):
        """Hiển thị trang Dashboard"""
        title_label = ttk.Label(self.content_frame, text="📊 Dashboard", style="Content.TLabel")
        title_label.grid(row=0, column=0, pady=20, sticky="w")
        
        welcome_label = ttk.Label(self.content_frame, text=f"Chào mừng {self.username} đến với EduManager Pro!", 
                                 font=("Helvetica", 14), background="white")
        welcome_label.grid(row=1, column=0, pady=10, sticky="w")
        
        info_label = ttk.Label(self.content_frame, text="Sử dụng menu bên trái để điều hướng đến các chức năng khác nhau.", 
                              font=("Helvetica", 12), background="white", foreground="#7f8c8d")
        info_label.grid(row=2, column=0, pady=5, sticky="w")
    
    def _show_students(self):
        """Hiển thị trang Quản lý học sinh"""
        title_label = ttk.Label(self.content_frame, text="👥 Quản lý học sinh", style="Content.TLabel")
        title_label.grid(row=0, column=0, pady=20, sticky="w")
        
        content_label = ttk.Label(self.content_frame, text="Trang quản lý học sinh - Đang phát triển", 
                                 font=("Helvetica", 14), background="white")
        content_label.grid(row=1, column=0, pady=10, sticky="w")
    
    def _show_grades(self):
        """Hiển thị trang Quản lý điểm"""
        title_label = ttk.Label(self.content_frame, text="📝 Quản lý điểm", style="Content.TLabel")
        title_label.grid(row=0, column=0, pady=20, sticky="w")
        
        content_label = ttk.Label(self.content_frame, text="Trang quản lý điểm - Đang phát triển", 
                                 font=("Helvetica", 14), background="white")
        content_label.grid(row=1, column=0, pady=10, sticky="w")
    
    def _show_classes(self):
        """Hiển thị trang Quản lý lớp học"""
        title_label = ttk.Label(self.content_frame, text="📚 Quản lý lớp học", style="Content.TLabel")
        title_label.grid(row=0, column=0, pady=20, sticky="w")
        
        content_label = ttk.Label(self.content_frame, text="Trang quản lý lớp học - Đang phát triển", 
                                 font=("Helvetica", 14), background="white")
        content_label.grid(row=1, column=0, pady=10, sticky="w")
    
    def _show_reports(self):
        """Hiển thị trang Báo cáo"""
        title_label = ttk.Label(self.content_frame, text="📋 Báo cáo", style="Content.TLabel")
        title_label.grid(row=0, column=0, pady=20, sticky="w")
        
        content_label = ttk.Label(self.content_frame, text="Trang báo cáo - Đang phát triển", 
                                 font=("Helvetica", 14), background="white")
        content_label.grid(row=1, column=0, pady=10, sticky="w")
    
    def _show_settings(self):
        """Hiển thị trang Cài đặt"""
        title_label = ttk.Label(self.content_frame, text="⚙️ Cài đặt", style="Content.TLabel")
        title_label.grid(row=0, column=0, pady=20, sticky="w")
        
        content_label = ttk.Label(self.content_frame, text="Trang cài đặt - Đang phát triển", 
                                 font=("Helvetica", 14), background="white")
        content_label.grid(row=1, column=0, pady=10, sticky="w")
    
    def _logout(self):
        """Đăng xuất"""
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn đăng xuất?"):
            self.destroy()
            # Quay lại màn hình login
            login_view = LoginView(None)
            model = LoginModel()
            presenter = LoginPresenter(login_view, model)
            login_view.presenter = presenter
            login_view.mainloop()


# ==================== PRESENTER ====================
class LoginPresenter:
    """Presenter điều khiển logic giữa View và Model"""
    
    def __init__(self, view: ILoginView, model: LoginModel):
        self.view = view
        self.model = model
    
    def on_login_clicked(self):
        """Xử lý sự kiện đăng nhập"""
        # Lấy thông tin từ view
        username, password, remember = self.view.get_credentials()
        
        # Validate input
        is_valid, error_message = self.model.validate_credentials(username, password)
        if not is_valid:
            self.view.show_error(error_message)
            return
        
        # Hiển thị loading
        self.view.show_loading(True)
        
        # Gọi API (giả lập async)
        self._authenticate_async(username, password, remember)
    
    def _authenticate_async(self, username: str, password: str, remember: bool):
        """Giả lập async API call"""
        # Trong thực tế, đây sẽ là async call
        def authenticate():
            success, message = self.model.authenticate(username, password)
            
            # Update UI trong main thread
            self.view.after(0, lambda: self._handle_auth_result(success, message, username, remember))
        
        # Chạy trong background thread (giả lập)
        import threading
        thread = threading.Thread(target=authenticate)
        thread.daemon = True
        thread.start()
    
    def _handle_auth_result(self, success: bool, message: str, username: str, remember: bool):
        """Xử lý kết quả authentication"""
        self.view.show_loading(False)
        
        if success:
            self.view.show_success(username, remember)
        else:
            self.view.show_error(message)


# ==================== MAIN APPLICATION ====================
def main():
    """Main function sử dụng MVP pattern"""
    # Tạo Model
    model = LoginModel()
    
    # Tạo View và Presenter
    view = LoginView(None)  # Presenter sẽ được set sau
    presenter = LoginPresenter(view, model)
    view.presenter = presenter  # Set presenter cho view
    
    # Chạy ứng dụng
    view.mainloop()


if __name__ == "__main__":
    main()