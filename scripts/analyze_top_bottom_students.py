"""
analyze_top_bottom_students.py
------------------------------
Phân tích học sinh xuất sắc và yếu kém
- Top 10% học sinh có điểm cao nhất
- Bottom 10% học sinh có điểm thấp nhất
- So sánh đặc điểm giữa hai nhóm
- Tạo biểu đồ so sánh
"""

import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Thiết lập font cho tiếng Việt
plt.rcParams['font.family'] = ['Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ_ROOT = os.path.dirname(HERE)
DATA_DIR = os.path.join(PROJ_ROOT, "data")

def load_data():
    """Load dữ liệu học sinh đã được làm sạch"""
    json_path = os.path.join(DATA_DIR, "students_clean.json")
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Không tìm thấy file {json_path}")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    df = pd.DataFrame(data)
    return df

def calculate_age(dob_str):
    """Tính tuổi từ ngày sinh"""
    try:
        from datetime import datetime
        dob = datetime.strptime(dob_str, '%Y-%m-%d')
        today = datetime.now()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age
    except:
        return None

def prepare_data(df):
    """Chuẩn bị dữ liệu cho phân tích"""
    # Tính điểm trung bình
    df['average_score'] = (df['math_score'] + df['literature_score'] + df['english_score']) / 3
    df['total_score'] = df['math_score'] + df['literature_score'] + df['english_score']
    
    # Tính tuổi
    df['age'] = df['dob'].apply(calculate_age)
    
    # Tạo nhóm tuổi
    def get_age_group(age):
        if pd.isna(age):
            return 'Unknown'
        elif age <= 17:
            return '16-17'
        elif age <= 19:
            return '18-19'
        else:
            return '20+'
    
    df['age_group'] = df['age'].apply(get_age_group)
    
    return df

def identify_top_bottom_students(df, percentile=10):
    """Xác định học sinh top và bottom"""
    # Tính percentile
    top_threshold = df['average_score'].quantile(1 - percentile/100)
    bottom_threshold = df['average_score'].quantile(percentile/100)
    
    # Phân loại học sinh
    df['performance_category'] = 'Average'
    df.loc[df['average_score'] >= top_threshold, 'performance_category'] = 'Top'
    df.loc[df['average_score'] <= bottom_threshold, 'performance_category'] = 'Bottom'
    
    # Lấy danh sách top và bottom
    top_students = df[df['performance_category'] == 'Top'].copy()
    bottom_students = df[df['performance_category'] == 'Bottom'].copy()
    
    return top_students, bottom_students, top_threshold, bottom_threshold

def analyze_characteristics(top_students, bottom_students):
    """Phân tích đặc điểm của hai nhóm"""
    print("=== PHÂN TÍCH HỌC SINH XUẤT SẮC VÀ YẾU KÉM ===")
    print(f"Top 10%: {len(top_students)} học sinh")
    print(f"Bottom 10%: {len(bottom_students)} học sinh")
    
    # Thống kê mô tả
    print("\n=== THỐNG KÊ MÔ TẢ ===")
    
    # Điểm số
    print("\nĐiểm trung bình:")
    print(f"Top 10%: {top_students['average_score'].mean():.2f}")
    print(f"Bottom 10%: {bottom_students['average_score'].mean():.2f}")
    
    print("\nĐiểm từng môn (Top 10%):")
    print(f"  Toán: {top_students['math_score'].mean():.2f}")
    print(f"  Văn: {top_students['literature_score'].mean():.2f}")
    print(f"  Tiếng Anh: {top_students['english_score'].mean():.2f}")
    
    print("\nĐiểm từng môn (Bottom 10%):")
    print(f"  Toán: {bottom_students['math_score'].mean():.2f}")
    print(f"  Văn: {bottom_students['literature_score'].mean():.2f}")
    print(f"  Tiếng Anh: {bottom_students['english_score'].mean():.2f}")
    
    # Phân tích theo quê quán
    print("\n=== PHÂN TÍCH THEO QUÊ QUÁN ===")
    top_hometowns = top_students['home_town'].value_counts()
    bottom_hometowns = bottom_students['home_town'].value_counts()
    
    print("\nTop 10% - Quê quán phổ biến:")
    for hometown, count in top_hometowns.head(5).items():
        percentage = (count / len(top_students)) * 100
        print(f"  {hometown}: {count} học sinh ({percentage:.1f}%)")
    
    print("\nBottom 10% - Quê quán phổ biến:")
    for hometown, count in bottom_hometowns.head(5).items():
        percentage = (count / len(bottom_students)) * 100
        print(f"  {hometown}: {count} học sinh ({percentage:.1f}%)")
    
    # Phân tích theo tuổi
    print("\n=== PHÂN TÍCH THEO TUỔI ===")
    top_ages = top_students['age_group'].value_counts()
    bottom_ages = bottom_students['age_group'].value_counts()
    
    print("\nTop 10% - Phân bố theo nhóm tuổi:")
    for age_group, count in top_ages.items():
        percentage = (count / len(top_students)) * 100
        print(f"  {age_group}: {count} học sinh ({percentage:.1f}%)")
    
    print("\nBottom 10% - Phân bố theo nhóm tuổi:")
    for age_group, count in bottom_ages.items():
        percentage = (count / len(bottom_students)) * 100
        print(f"  {age_group}: {count} học sinh ({percentage:.1f}%)")
    
    return top_hometowns, bottom_hometowns, top_ages, bottom_ages

def create_comparison_charts(top_students, bottom_students, top_hometowns, bottom_hometowns, top_ages, bottom_ages):
    """Tạo biểu đồ so sánh"""
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # 1. Biểu đồ so sánh điểm số
    plt.figure(figsize=(15, 10))
    
    # Subplot 1: So sánh điểm trung bình
    plt.subplot(2, 3, 1)
    categories = ['Top 10%', 'Bottom 10%']
    avg_scores = [top_students['average_score'].mean(), bottom_students['average_score'].mean()]
    colors = ['#2ecc71', '#e74c3c']
    bars = plt.bar(categories, avg_scores, color=colors, alpha=0.8)
    plt.title('Điểm trung bình tổng', fontweight='bold')
    plt.ylabel('Điểm trung bình')
    
    # Thêm giá trị lên cột
    for bar, score in zip(bars, avg_scores):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                f'{score:.2f}', ha='center', va='bottom', fontweight='bold')
    
    # Subplot 2: So sánh điểm từng môn
    plt.subplot(2, 3, 2)
    subjects = ['Toán', 'Văn', 'Tiếng Anh']
    top_scores = [top_students['math_score'].mean(), top_students['literature_score'].mean(), top_students['english_score'].mean()]
    bottom_scores = [bottom_students['math_score'].mean(), bottom_students['literature_score'].mean(), bottom_students['english_score'].mean()]
    
    x = np.arange(len(subjects))
    width = 0.35
    
    plt.bar(x - width/2, top_scores, width, label='Top 10%', color='#2ecc71', alpha=0.8)
    plt.bar(x + width/2, bottom_scores, width, label='Bottom 10%', color='#e74c3c', alpha=0.8)
    
    plt.title('Điểm trung bình từng môn', fontweight='bold')
    plt.ylabel('Điểm trung bình')
    plt.xticks(x, subjects)
    plt.legend()
    
    # Subplot 3: Phân bố điểm
    plt.subplot(2, 3, 3)
    plt.hist(top_students['average_score'], bins=10, alpha=0.7, label='Top 10%', color='#2ecc71', density=True)
    plt.hist(bottom_students['average_score'], bins=10, alpha=0.7, label='Bottom 10%', color='#e74c3c', density=True)
    plt.title('Phân phối điểm số', fontweight='bold')
    plt.xlabel('Điểm trung bình')
    plt.ylabel('Mật độ')
    plt.legend()
    
    # Subplot 4: So sánh quê quán (Top 5)
    plt.subplot(2, 3, 4)
    top_hometowns_top5 = top_hometowns.head(5)
    bottom_hometowns_top5 = bottom_hometowns.head(5)
    
    # Tạo dữ liệu cho biểu đồ
    hometowns = list(set(top_hometowns_top5.index) | set(bottom_hometowns_top5.index))
    top_counts = [top_hometowns.get(h, 0) for h in hometowns]
    bottom_counts = [bottom_hometowns.get(h, 0) for h in hometowns]
    
    x = np.arange(len(hometowns))
    width = 0.35
    
    plt.bar(x - width/2, top_counts, width, label='Top 10%', color='#2ecc71', alpha=0.8)
    plt.bar(x + width/2, bottom_counts, width, label='Bottom 10%', color='#e74c3c', alpha=0.8)
    
    plt.title('Phân bố theo quê quán (Top 5)', fontweight='bold')
    plt.ylabel('Số lượng học sinh')
    plt.xticks(x, hometowns, rotation=45)
    plt.legend()
    
    # Subplot 5: So sánh nhóm tuổi
    plt.subplot(2, 3, 5)
    age_groups = list(set(top_ages.index) | set(bottom_ages.index))
    top_age_counts = [top_ages.get(age, 0) for age in age_groups]
    bottom_age_counts = [bottom_ages.get(age, 0) for age in age_groups]
    
    x = np.arange(len(age_groups))
    width = 0.35
    
    plt.bar(x - width/2, top_age_counts, width, label='Top 10%', color='#2ecc71', alpha=0.8)
    plt.bar(x + width/2, bottom_age_counts, width, label='Bottom 10%', color='#e74c3c', alpha=0.8)
    
    plt.title('Phân bố theo nhóm tuổi', fontweight='bold')
    plt.ylabel('Số lượng học sinh')
    plt.xticks(x, age_groups)
    plt.legend()
    
    # Subplot 6: Scatter plot tuổi vs điểm
    plt.subplot(2, 3, 6)
    plt.scatter(top_students['age'], top_students['average_score'], 
               alpha=0.7, label='Top 10%', color='#2ecc71', s=50)
    plt.scatter(bottom_students['age'], bottom_students['average_score'], 
               alpha=0.7, label='Bottom 10%', color='#e74c3c', s=50)
    
    plt.title('Tương quan tuổi và điểm số', fontweight='bold')
    plt.xlabel('Tuổi')
    plt.ylabel('Điểm trung bình')
    plt.legend()
    
    plt.tight_layout()
    
    chart1_path = os.path.join(DATA_DIR, 'top_bottom_students_comparison.png')
    plt.savefig(chart1_path, dpi=150, bbox_inches='tight')
    print(f"Đã lưu biểu đồ: {chart1_path}")
    
    # 2. Biểu đồ chi tiết top và bottom students
    create_detailed_charts(top_students, bottom_students)
    
    return chart1_path

