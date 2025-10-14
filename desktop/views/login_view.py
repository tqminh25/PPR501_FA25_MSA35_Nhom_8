"""
Login View - UI cho màn hình đăng nhập
"""

import tkinter as tk
from tkinter import messagebox, ttk
from abc import ABC, abstractmethod
from typing import Tuple, TYPE_CHECKING

from config.styles import AppStyles
from utils.window_utils import WindowUtils

if TYPE_CHECKING:
    from presenters.login_presenter import LoginPresenter


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
    def show_success(self, username: str, remember: str):
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


class LoginView(tk.Tk, ILoginView):
    """View implementation cho Login UI"""
    
    def __init__(self, presenter: 'LoginPresenter' = None):
        super().__init__()
        self.presenter = presenter
        
        self.title("Đăng nhập - MVP Architecture")
        self._setup_window()
        self._initialize_style()
        self._build_ui()
    
    def _setup_window(self):
        """Thiết lập cửa sổ"""
        WindowUtils.setup_fullscreen(self, min_width=400, min_height=300)
    
    def _initialize_style(self):
        """Khởi tạo style cho UI"""
        self.style = AppStyles.initialize_login_styles()
    
    def _build_ui(self):
        """Xây dựng giao diện"""
        # Main container
        main_container = ttk.Frame(self)
        main_container.grid(row=0, column=0, sticky="nsew")
        main_container.configure(style="TFrame")
        
        # Cấu hình grid weights cho responsive
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        main_container.columnconfigure(0, weight=1)
        main_container.rowconfigure(0, weight=1)
        main_container.rowconfigure(1, weight=0)  # Form container không mở rộng

        # Form container - căn giữa hoàn hảo
        self.form_container = ttk.Frame(main_container)
        self.form_container.grid(row=0, column=0, sticky="")
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
        self.username_var = tk.StringVar(value="usertest")  # Giá trị mặc định
        self.username_entry = ttk.Entry(self.form_container, textvariable=self.username_var, width=30)
        username_label.grid(row=2, column=0, sticky="w")
        self.username_entry.grid(row=3, column=0, columnspan=3, sticky="ew", pady=(2, 12))

        # Password
        password_label = ttk.Label(self.form_container, text="Mật khẩu")
        self.password_var = tk.StringVar(value="123456")  # Giá trị mặc định
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

        # Focus và căn giữa form
        self.after(100, lambda: self.focus_force() or self.username_entry.focus_set())
        self.after(200, self._center_form)
        
        # Bind resize event để luôn căn giữa
        self.bind('<Configure>', lambda e: self._on_resize() if e.widget == self else None)
    
    def _center_form(self):
        """Căn giữa form một cách chính xác"""
        try:
            # Cập nhật geometry để đảm bảo form được căn giữa
            self.update_idletasks()
            
            # Lấy kích thước form
            form_width = self.form_container.winfo_reqwidth()
            form_height = self.form_container.winfo_reqheight()
            
            # Lấy kích thước window
            window_width = self.winfo_width()
            window_height = self.winfo_height()
            
            # Tính toán vị trí căn giữa
            x = (window_width - form_width) // 2
            y = (window_height - form_height) // 2
            
            # Cập nhật vị trí form container
            self.form_container.grid_configure(padx=x, pady=y)
            
        except tk.TclError:
            pass  # Window đã bị destroy
    
    def _on_resize(self):
        """Xử lý khi window resize"""
        self.after(100, self._center_form)
    
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
        if self.presenter:
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
    
    def show_success(self, username: str, remember: str):
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
    
    def _create_app_screen(self, username: str, remember: str):
        """Tạo màn hình App chính"""
        # Import here to avoid circular import
        from .app_view import AppWindow
        
        # Tạo App window mới
        app_window = AppWindow(self, username, remember)
        app_window.mainloop()
