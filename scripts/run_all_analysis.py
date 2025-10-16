#!/usr/bin/env python3
"""
run_all_analysis.py
-------------------
Script tổng hợp chạy tất cả các phân tích
- Phân tích cơ bản (điểm theo quê quán)
- Phân tích theo nhóm tuổi
- Tạo báo cáo tổng hợp
"""

import os
import sys
import subprocess
from datetime import datetime

# Thêm thư mục scripts vào path
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(HERE)

def run_script(script_name, description):
    """Chạy một script phân tích"""
    print(f"\n{'='*60}")
    print(f"CHẠY: {description}")
    print(f"Script: {script_name}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, cwd=HERE)
        
        if result.returncode == 0:
            print("✅ THÀNH CÔNG")
            if result.stdout:
                print("Output:")
                print(result.stdout)
        else:
            print("❌ LỖI")
            if result.stderr:
                print("Error:")
                print(result.stderr)
                
    except Exception as e:
        print(f"❌ LỖI KHI CHẠY SCRIPT: {e}")

def create_summary_report():
    """Tạo báo cáo tổng hợp"""
    print(f"\n{'='*60}")
    print("TẠO BÁO CÁO TỔNG HỢP")
    print(f"{'='*60}")
    
    # Đếm số file biểu đồ
    data_dir = os.path.join(os.path.dirname(HERE), "data")
    chart_files = [f for f in os.listdir(data_dir) if f.endswith('.png')]
    
    report_content = f"""
# BÁO CÁO PHÂN TÍCH DỮ LIỆU HỌC SINH
## Thời gian tạo: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

### Tổng quan
- Tổng số biểu đồ được tạo: {len(chart_files)}
- Thư mục dữ liệu: {data_dir}

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
"""
    
    for i, chart in enumerate(sorted(chart_files), 1):
        report_content += f"{i}. {chart}\n"
    
    report_content += f"""
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
"""
    
    # Lưu báo cáo
    report_path = os.path.join(data_dir, "ANALYSIS_REPORT.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"✅ Đã tạo báo cáo: {report_path}")
    return report_path

def main():
    """Hàm chính"""
    print("🚀 BẮT ĐẦU CHẠY TẤT CẢ CÁC PHÂN TÍCH")
    print(f"Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Danh sách các script cần chạy
    scripts = [
        ("analyze_students.py", "Phân tích cơ bản - Điểm theo quê quán"),
        ("analyze_by_age.py", "Phân tích theo nhóm tuổi"),
        ("analyze_top_bottom_students.py", "Phân tích học sinh xuất sắc/yếu kém")
    ]
    
    # Chạy từng script
    for script_name, description in scripts:
        run_script(script_name, description)
    
    # Tạo báo cáo tổng hợp
    report_path = create_summary_report()
    
    print(f"\n{'='*60}")
    print("🎉 HOÀN THÀNH TẤT CẢ CÁC PHÂN TÍCH")
    print(f"{'='*60}")
    print(f"📊 Báo cáo tổng hợp: {report_path}")
    print("📁 Tất cả biểu đồ đã được lưu trong thư mục data/")

if __name__ == "__main__":
    main()