def create_detailed_charts(top_students, bottom_students):
    """Tạo biểu đồ chi tiết"""
    
    # Biểu đồ radar chart so sánh
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), subplot_kw=dict(projection='polar'))
    
    # Dữ liệu cho radar chart
    categories = ['Toán', 'Văn', 'Tiếng Anh']
    top_values = [top_students['math_score'].mean(), 
                  top_students['literature_score'].mean(), 
                  top_students['english_score'].mean()]
    bottom_values = [bottom_students['math_score'].mean(), 
                     bottom_students['literature_score'].mean(), 
                     bottom_students['english_score'].mean()]
    
    # Normalize values to 0-10 scale
    top_values_norm = [v for v in top_values]
    bottom_values_norm = [v for v in bottom_values]
    
    # Top 10% radar chart
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    top_values_norm += top_values_norm[:1]  # Complete the circle
    angles += angles[:1]
    
    ax1.plot(angles, top_values_norm, 'o-', linewidth=2, color='#2ecc71', label='Top 10%')
    ax1.fill(angles, top_values_norm, alpha=0.25, color='#2ecc71')
    ax1.set_xticks(angles[:-1])
    ax1.set_xticklabels(categories)
    ax1.set_ylim(0, 10)
    ax1.set_title('Top 10% - Điểm trung bình từng môn', fontweight='bold', pad=20)
    ax1.grid(True)
    
    # Bottom 10% radar chart
    bottom_values_norm += bottom_values_norm[:1]  # Complete the circle
    
    ax2.plot(angles, bottom_values_norm, 'o-', linewidth=2, color='#e74c3c', label='Bottom 10%')
    ax2.fill(angles, bottom_values_norm, alpha=0.25, color='#e74c3c')
    ax2.set_xticks(angles[:-1])
    ax2.set_xticklabels(categories)
    ax2.set_ylim(0, 10)
    ax2.set_title('Bottom 10% - Điểm trung bình từng môn', fontweight='bold', pad=20)
    ax2.grid(True)
    
    plt.tight_layout()
    
    chart2_path = os.path.join(DATA_DIR, 'top_bottom_radar_chart.png')
    plt.savefig(chart2_path, dpi=150, bbox_inches='tight')
    print(f"Đã lưu biểu đồ: {chart2_path}")

