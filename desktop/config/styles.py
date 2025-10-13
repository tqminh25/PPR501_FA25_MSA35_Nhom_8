"""
Style configuration cho ứng dụng
"""

import tkinter as tk
from tkinter import ttk
from .constants import COLORS, FONTS


class AppStyles:
    """Quản lý styles cho toàn bộ ứng dụng"""
    
    @staticmethod
    def initialize_login_styles():
        """Khởi tạo styles cho login screen"""
        style = ttk.Style()
        
        # Theme selection
        preferred_theme_order = ("aqua", "vista", "clam", "default")
        for theme in preferred_theme_order:
            try:
                style.theme_use(theme)
                break
            except tk.TclError:
                continue

        # Login styles
        style.configure("TLabel", font=FONTS['default'], background=COLORS['background'])
        style.configure("Title.TLabel", font=FONTS['title'], background=COLORS['background'])
        style.configure("TButton", font=FONTS['default'])
        style.configure("TCheckbutton", font=FONTS['default'], background=COLORS['background'])
        style.configure("TEntry", padding=4)
        style.configure("TFrame", background=COLORS['background'])
        style.configure("Loading.TButton", foreground="gray")
        
        return style
    
    @staticmethod
    def initialize_app_styles():
        """Khởi tạo styles cho app screen"""
        style = ttk.Style()
        
        # Theme selection
        preferred_theme_order = ("aqua", "vista", "clam", "default")
        for theme in preferred_theme_order:
            try:
                style.theme_use(theme)
                break
            except tk.TclError:
                continue

        # App styles
        style.configure("Header.TFrame", background=COLORS['background'], relief="flat")
        style.configure("Header.TLabel", background=COLORS['background'], 
                       foreground=COLORS['text_primary'], font=FONTS['header'])
        style.configure("Sidebar.TFrame", background=COLORS['background'], relief="flat")
        style.configure("Sidebar.TLabel", background=COLORS['background'], 
                       foreground=COLORS['text_primary'], font=FONTS['default'])
        style.configure("Sidebar.TButton", background=COLORS['background'], 
                       foreground=COLORS['text_primary'], font=FONTS['menu'], 
                       borderwidth=1, padding=(10, 8))
        style.map("Sidebar.TButton", background=[('active', '#f0f0f0'), ('pressed', '#e0e0e0')])
        style.configure("Content.TFrame", background=COLORS['background'], relief="flat")
        style.configure("Content.TLabel", background=COLORS['background'], 
                       foreground=COLORS['text_primary'], font=FONTS['content'])
        style.configure("White.TFrame", background="white", relief="flat")
        style.configure("White.TLabel", background="white", 
                       foreground=COLORS['text_primary'], font=FONTS['content'])
        style.configure("Logout.TButton", background=COLORS['error'], 
                       foreground="white", font=FONTS['menu'], padding=(8, 4))
        style.map("Logout.TButton", background=[('active', '#c0392b'), ('pressed', '#a93226')])
        
        # Toggle button styles
        style.configure("Toggle.TButton", background=COLORS['primary'], 
                       foreground="white", font=FONTS['menu'], padding=(8, 8))
        style.map("Toggle.TButton", background=[('active', COLORS['primary_hover']), ('pressed', '#3730a3')])
        
        # Collapsed sidebar styles
        style.configure("CollapsedSidebar.TFrame", background=COLORS['background'], relief="flat")
        style.configure("CollapsedSidebar.TButton", background=COLORS['background'], 
                       foreground=COLORS['text_primary'], font=FONTS['menu'], 
                       borderwidth=1, padding=(8, 12))
        style.map("CollapsedSidebar.TButton", background=[('active', '#f0f0f0'), ('pressed', '#e0e0e0')])
        
        return style
