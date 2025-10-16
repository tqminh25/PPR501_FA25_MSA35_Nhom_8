"""
analyze_by_age.py
-----------------
Phân tích điểm số theo nhóm tuổi của học sinh
- Tính tuổi từ ngày sinh (dob)
- Phân chia thành các nhóm: 16-17, 18-19, 20+
- So sánh điểm trung bình theo nhóm tuổi
- Tạo biểu đồ so sánh
"""

import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns

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
        # Parse ngày sinh
        dob = datetime.strptime(dob_str, '%Y-%m-%d')
        today = datetime.now()
        
        # Tính tuổi
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age
    except:
        return None

def create_age_groups(df):
    """Tạo nhóm tuổi và thêm vào dataframe"""
    # Tính tuổi
    df['age'] = df['dob'].apply(calculate_age)
    
    # Loại bỏ các record không tính được tuổi
    df = df.dropna(subset=['age'])
    
    # Tạo nhóm tuổi
    def get_age_group(age):
        if age <= 17:
            return '16-17'
        elif age <= 19:
            return '18-19'
        else:
            return '20+'
    
    df['age_group'] = df['age'].apply(get_age_group)
    
    return df

def analyze_by_age_groups(df):
    """Phân tích điểm số theo nhóm tuổi"""
    # Tính thống kê mô tả
    age_stats = df.groupby('age_group').agg({
        'math_score': ['count', 'mean', 'std', 'min', 'max'],
        'literature_score': ['count', 'mean', 'std', 'min', 'max'],
        'english_score': ['count', 'mean', 'std', 'min', 'max'],
        'age': ['min', 'max']
    }).round(2)
    
    # Flatten column names
    age_stats.columns = ['_'.join(col).strip() for col in age_stats.columns]
    
    print("=== PHÂN TÍCH ĐIỂM SỐ THEO NHÓM TUỔI ===")
    print(f"Tổng số học sinh: {len(df)}")
    print(f"Số nhóm tuổi: {df['age_group'].nunique()}")
    print("\nThống kê mô tả:")
    print(age_stats)
    
    # Tính điểm trung bình tổng
    df['total_score'] = df['math_score'] + df['literature_score'] + df['english_score']
    df['average_score'] = df['total_score'] / 3
    
    # Thống kê điểm trung bình theo nhóm tuổi
    avg_by_age = df.groupby('age_group').agg({
        'math_score': 'mean',
        'literature_score': 'mean', 
        'english_score': 'mean',
        'average_score': 'mean',
        'total_score': 'mean'
    }).round(2)
    
    print("\n=== ĐIỂM TRUNG BÌNH THEO NHÓM TUỔI ===")
    print(avg_by_age)
    
    return age_stats, avg_by_age

