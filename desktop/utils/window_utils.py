"""
Window utility functions
"""

import sys
import tkinter as tk


class WindowUtils:
    """Utility class cho window operations"""
    
    @staticmethod
    def setup_fullscreen(window, min_width=400, min_height=300):
        """Thiết lập fullscreen cho window"""
        if sys.platform == "win32":
            window.state('zoomed')
        elif sys.platform == "darwin":
            window.update_idletasks()
            width = window.winfo_screenwidth()
            height = window.winfo_screenheight()
            window.geometry(f"{width}x{height}+0+0")
        else:
            window.state('zoomed')
        
        window.minsize(min_width, min_height)
        window.resizable(True, True)
        window.configure(bg='white')
    
    @staticmethod
    def center_window(window, width, height):
        """Căn giữa window trên màn hình"""
        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    @staticmethod
    def setup_grid_weights(window, rows=1, cols=1):
        """Thiết lập grid weights cho responsive layout"""
        for i in range(rows):
            window.rowconfigure(i, weight=1)
        for i in range(cols):
            window.columnconfigure(i, weight=1)
    
    @staticmethod
    def setup_responsive_layout(window, sidebar_width_percent=0.3):
        """Thiết lập responsive layout với sidebar chiếm phần trăm nhất định"""
        window.update_idletasks()
        window_width = window.winfo_width()
        sidebar_width = int(window_width * sidebar_width_percent)
        
        # Cấu hình grid weights
        window.columnconfigure(0, weight=0, minsize=sidebar_width)  # Sidebar
        window.columnconfigure(1, weight=1)  # Content area
        window.rowconfigure(0, weight=0)  # Header
        window.rowconfigure(1, weight=1)  # Main content
    
    @staticmethod
    def bind_resize_event(window, callback):
        """Bind resize event để cập nhật layout khi thay đổi kích thước"""
        window.bind('<Configure>', lambda e: callback() if e.widget == window else None)
