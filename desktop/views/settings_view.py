"""
Settings View - Cài đặt hệ thống
"""

import tkinter as tk
from tkinter import ttk, messagebox
from .base_view import BaseContentView
from config.constants import COLORS


class SettingsView(BaseContentView):
    """View cho cài đặt hệ thống"""
    
    def __init__(self, parent_frame: ttk.Frame):
        # Khởi tạo dữ liệu trước khi gọi super().__init__()
        self.settings_data = {}
        self._load_sample_data()
        
        super().__init__(parent_frame, "⚙️ Cài đặt hệ thống")
        self._setup_white_background()
    
    def _create_content(self):
        """Tạo nội dung cài đặt"""
        # General settings
        self._create_general_settings()
        
        # User settings
        self._create_user_settings()
        
        # System settings
        self._create_system_settings()
        
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
        """Load dữ liệu mẫu cho cài đặt"""
        self.settings_data = {
            'language': 'Tiếng Việt',
            'theme': 'Light',
            'auto_save': True,
            'notifications': True,
            'backup_enabled': True,
            'backup_frequency': 'Daily',
            'max_file_size': '10MB',
            'session_timeout': 30
        }
    
    def _create_general_settings(self):
        """Tạo phần cài đặt chung"""
        general_frame = ttk.LabelFrame(self.content_frame, text="Cài đặt chung", 
                                     style="White.TFrame", padding=10)
        general_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        general_frame.columnconfigure(1, weight=1)
        
        # Ngôn ngữ
        ttk.Label(general_frame, text="Ngôn ngữ:", style="White.TLabel").grid(row=0, column=0, sticky="w", pady=5)
        self.language_var = tk.StringVar(value=self.settings_data['language'])
        language_combo = ttk.Combobox(general_frame, textvariable=self.language_var, width=20)
        language_combo['values'] = ("Tiếng Việt", "English", "中文")
        language_combo.grid(row=0, column=1, sticky="w", padx=(10, 0), pady=5)
        
        # Theme
        ttk.Label(general_frame, text="Giao diện:", style="White.TLabel").grid(row=1, column=0, sticky="w", pady=5)
        self.theme_var = tk.StringVar(value=self.settings_data['theme'])
        theme_combo = ttk.Combobox(general_frame, textvariable=self.theme_var, width=20)
        theme_combo['values'] = ("Light", "Dark", "Auto")
        theme_combo.grid(row=1, column=1, sticky="w", padx=(10, 0), pady=5)
        
        # Auto save
        self.auto_save_var = tk.BooleanVar(value=self.settings_data['auto_save'])
        auto_save_check = ttk.Checkbutton(general_frame, text="Tự động lưu", 
                                        variable=self.auto_save_var, style="White.TCheckbutton")
        auto_save_check.grid(row=2, column=0, columnspan=2, sticky="w", pady=5)
        
        # Notifications
        self.notifications_var = tk.BooleanVar(value=self.settings_data['notifications'])
        notifications_check = ttk.Checkbutton(general_frame, text="Thông báo", 
                                           variable=self.notifications_var, style="White.TCheckbutton")
        notifications_check.grid(row=3, column=0, columnspan=2, sticky="w", pady=5)
    
    def _create_user_settings(self):
        """Tạo phần cài đặt người dùng"""
        user_frame = ttk.LabelFrame(self.content_frame, text="Cài đặt người dùng", 
                                  style="White.TFrame", padding=10)
        user_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        user_frame.columnconfigure(1, weight=1)
        
        # Thông tin cá nhân
        ttk.Label(user_frame, text="Tên hiển thị:", style="White.TLabel").grid(row=0, column=0, sticky="w", pady=5)
        self.display_name_var = tk.StringVar(value="Administrator")
        display_name_entry = ttk.Entry(user_frame, textvariable=self.display_name_var, width=30)
        display_name_entry.grid(row=0, column=1, sticky="w", padx=(10, 0), pady=5)
        
        ttk.Label(user_frame, text="Email:", style="White.TLabel").grid(row=1, column=0, sticky="w", pady=5)
        self.email_var = tk.StringVar(value="admin@school.edu.vn")
        email_entry = ttk.Entry(user_frame, textvariable=self.email_var, width=30)
        email_entry.grid(row=1, column=1, sticky="w", padx=(10, 0), pady=5)
        
        ttk.Label(user_frame, text="Số điện thoại:", style="White.TLabel").grid(row=2, column=0, sticky="w", pady=5)
        self.phone_var = tk.StringVar(value="0123456789")
        phone_entry = ttk.Entry(user_frame, textvariable=self.phone_var, width=30)
        phone_entry.grid(row=2, column=1, sticky="w", padx=(10, 0), pady=5)
        
        # Nút đổi mật khẩu
        change_password_btn = ttk.Button(user_frame, text="Đổi mật khẩu", 
                                       command=self._change_password)
        change_password_btn.grid(row=3, column=0, columnspan=2, pady=10)
    
    def _create_system_settings(self):
        """Tạo phần cài đặt hệ thống"""
        system_frame = ttk.LabelFrame(self.content_frame, text="Cài đặt hệ thống", 
                                    style="White.TFrame", padding=10)
        system_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        system_frame.columnconfigure(1, weight=1)
        
        # Backup settings
        self.backup_enabled_var = tk.BooleanVar(value=self.settings_data['backup_enabled'])
        backup_check = ttk.Checkbutton(system_frame, text="Bật sao lưu tự động", 
                                     variable=self.backup_enabled_var, style="White.TCheckbutton")
        backup_check.grid(row=0, column=0, columnspan=2, sticky="w", pady=5)
        
        ttk.Label(system_frame, text="Tần suất sao lưu:", style="White.TLabel").grid(row=1, column=0, sticky="w", pady=5)
        self.backup_freq_var = tk.StringVar(value=self.settings_data['backup_frequency'])
        backup_freq_combo = ttk.Combobox(system_frame, textvariable=self.backup_freq_var, width=20)
        backup_freq_combo['values'] = ("Daily", "Weekly", "Monthly")
        backup_freq_combo.grid(row=1, column=1, sticky="w", padx=(10, 0), pady=5)
        
        # File size limit
        ttk.Label(system_frame, text="Kích thước file tối đa:", style="White.TLabel").grid(row=2, column=0, sticky="w", pady=5)
        self.max_file_size_var = tk.StringVar(value=self.settings_data['max_file_size'])
        file_size_combo = ttk.Combobox(system_frame, textvariable=self.max_file_size_var, width=20)
        file_size_combo['values'] = ("5MB", "10MB", "25MB", "50MB", "100MB")
        file_size_combo.grid(row=2, column=1, sticky="w", padx=(10, 0), pady=5)
        
        # Session timeout
        ttk.Label(system_frame, text="Thời gian timeout (phút):", style="White.TLabel").grid(row=3, column=0, sticky="w", pady=5)
        self.timeout_var = tk.IntVar(value=self.settings_data['session_timeout'])
        timeout_spinbox = ttk.Spinbox(system_frame, from_=5, to=120, textvariable=self.timeout_var, width=20)
        timeout_spinbox.grid(row=3, column=1, sticky="w", padx=(10, 0), pady=5)
        
        # Action buttons
        button_frame = ttk.Frame(system_frame, style="White.TFrame")
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        save_btn = ttk.Button(button_frame, text="💾 Lưu cài đặt", 
                            command=self._save_settings)
        save_btn.grid(row=0, column=0, padx=(0, 10))
        
        reset_btn = ttk.Button(button_frame, text="🔄 Đặt lại mặc định", 
                             command=self._reset_settings)
        reset_btn.grid(row=0, column=1, padx=(0, 10))
        
        export_btn = ttk.Button(button_frame, text="📤 Xuất cài đặt", 
                              command=self._export_settings)
        export_btn.grid(row=0, column=2)
    
    def _change_password(self):
        """Đổi mật khẩu"""
        messagebox.showinfo("Thông báo", "Chức năng đổi mật khẩu - Đang phát triển")
    
    def _save_settings(self):
        """Lưu cài đặt"""
        # Cập nhật dữ liệu
        self.settings_data.update({
            'language': self.language_var.get(),
            'theme': self.theme_var.get(),
            'auto_save': self.auto_save_var.get(),
            'notifications': self.notifications_var.get(),
            'backup_enabled': self.backup_enabled_var.get(),
            'backup_frequency': self.backup_freq_var.get(),
            'max_file_size': self.max_file_size_var.get(),
            'session_timeout': self.timeout_var.get()
        })
        
        messagebox.showinfo("Thành công", "Đã lưu cài đặt thành công!")
    
    def _reset_settings(self):
        """Đặt lại cài đặt mặc định"""
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn đặt lại cài đặt mặc định?"):
            self._load_sample_data()
            # Cập nhật UI
            self.language_var.set(self.settings_data['language'])
            self.theme_var.set(self.settings_data['theme'])
            self.auto_save_var.set(self.settings_data['auto_save'])
            self.notifications_var.set(self.settings_data['notifications'])
            self.backup_enabled_var.set(self.settings_data['backup_enabled'])
            self.backup_freq_var.set(self.settings_data['backup_frequency'])
            self.max_file_size_var.set(self.settings_data['max_file_size'])
            self.timeout_var.set(self.settings_data['session_timeout'])
            
            messagebox.showinfo("Thành công", "Đã đặt lại cài đặt mặc định!")
    
    def _export_settings(self):
        """Xuất cài đặt"""
        messagebox.showinfo("Thông báo", "Chức năng xuất cài đặt - Đang phát triển")
    
    def refresh(self):
        """Refresh view"""
        self._load_sample_data()
        # Có thể thêm logic refresh UI ở đây



