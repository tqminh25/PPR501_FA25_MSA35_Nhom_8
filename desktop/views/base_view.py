"""
Base View class - Class cơ sở cho tất cả các view
"""

import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod
from typing import Optional


class BaseView(ABC):
    """Base class cho tất cả các view"""
    
    def __init__(self, parent_frame: ttk.Frame, title: str = ""):
        self.parent_frame = parent_frame
        self.title = title
        self.main_frame = None
        self._create_view()
    
    @abstractmethod
    def _create_view(self):
        """Tạo giao diện cho view - phải được implement bởi subclass"""
        pass
    
    def show(self):
        """Hiển thị view"""
        if self.main_frame:
            try:
                self.main_frame.grid()
            except tk.TclError:
                # Nếu widget đã bị destroy, tạo lại
                pass
    
    def hide(self):
        """Ẩn view"""
        if self.main_frame:
            try:
                self.main_frame.grid_remove()
            except tk.TclError:
                # Nếu widget đã bị destroy, bỏ qua
                pass
    
    def destroy(self):
        """Hủy view"""
        if self.main_frame:
            self.main_frame.destroy()
    
    def get_title(self) -> str:
        """Lấy title của view"""
        return self.title
    
    def refresh(self):
        """Refresh view - có thể override bởi subclass"""
        pass


class BaseContentView(BaseView):
    """Base class cho các content view trong App"""
    
    def __init__(self, parent_frame: ttk.Frame, title: str = ""):
        super().__init__(parent_frame, title)
    
    def _create_view(self):
        """Tạo base content view"""
        # Main frame
        self.main_frame = ttk.Frame(self.parent_frame, style="Content.TFrame")
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        
        # Title frame
        self.title_frame = ttk.Frame(self.main_frame, style="Content.TFrame")
        self.title_frame.grid(row=0, column=0, sticky="ew", pady=(5, 0))
        self.title_frame.columnconfigure(0, weight=1)
        
        # Title label
        self.title_label = ttk.Label(self.title_frame, text=self.title, 
                                   style="Content.TLabel")
        self.title_label.grid(row=0, column=0, sticky="w")
        
        # Content frame - để subclass override
        self.content_frame = ttk.Frame(self.main_frame, style="Content.TFrame")
        self.content_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 0))
        self.content_frame.columnconfigure(0, weight=1)
        # Cho phép tất cả các row expand
        for i in range(10):  # Hỗ trợ tối đa 10 rows
            self.content_frame.rowconfigure(i, weight=1)
        
        # Tạo nội dung cụ thể
        self._create_content()
    
    @abstractmethod
    def _create_content(self):
        """Tạo nội dung cụ thể - phải được implement bởi subclass"""
        pass
