"""
Report View - Báo cáo thống kê
"""

import tkinter as tk
from tkinter import ttk, messagebox
from .base_view import BaseContentView
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from models.api_client import get_students, get_statistics


class ReportView(BaseContentView):
    """View cho báo cáo thống kê"""
    
    def __init__(self, parent_frame: ttk.Frame):
        # Khởi tạo dữ liệu trước khi gọi super().__init__()
        self.report_data = {}
        self.students_data = []
        self.filter_var = None
        self.details_text = None
        self._load_data_from_api()
        
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
    
    def _create_statistics_panel(self, parent):
        """Tạo panel thống kê"""
        stats_frame = ttk.LabelFrame(parent, text="📈 Thống kê tổng quan", 
                                   style="Content.TFrame")
        stats_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=5)
        stats_frame.columnconfigure(0, weight=1)
        
        # Statistics cards
        self._create_stat_cards(stats_frame)
    
    def _create_stat_cards(self, parent):
        """Tạo các thẻ thống kê"""
        cards_frame = ttk.Frame(parent, style="Content.TFrame")
        cards_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        cards_frame.columnconfigure(0, weight=1)
        cards_frame.columnconfigure(1, weight=1)
        cards_frame.columnconfigure(2, weight=1)
        
        # Card 1 - Tổng số học sinh
        self._create_stat_card(cards_frame, "👥", "Tổng học sinh", 
                             str(self.report_data.get('total_students', 0)), 
                             "Học sinh", 0, 0)
        
        # Card 2 - Điểm trung bình tổng
        self._create_stat_card(cards_frame, "📊", "Điểm TB tổng", 
                             f"{self.report_data.get('avg_score', 0):.1f}", 
                             "Điểm", 0, 1)
        
        # Card 3 - Điểm Toán
        self._create_stat_card(cards_frame, "🔢", "Điểm Toán", 
                             f"{self.report_data.get('math_avg', 0):.1f}", 
                             "Điểm", 0, 2)
        
        # Card 4 - Điểm Văn
        self._create_stat_card(cards_frame, "📝", "Điểm Văn", 
                             f"{self.report_data.get('literature_avg', 0):.1f}", 
                             "Điểm", 1, 0)
        
        # Card 5 - Điểm Tiếng Anh
        self._create_stat_card(cards_frame, "🌍", "Điểm Tiếng Anh", 
                             f"{self.report_data.get('english_avg', 0):.1f}", 
                             "Điểm", 1, 1)
    
    def _create_stat_card(self, parent, icon, title, value, unit, row, col):
        """Tạo một thẻ thống kê với background trắng"""
        card = tk.Frame(parent, bg="white", relief="solid", borderwidth=1)
        card.grid(row=row, column=col, sticky="ew", padx=5, pady=5)
        card.columnconfigure(0, weight=1)
        
        # Icon và title
        header_frame = tk.Frame(card, bg="white")
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        
        icon_label = tk.Label(header_frame, text=icon, font=("Helvetica", 16), 
                            bg="white", fg="#4f46e5")
        icon_label.grid(row=0, column=0, padx=(0, 5))
        
        title_label = tk.Label(header_frame, text=title, font=("Helvetica", 12, "bold"), 
                             bg="white", fg="#374151")
        title_label.grid(row=0, column=1, sticky="w")
        
        # Value
        value_label = tk.Label(card, text=value, font=("Helvetica", 24, "bold"), 
                              bg="white", fg="#1f2937")
        value_label.grid(row=1, column=0, pady=5)
        
        # Unit
        unit_label = tk.Label(card, text=unit, font=("Helvetica", 11), 
                             bg="white", fg="#6b7280")
        unit_label.grid(row=2, column=0, pady=(0, 10))
        
        return card
    
    def _load_data_from_api(self):
        """Load dữ liệu từ API"""
        try:
            # Lấy thống kê từ API statistics
            stats_response = get_statistics()
            self.report_data = {
                'total_students': stats_response.get('total_students', 0),
                'avg_score': stats_response.get('avg_overall_score', 0.0),
                'math_avg': stats_response.get('avg_math_score', 0.0),
                'literature_avg': stats_response.get('avg_literature_score', 0.0),
                'english_avg': stats_response.get('avg_english_score', 0.0),
            }
            
            # Lấy dữ liệu học sinh để tính thống kê chi tiết
            students_response = get_students(page=1, page_size=10000)
            self.students_data = students_response.get('items', [])
            
            # Tính thống kê chi tiết từ dữ liệu học sinh
            self._calculate_detailed_statistics()
            
        except (ConnectionError, TimeoutError, ValueError) as e:
            print(f"Lỗi khi tải dữ liệu từ API: {e}")
    
    def _calculate_detailed_statistics(self):
        """Tính toán thống kê chi tiết từ dữ liệu học sinh"""
        if not self.students_data:
            return
        
        # Thống kê theo quê quán (home_town)
        home_town_stats = {}
        for student in self.students_data:
            home_town = student.get('home_town', 'Không xác định')
            if home_town not in home_town_stats:
                home_town_stats[home_town] = {'students': 0, 'scores': []}
            
            home_town_stats[home_town]['students'] += 1
            scores = [
                student.get('math_score'),
                student.get('literature_score'),
                student.get('english_score')
            ]
            # Lọc điểm hợp lệ (0-10)
            valid_scores = [score for score in scores if score is not None and 0 <= score <= 10]
            if len(valid_scores) == 3:  # Chỉ tính học sinh có đủ 3 điểm hợp lệ
                avg_student = sum(valid_scores) / len(valid_scores)
                home_town_stats[home_town]['scores'].append(avg_student)
        
        # Tính điểm trung bình theo quê quán
        class_stats = {}
        for home_town, stats in home_town_stats.items():
            if stats['scores']:
                avg_score_hometown = sum(stats['scores']) / len(stats['scores'])
                class_stats[home_town] = {
                    'students': stats['students'],
                    'avg_score': round(avg_score_hometown, 1)
                }
        
        # Cập nhật thống kê chi tiết
        self.report_data.update({
            'class_stats': class_stats,
        })
    
    def _on_filter_change(self, event=None):
        """Xử lý khi thay đổi filter"""
        if self.filter_var:
            filter_value = self.filter_var.get()
            messagebox.showinfo("Thông báo", f"Đã chọn filter: {filter_value}")
        # Suppress unused argument warning
        _ = event
    
    def _generate_report(self):
        """Tạo báo cáo mới"""
        try:
            messagebox.showinfo("Thông báo", "Đang tạo báo cáo...")
            # Tải lại dữ liệu từ API
            self._load_data_from_api()
            self.refresh()
            messagebox.showinfo("Thành công", "Báo cáo đã được tạo thành công!")
        except (ConnectionError, TimeoutError, ValueError) as e:
            messagebox.showerror("Lỗi", f"Không thể tạo báo cáo: {str(e)}")
    
    def _export_excel(self):
        """Xuất báo cáo ra Excel"""
        
    
    def _print_report(self):
        """In báo cáo"""
        messagebox.showinfo("Thông báo", "Chức năng in báo cáo - Đang phát triển")
    
    def refresh(self):
        """Refresh view"""
        # Cập nhật các thẻ thống kê
        self._update_stat_cards()
    
    def _update_stat_cards(self):
        """Cập nhật các thẻ thống kê với dữ liệu mới"""
        # Tìm và cập nhật các thẻ thống kê
        for widget in self.content_frame.winfo_children():
            if isinstance(widget, ttk.Frame):
                self._update_widget_stats(widget)
    
    def _update_widget_stats(self, widget):
        """Cập nhật thống kê trong widget"""
        for child in widget.winfo_children():
            if isinstance(child, (tk.Frame, ttk.Frame)):
                # Tìm các label chứa giá trị thống kê
                for grandchild in child.winfo_children():
                    if isinstance(grandchild, (tk.Label, ttk.Label)):
                        # Kiểm tra nếu đây là label chứa giá trị (font size lớn)
                        font_info = grandchild.cget("font")
                        if isinstance(font_info, tuple) and len(font_info) >= 2:
                            font_size = font_info[1]
                            if font_size >= 20:  # Label giá trị có font size lớn
                                # Tìm title tương ứng trong cùng parent frame
                                parent_frame = grandchild.master
                                for sibling in parent_frame.winfo_children():
                                    if isinstance(sibling, (tk.Label, ttk.Label)):
                                        sibling_text = sibling.cget("text")
                                        if "Tổng học sinh" in sibling_text:
                                            grandchild.config(text=str(self.report_data.get('total_students', 0)))
                                            break
                                        elif "Điểm TB tổng" in sibling_text:
                                            grandchild.config(text=f"{self.report_data.get('avg_score', 0):.1f}")
                                            break
                                        elif "Điểm Toán" in sibling_text:
                                            grandchild.config(text=f"{self.report_data.get('math_avg', 0):.1f}")
                                            break
                                        elif "Điểm Văn" in sibling_text:
                                            grandchild.config(text=f"{self.report_data.get('literature_avg', 0):.1f}")
                                            break
                                        elif "Điểm Tiếng Anh" in sibling_text:
                                            grandchild.config(text=f"{self.report_data.get('english_avg', 0):.1f}")
                                            break
                self._update_widget_stats(child)