def create_age_comparison_charts(df, avg_by_age):
    """Tạo biểu đồ so sánh theo nhóm tuổi"""
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # 1. Biểu đồ cột so sánh điểm trung bình
    plt.figure(figsize=(12, 8))
    
    # Chuẩn bị dữ liệu
    age_groups = avg_by_age.index
    math_scores = avg_by_age['math_score']
    lit_scores = avg_by_age['literature_score']
    eng_scores = avg_by_age['english_score']
    
    x = np.arange(len(age_groups))
    width = 0.25
    
    plt.bar(x - width, math_scores, width, label='Toán', color='#1f77b4', alpha=0.8)
    plt.bar(x, lit_scores, width, label='Văn', color='#ff7f0e', alpha=0.8)
    plt.bar(x + width, eng_scores, width, label='Tiếng Anh', color='#2ca02c', alpha=0.8)
    
    plt.xlabel('Nhóm tuổi', fontsize=12)
    plt.ylabel('Điểm trung bình', fontsize=12)
    plt.title('So sánh điểm trung bình theo nhóm tuổi', fontsize=14, fontweight='bold')
    plt.xticks(x, age_groups)
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    
    chart1_path = os.path.join(DATA_DIR, 'scores_by_age_groups.png')
    plt.savefig(chart1_path, dpi=150, bbox_inches='tight')
    print(f"Đã lưu biểu đồ: {chart1_path}")
    
    # 2. Biểu đồ đường xu hướng
    plt.figure(figsize=(10, 6))
    
    # Tính điểm trung bình cho từng tuổi
    age_avg = df.groupby('age')['average_score'].mean().reset_index()
    
    plt.plot(age_avg['age'], age_avg['average_score'], marker='o', linewidth=2, markersize=6)
    plt.xlabel('Tuổi', fontsize=12)
    plt.ylabel('Điểm trung bình tổng', fontsize=12)
    plt.title('Xu hướng điểm số theo tuổi', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    chart2_path = os.path.join(DATA_DIR, 'score_trend_by_age.png')
    plt.savefig(chart2_path, dpi=150, bbox_inches='tight')
    print(f"Đã lưu biểu đồ: {chart2_path}")
    
    # 3. Box plot phân phối điểm theo nhóm tuổi
    plt.figure(figsize=(12, 8))
    
    # Tạo subplot cho 3 môn
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    subjects = ['math_score', 'literature_score', 'english_score']
    subject_names = ['Toán', 'Văn', 'Tiếng Anh']
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    
    for i, (subject, name, color) in enumerate(zip(subjects, subject_names, colors)):
        df.boxplot(column=subject, by='age_group', ax=axes[i], color=color)
        axes[i].set_title(f'Phân phối điểm {name}', fontweight='bold')
        axes[i].set_xlabel('Nhóm tuổi')
        axes[i].set_ylabel('Điểm số')
        axes[i].grid(True, alpha=0.3)
    
    plt.suptitle('Phân phối điểm số theo nhóm tuổi', fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    chart3_path = os.path.join(DATA_DIR, 'score_distribution_by_age.png')
    plt.savefig(chart3_path, dpi=150, bbox_inches='tight')
    print(f"Đã lưu biểu đồ: {chart3_path}")
    
    return [chart1_path, chart2_path, chart3_path]

def create_detailed_analysis(df):
    """Tạo phân tích chi tiết"""
    print("\n=== PHÂN TÍCH CHI TIẾT ===")
    
    # Số lượng học sinh theo nhóm tuổi
    age_counts = df['age_group'].value_counts().sort_index()
    print("\nSố lượng học sinh theo nhóm tuổi:")
    for group, count in age_counts.items():
        percentage = (count / len(df)) * 100
        print(f"  {group}: {count} học sinh ({percentage:.1f}%)")
    
    # Phân tích tương quan tuổi vs điểm số
    correlation = df[['age', 'math_score', 'literature_score', 'english_score', 'average_score']].corr()
    print(f"\nTương quan giữa tuổi và điểm số:")
    print(correlation['age'].round(3))
    
    # Top 5 học sinh có điểm cao nhất theo nhóm tuổi
    print("\nTop 5 học sinh có điểm cao nhất theo nhóm tuổi:")
    for group in df['age_group'].unique():
        group_data = df[df['age_group'] == group].nlargest(5, 'average_score')
        print(f"\nNhóm {group}:")
        for _, student in group_data.iterrows():
            print(f"  {student['last_name']} {student['first_name']} - Điểm TB: {student['average_score']:.2f}")

def main():
    """Hàm chính"""
    print("Bắt đầu phân tích điểm số theo nhóm tuổi...")
    
    # Load dữ liệu
    df = load_data()
    print(f"Đã load {len(df)} học sinh")
    
    # Tạo nhóm tuổi
    df = create_age_groups(df)
    print(f"Sau khi tính tuổi: {len(df)} học sinh")
    
    # Phân tích
    age_stats, avg_by_age = analyze_by_age_groups(df)
    
    # Tạo biểu đồ
    chart_paths = create_age_comparison_charts(df, avg_by_age)
    
    # Phân tích chi tiết
    create_detailed_analysis(df)
    
    print(f"\n=== HOÀN THÀNH ===")
    print(f"Đã tạo {len(chart_paths)} biểu đồ:")
    for path in chart_paths:
        print(f"  - {os.path.basename(path)}")

if __name__ == "__main__":
    main()
