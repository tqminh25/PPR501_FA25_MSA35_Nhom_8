#!/usr/bin/env python3
"""
create_system_overview.py
------------------------
Tạo diagram tổng quan toàn bộ hệ thống Student Management
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np

# Thiết lập font cho tiếng Việt
plt.rcParams['font.family'] = ['Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def create_system_overview_diagram():
    """Tạo diagram tổng quan toàn bộ hệ thống"""
    fig, ax = plt.subplots(1, 1, figsize=(18, 12))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Colors
    colors = {
        'frontend': '#e8f5e8',
        'backend': '#e3f2fd', 
        'database': '#fff3e0',
        'data': '#f3e5f5',
        'analysis': '#fce4ec'
    }
    
    # Title
    ax.text(6, 9.5, 'STUDENT MANAGEMENT SYSTEM - TỔNG QUAN KIẾN TRÚC', 
            ha='center', va='center', fontsize=22, fontweight='bold', color='#1565c0')
    
    # Frontend Layer
    frontend_box = FancyBboxPatch((0.5, 7.5), 3, 1.5, 
                                 boxstyle="round,pad=0.2", 
                                 facecolor=colors['frontend'], 
                                 edgecolor='#2e7d32', linewidth=3)
    ax.add_patch(frontend_box)
    ax.text(2, 8.7, 'FRONTEND LAYER', ha='center', va='center', 
            fontsize=14, fontweight='bold', color='#2e7d32')
    ax.text(2, 8.3, 'Desktop Application', ha='center', va='center', 
            fontsize=12, color='#424242')
    ax.text(2, 8.0, '• Tkinter GUI', ha='center', va='center', 
            fontsize=10, color='#424242')
    ax.text(2, 7.7, '• Login System', ha='center', va='center', 
            fontsize=10, color='#424242')
    ax.text(2, 7.4, '• Student Management', ha='center', va='center', 
            fontsize=10, color='#424242')
    ax.text(2, 7.1, '• Report & Analytics', ha='center', va='center', 
            fontsize=10, color='#424242')
    
    # Backend Layer
    backend_box = FancyBboxPatch((4, 7.5), 3, 1.5, 
                                boxstyle="round,pad=0.2", 
                                facecolor=colors['backend'], 
                                edgecolor='#1976d2', linewidth=3)
    ax.add_patch(backend_box)
    ax.text(5.5, 8.7, 'BACKEND LAYER', ha='center', va='center', 
            fontsize=14, fontweight='bold', color='#1976d2')
    ax.text(5.5, 8.3, 'FastAPI Server', ha='center', va='center', 
            fontsize=12, color='#424242')
    ax.text(5.5, 8.0, '• RESTful API', ha='center', va='center', 
            fontsize=10, color='#424242')
    ax.text(5.5, 7.7, '• Data Validation', ha='center', va='center', 
            fontsize=10, color='#424242')
    ax.text(5.5, 7.4, '• CRUD Operations', ha='center', va='center', 
            fontsize=10, color='#424242')
    ax.text(5.5, 7.1, '• Statistics API', ha='center', va='center', 
            fontsize=10, color='#424242')
    
    # Database Layer
    db_box = FancyBboxPatch((7.5, 7.5), 3, 1.5, 
                           boxstyle="round,pad=0.2", 
                           facecolor=colors['database'], 
                           edgecolor='#f57c00', linewidth=3)
    ax.add_patch(db_box)
    ax.text(9, 8.7, 'DATABASE LAYER', ha='center', va='center', 
            fontsize=14, fontweight='bold', color='#f57c00')
    ax.text(9, 8.3, 'SQLite Database', ha='center', va='center', 
            fontsize=12, color='#424242')
    ax.text(9, 8.0, '• Student Table', ha='center', va='center', 
            fontsize=10, color='#424242')
    ax.text(9, 7.7, '• 9 Columns', ha='center', va='center', 
            fontsize=10, color='#424242')
    ax.text(9, 7.4, '• Indexes & Constraints', ha='center', va='center', 
            fontsize=10, color='#424242')
    ax.text(9, 7.1, '• Data Integrity', ha='center', va='center', 
            fontsize=10, color='#424242')
    
    # Data Analysis Layer
    analysis_box = FancyBboxPatch((0.5, 5), 5, 1.5, 
                                 boxstyle="round,pad=0.2", 
                                 facecolor=colors['analysis'], 
                                 edgecolor='#c2185b', linewidth=3)
    ax.add_patch(analysis_box)
    ax.text(3, 6.2, 'DATA ANALYSIS LAYER', ha='center', va='center', 
            fontsize=14, fontweight='bold', color='#c2185b')
    ax.text(3, 5.8, 'Python Analysis Scripts', ha='center', va='center', 
            fontsize=12, color='#424242')
    ax.text(1.5, 5.5, '• Age-based Analysis', ha='center', va='center', 
            fontsize=10, color='#424242')
    ax.text(3, 5.5, '• Top/Bottom Students', ha='center', va='center', 
            fontsize=10, color='#424242')
    ax.text(4.5, 5.5, '• Hometown Comparison', ha='center', va='center', 
            fontsize=10, color='#424242')
    ax.text(1.5, 5.2, '• Score Distribution', ha='center', va='center', 
            fontsize=10, color='#424242')
    ax.text(3, 5.2, '• Statistical Reports', ha='center', va='center', 
            fontsize=10, color='#424242')
    ax.text(4.5, 5.2, '• Visualization Charts', ha='center', va='center', 
            fontsize=10, color='#424242')
    
    # Data Storage Layer
    storage_box = FancyBboxPatch((6, 5), 4.5, 1.5, 
                                boxstyle="round,pad=0.2", 
                                facecolor=colors['data'], 
                                edgecolor='#7b1fa2', linewidth=3)
    ax.add_patch(storage_box)
    ax.text(8.25, 6.2, 'DATA STORAGE LAYER', ha='center', va='center', 
            fontsize=14, fontweight='bold', color='#7b1fa2')
    ax.text(8.25, 5.8, 'File System Storage', ha='center', va='center', 
            fontsize=12, color='#424242')
    ax.text(7, 5.5, '• Raw Data (JSONL)', ha='center', va='center', 
            fontsize=10, color='#424242')
    ax.text(8.25, 5.5, '• Clean Data (JSON)', ha='center', va='center', 
            fontsize=10, color='#424242')
    ax.text(9.5, 5.5, '• Charts (PNG)', ha='center', va='center', 
            fontsize=10, color='#424242')
    ax.text(7, 5.2, '• Reports (MD)', ha='center', va='center', 
            fontsize=10, color='#424242')
    ax.text(8.25, 5.2, '• Database (SQLite)', ha='center', va='center', 
            fontsize=10, color='#424242')
    ax.text(9.5, 5.2, '• Logs & Configs', ha='center', va='center', 
            fontsize=10, color='#424242')
    
    # Arrows - Data Flow
    # Frontend to Backend
    arrow1 = ConnectionPatch((3.5, 8.25), (4, 8.25), "data", "data",
                           arrowstyle="->", shrinkA=5, shrinkB=5, 
                           mutation_scale=20, fc="#2e7d32", lw=3)
    ax.add_patch(arrow1)
    ax.text(3.7, 8.4, 'HTTP/REST', ha='center', va='center', 
            fontsize=9, color='#2e7d32', fontweight='bold')
    
    # Backend to Database
    arrow2 = ConnectionPatch((7, 8.25), (7.5, 8.25), "data", "data",
                           arrowstyle="->", shrinkA=5, shrinkB=5, 
                           mutation_scale=20, fc="#1976d2", lw=3)
    ax.add_patch(arrow2)
    ax.text(7.2, 8.4, 'SQL', ha='center', va='center', 
            fontsize=9, color='#1976d2', fontweight='bold')
    
    # Database to Analysis
    arrow3 = ConnectionPatch((9, 7.5), (5.5, 6.5), "data", "data",
                           arrowstyle="->", shrinkA=5, shrinkB=5, 
                           mutation_scale=20, fc="#f57c00", lw=3)
    ax.add_patch(arrow3)
    ax.text(7.2, 6.8, 'Data Export', ha='center', va='center', 
            fontsize=9, color='#f57c00', fontweight='bold')
    
    # Analysis to Storage
    arrow4 = ConnectionPatch((5.5, 5), (6, 5), "data", "data",
                           arrowstyle="->", shrinkA=5, shrinkB=5, 
                           mutation_scale=20, fc="#c2185b", lw=3)
    ax.add_patch(arrow4)
    ax.text(5.7, 4.7, 'Save Results', ha='center', va='center', 
            fontsize=9, color='#c2185b', fontweight='bold')
    
    # Storage to Frontend
    arrow5 = ConnectionPatch((6, 5.75), (3.5, 7.5), "data", "data",
                           arrowstyle="->", shrinkA=5, shrinkB=5, 
                           mutation_scale=20, fc="#7b1fa2", lw=3)
    ax.add_patch(arrow5)
    ax.text(4.5, 6.5, 'Load Charts', ha='center', va='center', 
            fontsize=9, color='#7b1fa2', fontweight='bold')
    
    # Technology Stack
    tech_box = FancyBboxPatch((0.5, 2.5), 11, 2, 
                             boxstyle="round,pad=0.2", 
                             facecolor='#fff8e1', 
                             edgecolor='#ff8f00', linewidth=3)
    ax.add_patch(tech_box)
    ax.text(6, 4.2, 'TECHNOLOGY STACK & TOOLS', ha='center', va='center', 
            fontsize=16, fontweight='bold', color='#ff8f00')
    
    # Frontend Tech
    ax.text(2, 3.7, 'Frontend:', ha='left', va='center', 
            fontsize=12, fontweight='bold', color='#2e7d32')
    ax.text(2, 3.4, '• Python Tkinter', ha='left', va='center', 
            fontsize=10, color='#424242')
    ax.text(2, 3.1, '• PIL/Pillow (Images)', ha='left', va='center', 
            fontsize=10, color='#424242')
    ax.text(2, 2.8, '• Custom GUI Framework', ha='left', va='center', 
            fontsize=10, color='#424242')
    
    # Backend Tech
    ax.text(4.5, 3.7, 'Backend:', ha='left', va='center', 
            fontsize=12, fontweight='bold', color='#1976d2')
    ax.text(4.5, 3.4, '• FastAPI', ha='left', va='center', 
            fontsize=10, color='#424242')
    ax.text(4.5, 3.1, '• SQLAlchemy ORM', ha='left', va='center', 
            fontsize=10, color='#424242')
    ax.text(4.5, 2.8, '• Pydantic Validation', ha='left', va='center', 
            fontsize=10, color='#424242')
    
    # Database Tech
    ax.text(7, 3.7, 'Database:', ha='left', va='center', 
            fontsize=12, fontweight='bold', color='#f57c00')
    ax.text(7, 3.4, '• SQLite', ha='left', va='center', 
            fontsize=10, color='#424242')
    ax.text(7, 3.1, '• 9 Columns Schema', ha='left', va='center', 
            fontsize=10, color='#424242')
    ax.text(7, 2.8, '• Indexes & Constraints', ha='left', va='center', 
            fontsize=10, color='#424242')
    
    # Analysis Tech
    ax.text(9.5, 3.7, 'Analysis:', ha='left', va='center', 
            fontsize=12, fontweight='bold', color='#c2185b')
    ax.text(9.5, 3.4, '• Pandas & NumPy', ha='left', va='center', 
            fontsize=10, color='#424242')
    ax.text(9.5, 3.1, '• Matplotlib & Seaborn', ha='left', va='center', 
            fontsize=10, color='#424242')
    ax.text(9.5, 2.8, '• Statistical Analysis', ha='left', va='center', 
            fontsize=10, color='#424242')
    
    # Key Features
    features_box = FancyBboxPatch((0.5, 0.5), 11, 1.5, 
                                 boxstyle="round,pad=0.2", 
                                 facecolor='#e8f5e8', 
                                 edgecolor='#4caf50', linewidth=3)
    ax.add_patch(features_box)
    ax.text(6, 1.7, 'KEY FEATURES & CAPABILITIES', ha='center', va='center', 
            fontsize=16, fontweight='bold', color='#4caf50')
    ax.text(2, 1.3, '• Complete CRUD Operations', ha='left', va='center', 
            fontsize=11, color='#424242')
    ax.text(6, 1.3, '• Advanced Data Analytics', ha='left', va='center', 
            fontsize=11, color='#424242')
    ax.text(9.5, 1.3, '• Interactive Visualizations', ha='left', va='center', 
            fontsize=11, color='#424242')
    ax.text(2, 0.9, '• Real-time Statistics', ha='left', va='center', 
            fontsize=11, color='#424242')
    ax.text(6, 0.9, '• Multi-dimensional Analysis', ha='left', va='center', 
            fontsize=11, color='#424242')
    ax.text(9.5, 0.9, '• Export & Reporting', ha='left', va='center', 
            fontsize=11, color='#424242')
    
    plt.tight_layout()
    return fig

def main():
    """Tạo diagram tổng quan hệ thống"""
    print("Tạo diagram tổng quan hệ thống...")
    
    import os
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)
    
    # Tạo System Overview Diagram
    fig = create_system_overview_diagram()
    fig.savefig(os.path.join(output_dir, "system_overview.png"), 
                 dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Đã tạo: system_overview.png")
    
    print(f"\n🎉 Hoàn thành! Đã tạo diagram tổng quan trong {output_dir}/")
    print("📊 File đã tạo: system_overview.png - Tổng quan toàn bộ hệ thống")

if __name__ == "__main__":
    main()