def create_detailed_report(top_students, bottom_students, top_threshold, bottom_threshold):
    """Tạo báo cáo chi tiết"""
    print("\n=== BÁO CÁO CHI TIẾT ===")
    
    # Top 10 học sinh xuất sắc nhất
    print("\n🏆 TOP 10 HỌC SINH XUẤT SẮC NHẤT:")
    top_10 = top_students.nlargest(10, 'average_score')
    for i, (_, student) in enumerate(top_10.iterrows(), 1):
        print(f"{i:2d}. {student['last_name']} {student['first_name']} - "
              f"Điểm TB: {student['average_score']:.2f} - "
              f"Quê: {student['home_town']} - "
              f"Tuổi: {student['age']}")
    
    # Bottom 10 học sinh yếu kém nhất
    print("\n📉 BOTTOM 10 HỌC SINH YẾU KÉM NHẤT:")
    bottom_10 = bottom_students.nsmallest(10, 'average_score')
    for i, (_, student) in enumerate(bottom_10.iterrows(), 1):
        print(f"{i:2d}. {student['last_name']} {student['first_name']} - "
              f"Điểm TB: {student['average_score']:.2f} - "
              f"Quê: {student['home_town']} - "
              f"Tuổi: {student['age']}")
    
    # Thống kê so sánh
    print(f"\n📊 THỐNG KÊ SO SÁNH:")
    print(f"Ngưỡng Top 10%: {top_threshold:.2f}")
    print(f"Ngưỡng Bottom 10%: {bottom_threshold:.2f}")
    print(f"Khoảng cách điểm: {top_threshold - bottom_threshold:.2f}")
    
    # Phân tích môn học yếu nhất của bottom 10%
    print(f"\n📚 PHÂN TÍCH MÔN HỌC YẾU NHẤT (Bottom 10%):")
    bottom_subjects = {
        'Toán': bottom_students['math_score'].mean(),
        'Văn': bottom_students['literature_score'].mean(),
        'Tiếng Anh': bottom_students['english_score'].mean()
    }
    weakest_subject = min(bottom_subjects, key=bottom_subjects.get)
    print(f"Môn yếu nhất: {weakest_subject} ({bottom_subjects[weakest_subject]:.2f})")
    
    # Phân tích môn học mạnh nhất của top 10%
    print(f"\n💪 PHÂN TÍCH MÔN HỌC MẠNH NHẤT (Top 10%):")
    top_subjects = {
        'Toán': top_students['math_score'].mean(),
        'Văn': top_students['literature_score'].mean(),
        'Tiếng Anh': top_students['english_score'].mean()
    }
    strongest_subject = max(top_subjects, key=top_subjects.get)
    print(f"Môn mạnh nhất: {strongest_subject} ({top_subjects[strongest_subject]:.2f})")

def main():
    """Hàm chính"""
    print("🎯 BẮT ĐẦU PHÂN TÍCH HỌC SINH XUẤT SẮC VÀ YẾU KÉM")
    
    # Load và chuẩn bị dữ liệu
    df = load_data()
    df = prepare_data(df)
    
    # Xác định top và bottom students
    top_students, bottom_students, top_threshold, bottom_threshold = identify_top_bottom_students(df)
    
    # Phân tích đặc điểm
    top_hometowns, bottom_hometowns, top_ages, bottom_ages = analyze_characteristics(top_students, bottom_students)
    
    # Tạo biểu đồ
    chart_paths = create_comparison_charts(top_students, bottom_students, top_hometowns, bottom_hometowns, top_ages, bottom_ages)
    
    # Tạo báo cáo chi tiết
    create_detailed_report(top_students, bottom_students, top_threshold, bottom_threshold)
    
    print(f"\n✅ HOÀN THÀNH PHÂN TÍCH")
    print(f"📊 Đã tạo biểu đồ so sánh")
    print(f"📈 Top 10%: {len(top_students)} học sinh")
    print(f"📉 Bottom 10%: {len(bottom_students)} học sinh")

if __name__ == "__main__":
    main()
