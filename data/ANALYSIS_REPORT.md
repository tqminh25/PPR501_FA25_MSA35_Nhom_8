
# BÁO CÁO PHÂN TÍCH DỮ LIỆU HỌC SINH
## Thời gian tạo: 2025-10-16 19:17:41

### Tổng quan
- Tổng số biểu đồ được tạo: 9
- Thư mục dữ liệu: /Users/binhpham/Documents/Study/MSE/Bai tap nhonm 8/PPR501_FA25_MSA35_Nhom_8/data

### Các phân tích đã thực hiện:

#### 1. Phân tích cơ bản
- So sánh điểm trung bình theo quê quán (Toán, Văn, Tiếng Anh)
- Xếp hạng tỉnh/thành theo điểm từng môn
- Biểu đồ: avg_math_eng_lit_by_hometown.png
- Biểu đồ: rank_home_town_by_*.png

#### 2. Phân tích theo nhóm tuổi
- Phân chia học sinh theo độ tuổi (16-17, 18-19, 20+)
- So sánh điểm trung bình theo nhóm tuổi
- Phân tích xu hướng điểm số theo tuổi
- Biểu đồ: scores_by_age_groups.png
- Biểu đồ: score_trend_by_age.png
- Biểu đồ: score_distribution_by_age.png

#### 3. Phân tích học sinh xuất sắc/yếu kém
- Top 10% học sinh có điểm cao nhất
- Bottom 10% học sinh có điểm thấp nhất
- So sánh đặc điểm giữa hai nhóm
- Phân tích theo quê quán và tuổi
- Biểu đồ: top_bottom_students_comparison.png
- Biểu đồ: top_bottom_radar_chart.png

### Danh sách file biểu đồ:
1. avg_math_eng_lit_by_hometown.png
2. rank_home_town_by_english_avg.png
3. rank_home_town_by_literature_avg.png
4. rank_home_town_by_math_avg.png
5. score_distribution_by_age.png
6. score_trend_by_age.png
7. scores_by_age_groups.png
8. top_bottom_radar_chart.png
9. top_bottom_students_comparison.png

### Kết luận chính:
1. **Phân tích theo quê quán**: Có sự khác biệt về điểm số giữa các tỉnh/thành
2. **Phân tích theo tuổi**: Nhóm tuổi 20+ chiếm đa số (79%) và có điểm số cao hơn nhóm 18-19
3. **Tương quan tuổi-điểm**: Có tương quan dương nhẹ giữa tuổi và điểm số (r=0.092)
4. **Phân tích xuất sắc/yếu kém**: 
   - Top 10% có điểm TB 8.94, Bottom 10% có điểm TB 5.36
   - Khoảng cách điểm giữa hai nhóm là 2.84 điểm
   - Top 10% mạnh nhất ở môn Tiếng Anh (9.26), Bottom 10% yếu nhất cũng ở Tiếng Anh (3.82)
   - Top 10% tập trung nhiều ở Huế (36.4%) và Cần Thơ (27.3%)

### Khuyến nghị:
- Tiếp tục thu thập dữ liệu để có phân tích sâu hơn
- Phân tích thêm các yếu tố khác như giới tính, loại trường học
- Xây dựng mô hình dự đoán điểm số dựa trên các yếu tố đã phân tích
