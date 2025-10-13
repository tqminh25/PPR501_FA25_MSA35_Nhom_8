"""
Report View - Báo cáo thống kê
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List
from .base_view import BaseContentView


class ReportView(BaseContentView):
    """View cho báo cáo thống kê"""
    
    def __init__(self, parent_frame: ttk.Frame):
        # Khởi tạo dữ liệu trước khi gọi super().__init__()
        self.report_data = {}
        self._load_sample_data()
        
        super().__init__(parent_frame, "📋 Báo cáo thống kê")
    
    def _create_content(self):
        """Tạo nội dung báo cáo"""
        # Toolbar
        self._create_toolbar()
        
        # Report content
        self._create_report_content()
    
    def _create_toolbar(self):
        """Tạo toolbar"""
        toolbar_frame = ttk.Frame(self.content_frame, style="Content.TFrame")
        toolbar_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(0, 10))
        toolbar_frame.columnconfigure(1, weight=1)
        
        # Nút tạo báo cáo
        generate_btn = ttk.Button(toolbar_frame, text="📊 Tạo báo cáo", 
                                command=self._generate_report)
        generate_btn.grid(row=0, column=0, padx=(0, 10))
        
        # Nút xuất Excel
        export_btn = ttk.Button(toolbar_frame, text="📤 Xuất Excel", 
                              command=self._export_excel)
        export_btn.grid(row=0, column=1, padx=(0, 10))
        
        # Nút in báo cáo
        print_btn = ttk.Button(toolbar_frame, text="🖨️ In báo cáo", 
                             command=self._print_report)
        print_btn.grid(row=0, column=2, padx=(0, 10))
        
        # Filter options
        filter_frame = ttk.Frame(toolbar_frame, style="Content.TFrame")
        filter_frame.grid(row=0, column=3, sticky="e")
        
        ttk.Label(filter_frame, text="Lọc theo:", style="Content.TLabel").grid(row=0, column=0, padx=(0, 5))
        self.filter_var = tk.StringVar(value="Tất cả")
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_var, 
                                  values=["Tất cả", "Theo lớp", "Theo điểm"], 
                                  state="readonly", width=12)
        filter_combo.grid(row=0, column=1)
        filter_combo.bind('<<ComboboxSelected>>', self._on_filter_change)
    
    def _create_report_content(self):
        """Tạo nội dung báo cáo"""
        # Main content frame
        content_frame = ttk.Frame(self.content_frame, style="Content.TFrame")
        content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)
        content_frame.rowconfigure(0, weight=1)
        
        # Left panel - Statistics
        self._create_statistics_panel(content_frame)
        
        # Right panel - Charts/Details
        self._create_charts_panel(content_frame)
    
    def _create_statistics_panel(self, parent):
        """Tạo panel thống kê"""
        stats_frame = ttk.LabelFrame(parent, text="📈 Thống kê tổng quan", 
                                   style="Content.TFrame")
        stats_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=5)
        stats_frame.columnconfigure(0, weight=1)
        
        # Statistics cards
        self._create_stat_cards(stats_frame)
        
        # Detailed stats
        self._create_detailed_stats(stats_frame)
    
    def _create_stat_cards(self, parent):
        """Tạo các thẻ thống kê"""
        cards_frame = ttk.Frame(parent, style="Content.TFrame")
        cards_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        cards_frame.columnconfigure(0, weight=1)
        cards_frame.columnconfigure(1, weight=1)
        
        # Card 1 - Tổng số học sinh
        card1 = self._create_stat_card(cards_frame, "👥", "Tổng học sinh", 
                                     str(self.report_data.get('total_students', 0)), 
                                     "Học sinh", 0, 0)
        
        # Card 2 - Điểm trung bình
        card2 = self._create_stat_card(cards_frame, "📊", "Điểm TB", 
                                     f"{self.report_data.get('avg_score', 0):.1f}", 
                                     "Điểm", 0, 1)
        
        # Card 3 - Số lớp
        card3 = self._create_stat_card(cards_frame, "🏫", "Số lớp", 
                                     str(self.report_data.get('total_classes', 0)), 
                                     "Lớp", 1, 0)
        
        # Card 4 - Tỷ lệ đỗ
        card4 = self._create_stat_card(cards_frame, "✅", "Tỷ lệ đỗ", 
                                     f"{self.report_data.get('pass_rate', 0):.1f}%", 
                                     "Phần trăm", 1, 1)
    
    def _create_stat_card(self, parent, icon, title, value, unit, row, col):
        """Tạo một thẻ thống kê"""
        card = ttk.Frame(parent, style="Content.TFrame", relief="solid", borderwidth=1)
        card.grid(row=row, column=col, sticky="ew", padx=5, pady=5)
        card.columnconfigure(0, weight=1)
        
        # Icon và title
        header_frame = ttk.Frame(card, style="Content.TFrame")
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        
        icon_label = ttk.Label(header_frame, text=icon, font=("Helvetica", 16))
        icon_label.grid(row=0, column=0, padx=(0, 5))
        
        title_label = ttk.Label(header_frame, text=title, style="Content.TLabel")
        title_label.grid(row=0, column=1, sticky="w")
        
        # Value
        value_label = ttk.Label(card, text=value, font=("Helvetica", 24, "bold"), 
                              foreground="#2c3e50", style="Content.TLabel")
        value_label.grid(row=1, column=0, pady=5)
        
        # Unit
        unit_label = ttk.Label(card, text=unit, style="Content.TLabel")
        unit_label.grid(row=2, column=0, pady=(0, 10))
        
        return card
    
    def _create_detailed_stats(self, parent):
        """Tạo thống kê chi tiết"""
        details_frame = ttk.LabelFrame(parent, text="📋 Chi tiết", 
                                     style="Content.TFrame")
        details_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        details_frame.columnconfigure(0, weight=1)
        
        # Tạo text widget để hiển thị thống kê chi tiết
        self.details_text = tk.Text(details_frame, height=8, wrap=tk.WORD, 
                                  font=("Helvetica", 10))
        self.details_text.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(details_frame, orient="vertical", 
                                command=self.details_text.yview)
        self.details_text.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Load detailed stats
        self._load_detailed_stats()
    
    def _create_charts_panel(self, parent):
        """Tạo panel biểu đồ"""
        charts_frame = ttk.LabelFrame(parent, text="📊 Biểu đồ", 
                                    style="Content.TFrame")
        charts_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0), pady=5)
        charts_frame.columnconfigure(0, weight=1)
        charts_frame.rowconfigure(0, weight=1)
        
        # Placeholder cho biểu đồ
        chart_placeholder = ttk.Label(charts_frame, 
                                    text="📊\n\nBiểu đồ thống kê\n\n(Đang phát triển)", 
                                    font=("Helvetica", 14), style="Content.TLabel")
        chart_placeholder.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
    
    def _load_sample_data(self):
        """Load dữ liệu mẫu"""
        self.report_data = {
            'total_students': 150,
            'avg_score': 8.2,
            'total_classes': 6,
            'pass_rate': 85.5,
            'class_stats': {
                '10A1': {'students': 25, 'avg_score': 8.5},
                '10A2': {'students': 24, 'avg_score': 8.1},
                '11A1': {'students': 26, 'avg_score': 8.3},
                '11A2': {'students': 25, 'avg_score': 8.0},
                '12A1': {'students': 25, 'avg_score': 8.4},
                '12A2': {'students': 25, 'avg_score': 8.2},
            }
        }
    
    def _load_detailed_stats(self):
        """Load thống kê chi tiết"""
        details = f"""
