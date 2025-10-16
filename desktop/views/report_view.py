"""
Report View - Báo cáo thống kê
"""

import tkinter as tk
from tkinter import ttk, messagebox
from .base_view import BaseContentView
import sys
import os
from PIL import Image, ImageTk
import glob
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from models.api_client import get_students, get_statistics


class ReportView(BaseContentView):
    """View cho báo cáo thống kê"""
    
    def __init__(self, parent_frame: ttk.Frame):
        self.report_data = {}
        self.students_data = []
        self.filter_var = None
        self.details_text = None
        self.chart_images = []
        self.current_chart_index = 0
        self.data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
        self._load_data_from_api()
        self._load_chart_images()
        
        super().__init__(parent_frame, "📋 Báo cáo thống kê")
    
    def _create_content(self):
        self._create_toolbar()
        self._create_report_content()
        self._create_charts_panel()
    
    def _create_toolbar(self):
        toolbar_frame = ttk.Frame(self.content_frame, style="Content.TFrame")
        toolbar_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(0, 10))
        toolbar_frame.columnconfigure(1, weight=1)
    
    def _create_report_content(self):
        content_frame = ttk.Frame(self.content_frame, style="Content.TFrame")
        content_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)
        content_frame.columnconfigure(2, weight=1)
        content_frame.rowconfigure(0, weight=1)
        
        self._create_statistics_panel(content_frame)
    
    def _create_statistics_panel(self, parent):
        stats_frame = ttk.LabelFrame(parent, text="📈 Thống kê tổng quan", 
                                   style="Content.TFrame")
        stats_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=5)
        stats_frame.columnconfigure(0, weight=1)
        
        self._create_stat_cards(stats_frame)
    
    def _create_stat_cards(self, parent):
        cards_frame = ttk.Frame(parent, style="Content.TFrame")
        cards_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        cards_frame.columnconfigure(0, weight=1)
        cards_frame.columnconfigure(1, weight=1)
        cards_frame.columnconfigure(2, weight=1)
        
        self._create_stat_card(cards_frame, "👥", "Tổng học sinh", 
                             str(self.report_data.get('total_students', 0)), 
                             "Học sinh", 0, 0)
        
        self._create_stat_card(cards_frame, "📊", "Điểm TB tổng", 
                             f"{self.report_data.get('avg_score', 0):.1f}", 
                             "Điểm", 0, 1)
        
        self._create_stat_card(cards_frame, "🔢", "Điểm Toán", 
                             f"{self.report_data.get('math_avg', 0):.1f}", 
                             "Điểm", 0, 2)
        
        self._create_stat_card(cards_frame, "📝", "Điểm Văn", 
                             f"{self.report_data.get('literature_avg', 0):.1f}", 
                             "Điểm", 1, 0)
        
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
        try:
            messagebox.showinfo("Thông báo", "Đang tạo báo cáo...")
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
        self._update_stat_cards()
        self._load_chart_images()
        if hasattr(self, 'chart_frame'):
            self._create_chart_list()
            if self.chart_images:
                self._show_chart(0)
    
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
    
    def _load_chart_images(self):
        """Load tất cả ảnh biểu đồ từ thư mục data"""
        try:
            png_files = glob.glob(os.path.join(self.data_dir, "*.png"))
            self.chart_images = []
            
            for png_file in sorted(png_files):
                try:
                    image = Image.open(png_file)
                    # Resize image để fit trong panel
                    image.thumbnail((800, 600), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(image)
                    self.chart_images.append({
                        'photo': photo,
                        'path': png_file,
                        'name': os.path.basename(png_file)
                    })
                except Exception as e:
                    print(f"Lỗi load ảnh {png_file}: {e}")
            
            print(f"Đã load {len(self.chart_images)} biểu đồ")
            
        except Exception as e:
            print(f"Lỗi khi load biểu đồ: {e}")
            self.chart_images = []
    
    def _create_charts_panel(self):
        """Tạo panel hiển thị biểu đồ"""
        charts_frame = ttk.LabelFrame(self.content_frame, text="📊 Biểu đồ phân tích dữ liệu", 
                                    style="Content.TFrame")
        charts_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))
        charts_frame.columnconfigure(0, weight=1)
        charts_frame.rowconfigure(1, weight=1)
        
        # Navigation controls
        nav_frame = ttk.Frame(charts_frame, style="Content.TFrame")
        nav_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        nav_frame.columnconfigure(1, weight=1)
        
        # Previous button
        self.prev_btn = ttk.Button(nav_frame, text="◀ Trước", 
                                 command=self._show_previous_chart, state="disabled")
        self.prev_btn.grid(row=0, column=0, padx=(0, 10))
        
        # Chart info
        self.chart_info_label = ttk.Label(nav_frame, text="", style="Content.TLabel")
        self.chart_info_label.grid(row=0, column=1, sticky="ew")
        
        # Next button
        self.next_btn = ttk.Button(nav_frame, text="Sau ▶", 
                                 command=self._show_next_chart, state="disabled")
        self.next_btn.grid(row=0, column=2, padx=(10, 0))
        
        # Chart display area
        self.chart_frame = ttk.Frame(charts_frame, style="Content.TFrame")
        self.chart_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.chart_frame.columnconfigure(0, weight=1)
        self.chart_frame.rowconfigure(0, weight=1)
        
        # Chart list
        self._create_chart_list()
        
        # Show first chart if available
        if self.chart_images:
            self._show_chart(0)
        else:
            no_charts_label = ttk.Label(self.chart_frame, 
                                      text="Không có biểu đồ nào được tìm thấy.\nChạy phân tích dữ liệu để tạo biểu đồ.", 
                                      style="Content.TLabel")
            no_charts_label.grid(row=0, column=0, sticky="nsew")
    
    def _create_chart_list(self):
        """Tạo danh sách biểu đồ"""
        if not self.chart_images:
            return
            
        list_frame = ttk.LabelFrame(self.chart_frame, text="Danh sách biểu đồ", 
                                  style="Content.TFrame")
        list_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=0)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Create listbox
        self.chart_listbox = tk.Listbox(list_frame, height=15)
        self.chart_listbox.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.chart_listbox.bind('<<ListboxSelect>>', self._on_chart_select)
        self.chart_listbox.bind('<Double-Button-1>', self._on_chart_double_click)
        
        # Add charts to listbox
        for i, chart in enumerate(self.chart_images):
            self.chart_listbox.insert(tk.END, chart['name'])
        
        # Chart display area
        self.chart_display_frame = ttk.Frame(self.chart_frame, style="Content.TFrame")
        self.chart_display_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=0)
        self.chart_display_frame.columnconfigure(0, weight=1)
        self.chart_display_frame.rowconfigure(0, weight=1)
    
    def _show_chart(self, index):
        """Hiển thị biểu đồ theo index"""
        if not self.chart_images or index < 0 or index >= len(self.chart_images):
            return
        
        self.current_chart_index = index
        chart = self.chart_images[index]
        
        # Clear previous chart
        for widget in self.chart_display_frame.winfo_children():
            widget.destroy()
        
        # Create scrollable frame for large images
        canvas = tk.Canvas(self.chart_display_frame, bg="white")
        scrollbar_v = ttk.Scrollbar(self.chart_display_frame, orient="vertical", command=canvas.yview)
        scrollbar_h = ttk.Scrollbar(self.chart_display_frame, orient="horizontal", command=canvas.xview)
        
        scrollable_frame = ttk.Frame(canvas)
        
        canvas.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        # Display image with double-click event
        image_label = tk.Label(scrollable_frame, image=chart['photo'], bg="white", cursor="hand2")
        image_label.pack(pady=10)
        image_label.bind("<Double-Button-1>", lambda e: self._show_chart_popup(index))
        
        # Update scroll region
        scrollable_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
        
        # Pack widgets
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar_v.grid(row=0, column=1, sticky="ns")
        scrollbar_h.grid(row=1, column=0, sticky="ew")
        
        # Update navigation buttons
        self.prev_btn.config(state="normal" if index > 0 else "disabled")
        self.next_btn.config(state="normal" if index < len(self.chart_images) - 1 else "disabled")
        
        # Update info label
        self.chart_info_label.config(text=f"Biểu đồ {index + 1}/{len(self.chart_images)}: {chart['name']}")
        
        # Update listbox selection
        if hasattr(self, 'chart_listbox'):
            self.chart_listbox.selection_clear(0, tk.END)
            self.chart_listbox.selection_set(index)
            self.chart_listbox.see(index)
    
    def _show_previous_chart(self):
        """Hiển thị biểu đồ trước"""
        if self.current_chart_index > 0:
            self._show_chart(self.current_chart_index - 1)
    
    def _show_next_chart(self):
        """Hiển thị biểu đồ tiếp theo"""
        if self.current_chart_index < len(self.chart_images) - 1:
            self._show_chart(self.current_chart_index + 1)
    
    def _on_chart_select(self, event):
        selection = self.chart_listbox.curselection()
        if selection:
            index = selection[0]
            self._show_chart(index)
    
    def _on_chart_double_click(self, event):
        """Xử lý khi double-click vào biểu đồ trong listbox"""
        selection = self.chart_listbox.curselection()
        if selection:
            index = selection[0]
            self._show_chart_popup(index)
    
    def _show_chart_popup(self, index):
        """Hiển thị popup với ảnh biểu đồ lớn và thông tin chi tiết"""
        if not self.chart_images or index < 0 or index >= len(self.chart_images):
            return
        
        chart = self.chart_images[index]
        
        # Tạo popup window
        popup = tk.Toplevel(self.content_frame.winfo_toplevel())
        popup.title(f"Biểu đồ: {chart['name']}")
        popup.geometry("1200x800")
        popup.configure(bg="white")
        
        # Center popup
        popup.transient(self.content_frame.winfo_toplevel())
        popup.grab_set()
        
        # Main frame
        main_frame = tk.Frame(popup, bg="white")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        main_frame.columnconfigure(0, weight=2)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # Left panel - Image
        image_frame = tk.LabelFrame(main_frame, text="Biểu đồ", bg="white", fg="#374151", font=("Arial", 12, "bold"))
        image_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        image_frame.columnconfigure(0, weight=1)
        image_frame.rowconfigure(0, weight=1)
        
        # Load full size image
        try:
            full_image = Image.open(chart['path'])
            # Resize to fit popup but maintain aspect ratio
            max_width, max_height = 800, 600
            image_width, image_height = full_image.size
            
            # Calculate new size maintaining aspect ratio
            ratio = min(max_width/image_width, max_height/image_height)
            new_width = int(image_width * ratio)
            new_height = int(image_height * ratio)
            
            resized_image = full_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            popup_photo = ImageTk.PhotoImage(resized_image)
            
            # Create scrollable canvas for large images
            canvas = tk.Canvas(image_frame, bg="white")
            scrollbar_v = ttk.Scrollbar(image_frame, orient="vertical", command=canvas.yview)
            scrollbar_h = ttk.Scrollbar(image_frame, orient="horizontal", command=canvas.xview)
            
            canvas.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)
            
            # Add image to canvas
            canvas.create_image(0, 0, anchor="nw", image=popup_photo)
            canvas.configure(scrollregion=canvas.bbox("all"))
            
            # Pack widgets
            canvas.grid(row=0, column=0, sticky="nsew")
            scrollbar_v.grid(row=0, column=1, sticky="ns")
            scrollbar_h.grid(row=1, column=0, sticky="ew")
            
            # Keep reference to prevent garbage collection
            canvas.image = popup_photo
            
        except Exception as e:
            error_label = tk.Label(image_frame, text=f"Lỗi load ảnh: {e}", bg="white", fg="red")
            error_label.grid(row=0, column=0, sticky="nsew")
        
        # Right panel - Information
        info_frame = tk.LabelFrame(main_frame, text="Thông tin biểu đồ", bg="white", fg="#374151", font=("Arial", 12, "bold"))
        info_frame.grid(row=0, column=1, sticky="nsew")
        info_frame.columnconfigure(0, weight=1)
        
        # Create scrollable text area
        text_frame = tk.Frame(info_frame, bg="white")
        text_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        text_widget = tk.Text(text_frame, wrap="word", bg="white", fg="#374151", 
                            font=("Arial", 10), padx=10, pady=10)
        scrollbar_text = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar_text.set)
        
        # Get chart information
        chart_info = self._get_chart_information(chart['name'])
        
        # Insert information
        text_widget.insert("1.0", chart_info)
        text_widget.config(state="disabled")
        
        text_widget.grid(row=0, column=0, sticky="nsew")
        scrollbar_text.grid(row=0, column=1, sticky="ns")
        
        # Close button
        close_btn = tk.Button(main_frame, text="Đóng", command=popup.destroy, 
                            bg="#ef4444", fg="white", font=("Arial", 10, "bold"),
                            padx=20, pady=5, cursor="hand2")
        close_btn.grid(row=1, column=0, columnspan=2, pady=(10, 0))
    
    def _get_chart_information(self, chart_name):
        """Lấy thông tin chi tiết về biểu đồ"""
        info = f"📊 TÊN BIỂU ĐỒ: {chart_name}\n\n"
        
        # Chart descriptions based on filename
        chart_descriptions = {
            "avg_math_eng_lit_by_hometown.png": {
                "title": "So sánh điểm trung bình theo quê quán",
                "description": "Biểu đồ so sánh điểm trung bình của 3 môn học (Toán, Văn, Tiếng Anh) theo từng tỉnh/thành phố.",
                "insights": [
                    "• Thể hiện sự khác biệt về chất lượng giáo dục giữa các vùng miền",
                    "• Giúp xác định tỉnh/thành có kết quả học tập tốt nhất",
                    "• Phân tích xu hướng điểm số theo địa lý"
                ]
            },
            "rank_home_town_by_english_avg.png": {
                "title": "Xếp hạng tỉnh/thành theo điểm Tiếng Anh",
                "description": "Bảng xếp hạng các tỉnh/thành phố theo điểm trung bình môn Tiếng Anh từ thấp đến cao.",
                "insights": [
                    "• Xác định vùng có trình độ Tiếng Anh tốt nhất",
                    "• Phân tích khoảng cách giáo dục giữa các vùng",
                    "• Hỗ trợ hoạch định chính sách giáo dục"
                ]
            },
            "rank_home_town_by_math_avg.png": {
                "title": "Xếp hạng tỉnh/thành theo điểm Toán",
                "description": "Bảng xếp hạng các tỉnh/thành phố theo điểm trung bình môn Toán từ thấp đến cao.",
                "insights": [
                    "• Đánh giá năng lực toán học theo vùng miền",
                    "• Xác định vùng cần hỗ trợ về giáo dục Toán",
                    "• Phân tích chất lượng dạy học môn Toán"
                ]
            },
            "rank_home_town_by_literature_avg.png": {
                "title": "Xếp hạng tỉnh/thành theo điểm Văn",
                "description": "Bảng xếp hạng các tỉnh/thành phố theo điểm trung bình môn Văn từ thấp đến cao.",
                "insights": [
                    "• Đánh giá năng lực ngôn ngữ và văn học",
                    "• Phân tích chất lượng giáo dục nhân văn",
                    "• Xác định vùng có thế mạnh về Văn học"
                ]
            },
            "scores_by_age_groups.png": {
                "title": "So sánh điểm số theo nhóm tuổi",
                "description": "Biểu đồ so sánh điểm trung bình của các môn học theo nhóm tuổi (16-17, 18-19, 20+).",
                "insights": [
                    "• Phân tích tác động của tuổi tác đến kết quả học tập",
                    "• Xác định nhóm tuổi có kết quả tốt nhất",
                    "• Hỗ trợ thiết kế chương trình học phù hợp"
                ]
            },
            "score_trend_by_age.png": {
                "title": "Xu hướng điểm số theo tuổi",
                "description": "Biểu đồ đường thể hiện xu hướng thay đổi điểm số theo độ tuổi của học sinh.",
                "insights": [
                    "• Phân tích mối tương quan giữa tuổi và điểm số",
                    "• Xác định độ tuổi tối ưu cho học tập",
                    "• Dự đoán xu hướng kết quả học tập"
                ]
            },
            "score_distribution_by_age.png": {
                "title": "Phân phối điểm số theo nhóm tuổi",
                "description": "Biểu đồ box plot thể hiện phân phối điểm số của từng môn học theo nhóm tuổi.",
                "insights": [
                    "• Phân tích độ phân tán điểm số trong từng nhóm tuổi",
                    "• Xác định outliers và học sinh đặc biệt",
                    "• So sánh tính ổn định điểm số giữa các nhóm"
                ]
            },
            "top_bottom_students_comparison.png": {
                "title": "So sánh học sinh xuất sắc và yếu kém",
                "description": "Biểu đồ tổng hợp so sánh đặc điểm của Top 10% và Bottom 10% học sinh.",
                "insights": [
                    "• Phân tích sự khác biệt giữa học sinh giỏi và yếu",
                    "• Xác định yếu tố ảnh hưởng đến kết quả học tập",
                    "• Hỗ trợ xây dựng chiến lược giáo dục cá biệt hóa"
                ]
            },
            "top_bottom_radar_chart.png": {
                "title": "Biểu đồ radar so sánh điểm từng môn",
                "description": "Biểu đồ radar thể hiện điểm trung bình từng môn học của Top 10% và Bottom 10%.",
                "insights": [
                    "• So sánh thế mạnh/yếu của từng nhóm học sinh",
                    "• Xác định môn học có sự phân hóa lớn nhất",
                    "• Hỗ trợ xây dựng chương trình bồi dưỡng phù hợp"
                ]
            }
        }
        
        chart_info = chart_descriptions.get(chart_name, {
            "title": "Biểu đồ phân tích dữ liệu",
            "description": "Biểu đồ được tạo từ dữ liệu phân tích học sinh.",
            "insights": ["• Biểu đồ cung cấp thông tin chi tiết về dữ liệu học sinh"]
        })
        
        info += f"📋 MÔ TẢ:\n{chart_info['description']}\n\n"
        info += f"💡 INSIGHTS:\n"
        for insight in chart_info['insights']:
            info += f"{insight}\n"
        
        info += f"\n📁 ĐƯỜNG DẪN:\n{os.path.join(self.data_dir, chart_name)}\n\n"
        info += f"📊 DỮ LIỆU:\n"
        info += f"• Tổng số học sinh: {self.report_data.get('total_students', 0)}\n"
        info += f"• Điểm TB tổng: {self.report_data.get('avg_score', 0):.2f}\n"
        info += f"• Điểm TB Toán: {self.report_data.get('math_avg', 0):.2f}\n"
        info += f"• Điểm TB Văn: {self.report_data.get('literature_avg', 0):.2f}\n"
        info += f"• Điểm TB Tiếng Anh: {self.report_data.get('english_avg', 0):.2f}\n"
        
        return info