THỐNG KÊ CHI TIẾT HỌC SINH

📊 Tổng quan:
• Tổng số học sinh: {self.report_data['total_students']} học sinh
• Điểm trung bình: {self.report_data['avg_score']}/10
• Số lớp học: {self.report_data['total_classes']} lớp
• Tỷ lệ đỗ: {self.report_data['pass_rate']}%

📈 Thống kê theo lớp:
"""
        
        for class_name, stats in self.report_data['class_stats'].items():
            details += f"• {class_name}: {stats['students']} học sinh, TB: {stats['avg_score']}/10\n"
        
        details += f"""
🎯 Phân loại học sinh:
• Giỏi (8.0-10.0): {int(self.report_data['total_students'] * 0.3)} học sinh
• Khá (6.5-7.9): {int(self.report_data['total_students'] * 0.4)} học sinh  
• Trung bình (5.0-6.4): {int(self.report_data['total_students'] * 0.25)} học sinh
• Yếu (<5.0): {int(self.report_data['total_students'] * 0.05)} học sinh
"""
        
        self.details_text.delete(1.0, tk.END)
        self.details_text.insert(1.0, details)
        self.details_text.config(state=tk.DISABLED)
    
    def _on_filter_change(self, event=None):
        """Xử lý khi thay đổi filter"""
        filter_value = self.filter_var.get()
        messagebox.showinfo("Thông báo", f"Đã chọn filter: {filter_value}")
    
    def _generate_report(self):
        """Tạo báo cáo mới"""
        messagebox.showinfo("Thông báo", "Đang tạo báo cáo...")
        self.refresh()
        messagebox.showinfo("Thành công", "Báo cáo đã được tạo thành công!")
    
    def _export_excel(self):
        """Xuất báo cáo ra Excel"""
        messagebox.showinfo("Thông báo", "Chức năng xuất Excel - Đang phát triển")
    
    def _print_report(self):
        """In báo cáo"""
        messagebox.showinfo("Thông báo", "Chức năng in báo cáo - Đang phát triển")
    
    def refresh(self):
        """Refresh view"""
        self._load_detailed_stats()
