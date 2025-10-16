#!/usr/bin/env python3
"""
create_backend_diagram.py
------------------------
Tạo diagram kiến trúc backend cho Student Management System
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np

# Thiết lập font cho tiếng Việt
plt.rcParams['font.family'] = ['Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def create_backend_architecture_diagram():
    """Tạo diagram kiến trúc backend"""
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Colors
    colors = {
        'client': '#e3f2fd',
        'api': '#bbdefb', 
        'business': '#90caf9',
        'data': '#64b5f6',
        'db': '#42a5f5'
    }
    
    # Title
    ax.text(5, 9.5, 'KIẾN TRÚC BACKEND - STUDENT MANAGEMENT SYSTEM', 
            ha='center', va='center', fontsize=20, fontweight='bold', color='#1565c0')
    
    # Client Layer
    client_box = FancyBboxPatch((0.5, 8.2), 2, 0.8, 
                               boxstyle="round,pad=0.1", 
                               facecolor=colors['client'], 
                               edgecolor='#1976d2', linewidth=2)
    ax.add_patch(client_box)
    ax.text(1.5, 8.6, 'CLIENT LAYER', ha='center', va='center', 
            fontsize=12, fontweight='bold', color='#1565c0')
    ax.text(1.5, 8.3, 'Desktop App\n(Tkinter)', ha='center', va='center', 
            fontsize=10, color='#424242')
    
    # API Gateway Layer
    api_box = FancyBboxPatch((3.5, 8.2), 3, 0.8, 
                            boxstyle="round,pad=0.1", 
                            facecolor=colors['api'], 
                            edgecolor='#1976d2', linewidth=2)
    ax.add_patch(api_box)
    ax.text(5, 8.6, 'API GATEWAY LAYER', ha='center', va='center', 
            fontsize=12, fontweight='bold', color='#1565c0')
    ax.text(5, 8.3, 'FastAPI\nCORS Middleware', ha='center', va='center', 
            fontsize=10, color='#424242')
    
    # Business Logic Layer
    business_box = FancyBboxPatch((7, 8.2), 2.5, 0.8, 
                                 boxstyle="round,pad=0.1", 
                                 facecolor=colors['business'], 
                                 edgecolor='#1976d2', linewidth=2)
    ax.add_patch(business_box)
    ax.text(8.25, 8.6, 'BUSINESS LOGIC', ha='center', va='center', 
            fontsize=12, fontweight='bold', color='#1565c0')
    ax.text(8.25, 8.3, 'Routers\nControllers', ha='center', va='center', 
            fontsize=10, color='#424242')
    
    # Data Access Layer
    data_box = FancyBboxPatch((0.5, 6.5), 4, 1.2, 
                             boxstyle="round,pad=0.1", 
                             facecolor=colors['data'], 
                             edgecolor='#1976d2', linewidth=2)
    ax.add_patch(data_box)
    ax.text(2.5, 7.4, 'DATA ACCESS LAYER', ha='center', va='center', 
            fontsize=12, fontweight='bold', color='#1565c0')
    ax.text(2.5, 7.1, 'CRUD Operations\nSQLAlchemy ORM', ha='center', va='center', 
            fontsize=10, color='#424242')
    ax.text(2.5, 6.8, 'Pydantic Schemas\nData Validation', ha='center', va='center', 
            fontsize=10, color='#424242')
    
    # Database Layer
    db_box = FancyBboxPatch((5.5, 6.5), 4, 1.2, 
                           boxstyle="round,pad=0.1", 
                           facecolor=colors['db'], 
                           edgecolor='#1976d2', linewidth=2)
    ax.add_patch(db_box)
    ax.text(7.5, 7.4, 'DATABASE LAYER', ha='center', va='center', 
            fontsize=12, fontweight='bold', color='#1565c0')
    ax.text(7.5, 7.1, 'SQLite Database\nstudents.db', ha='center', va='center', 
            fontsize=10, color='#424242')
    ax.text(7.5, 6.8, 'Student Table\n9 Columns', ha='center', va='center', 
            fontsize=10, color='#424242')
    
    # Arrows
    # Client to API
    arrow1 = ConnectionPatch((2.5, 8.2), (3.5, 8.6), "data", "data",
                           arrowstyle="->", shrinkA=5, shrinkB=5, 
                           mutation_scale=20, fc="black", lw=2)
    ax.add_patch(arrow1)
    ax.text(3, 8.4, 'HTTP/REST', ha='center', va='center', 
            fontsize=9, color='#424242')
    
    # API to Business
    arrow2 = ConnectionPatch((6.5, 8.6), (7, 8.6), "data", "data",
                           arrowstyle="->", shrinkA=5, shrinkB=5, 
                           mutation_scale=20, fc="black", lw=2)
    ax.add_patch(arrow2)
    
    # Business to Data
    arrow3 = ConnectionPatch((8.25, 8.2), (4.5, 6.5), "data", "data",
                           arrowstyle="->", shrinkA=5, shrinkB=5, 
                           mutation_scale=20, fc="black", lw=2)
    ax.add_patch(arrow3)
    
    # Data to Database
    arrow4 = ConnectionPatch((4.5, 6.5), (5.5, 6.5), "data", "data",
                           arrowstyle="->", shrinkA=5, shrinkB=5, 
                           mutation_scale=20, fc="black", lw=2)
    ax.add_patch(arrow4)
    
    # Detailed Components
    # API Endpoints
    endpoints_box = FancyBboxPatch((0.5, 4.5), 4, 1.5, 
                                  boxstyle="round,pad=0.1", 
                                  facecolor='#f3e5f5', 
                                  edgecolor='#7b1fa2', linewidth=2)
    ax.add_patch(endpoints_box)
    ax.text(2.5, 5.7, 'API ENDPOINTS', ha='center', va='center', 
            fontsize=12, fontweight='bold', color='#7b1fa2')
    ax.text(2.5, 5.4, 'GET /students - List students', ha='center', va='center', 
            fontsize=9, color='#424242')
    ax.text(2.5, 5.2, 'POST /students - Create student', ha='center', va='center', 
            fontsize=9, color='#424242')
    ax.text(2.5, 5.0, 'PUT /students/{id} - Update student', ha='center', va='center', 
            fontsize=9, color='#424242')
    ax.text(2.5, 4.8, 'DELETE /students/{id} - Delete student', ha='center', va='center', 
            fontsize=9, color='#424242')
    ax.text(2.5, 4.6, 'GET /students/statistics - Get stats', ha='center', va='center', 
            fontsize=9, color='#424242')
    
    # Database Schema
    schema_box = FancyBboxPatch((5.5, 4.5), 4, 1.5, 
                               boxstyle="round,pad=0.1", 
                               facecolor='#e8f5e8', 
                               edgecolor='#2e7d32', linewidth=2)
    ax.add_patch(schema_box)
    ax.text(7.5, 5.7, 'DATABASE SCHEMA', ha='center', va='center', 
            fontsize=12, fontweight='bold', color='#2e7d32')
    ax.text(7.5, 5.4, 'Table: students', ha='center', va='center', 
            fontsize=10, fontweight='bold', color='#424242')
    ax.text(7.5, 5.2, '• id (PK, Integer)', ha='center', va='center', 
            fontsize=9, color='#424242')
    ax.text(7.5, 5.0, '• student_code (Unique, String)', ha='center', va='center', 
            fontsize=9, color='#424242')
    ax.text(7.5, 4.8, '• first_name, last_name (String)', ha='center', va='center', 
            fontsize=9, color='#424242')
    ax.text(7.5, 4.6, '• email (Unique, String)', ha='center', va='center', 
            fontsize=9, color='#424242')
    ax.text(7.5, 4.4, '• dob (Date), home_town (String)', ha='center', va='center', 
            fontsize=9, color='#424242')
    ax.text(7.5, 4.2, '• math_score, literature_score, english_score (Float)', ha='center', va='center', 
            fontsize=9, color='#424242')
    
    # Technology Stack
    tech_box = FancyBboxPatch((0.5, 2.5), 9, 1.5, 
                             boxstyle="round,pad=0.1", 
                             facecolor='#fff3e0', 
                             edgecolor='#f57c00', linewidth=2)
    ax.add_patch(tech_box)
    ax.text(5, 3.7, 'TECHNOLOGY STACK', ha='center', va='center', 
            fontsize=12, fontweight='bold', color='#f57c00')
    ax.text(2.5, 3.4, 'Backend Framework:\nFastAPI', ha='center', va='center', 
            fontsize=10, color='#424242')
    ax.text(5, 3.4, 'Database ORM:\nSQLAlchemy', ha='center', va='center', 
            fontsize=10, color='#424242')
    ax.text(7.5, 3.4, 'Data Validation:\nPydantic', ha='center', va='center', 
            fontsize=10, color='#424242')
    ax.text(2.5, 3.0, 'Database:\nSQLite', ha='center', va='center', 
            fontsize=10, color='#424242')
    ax.text(5, 3.0, 'API Documentation:\nSwagger/OpenAPI', ha='center', va='center', 
            fontsize=10, color='#424242')
    ax.text(7.5, 3.0, 'CORS:\nCross-Origin Support', ha='center', va='center', 
            fontsize=10, color='#424242')
    
    # Features
    features_box = FancyBboxPatch((0.5, 0.5), 9, 1.5, 
                                 boxstyle="round,pad=0.1", 
                                 facecolor='#fce4ec', 
                                 edgecolor='#c2185b', linewidth=2)
    ax.add_patch(features_box)
    ax.text(5, 1.7, 'KEY FEATURES', ha='center', va='center', 
            fontsize=12, fontweight='bold', color='#c2185b')
    ax.text(2.5, 1.4, '• RESTful API Design', ha='center', va='center', 
            fontsize=10, color='#424242')
    ax.text(5, 1.4, '• Data Validation & Serialization', ha='center', va='center', 
            fontsize=10, color='#424242')
    ax.text(7.5, 1.4, '• Search & Pagination', ha='center', va='center', 
            fontsize=10, color='#424242')
    ax.text(2.5, 1.0, '• Statistics & Analytics', ha='center', va='center', 
            fontsize=10, color='#424242')
    ax.text(5, 1.0, '• Error Handling', ha='center', va='center', 
            fontsize=10, color='#424242')
    ax.text(7.5, 1.0, '• Auto-generated Documentation', ha='center', va='center', 
            fontsize=10, color='#424242')
    
    plt.tight_layout()
    return fig

def create_database_erd_diagram():
    """Tạo ERD diagram cho database"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'ENTITY RELATIONSHIP DIAGRAM - STUDENT TABLE', 
            ha='center', va='center', fontsize=18, fontweight='bold', color='#1565c0')
    
    # Student Table
    table_box = FancyBboxPatch((2, 3), 6, 5, 
                              boxstyle="round,pad=0.2", 
                              facecolor='#e3f2fd', 
                              edgecolor='#1976d2', linewidth=3)
    ax.add_patch(table_box)
    
    # Table Header
    ax.text(5, 7.5, 'STUDENTS', ha='center', va='center', 
            fontsize=16, fontweight='bold', color='#1565c0')
    
    # Table Fields
    fields = [
        ('id', 'INTEGER', 'PRIMARY KEY', 'Auto-increment ID'),
        ('student_code', 'VARCHAR', 'UNIQUE, NOT NULL', 'Mã học sinh'),
        ('first_name', 'VARCHAR', 'NULL', 'Tên'),
        ('last_name', 'VARCHAR', 'NULL', 'Họ'),
        ('email', 'VARCHAR', 'UNIQUE, NULL', 'Email'),
        ('dob', 'DATE', 'NULL', 'Ngày sinh'),
        ('home_town', 'VARCHAR', 'NULL', 'Quê quán'),
        ('math_score', 'FLOAT', 'NULL (0-10)', 'Điểm Toán'),
        ('literature_score', 'FLOAT', 'NULL (0-10)', 'Điểm Văn'),
        ('english_score', 'FLOAT', 'NULL (0-10)', 'Điểm Tiếng Anh')
    ]
    
    y_pos = 6.8
    for field, data_type, constraints, description in fields:
        # Field name
        ax.text(2.5, y_pos, field, ha='left', va='center', 
                fontsize=11, fontweight='bold', color='#1976d2')
        
        # Data type
        ax.text(4, y_pos, data_type, ha='left', va='center', 
                fontsize=10, color='#424242')
        
        # Constraints
        ax.text(5.5, y_pos, constraints, ha='left', va='center', 
                fontsize=9, color='#f57c00')
        
        # Description
        ax.text(7.2, y_pos, description, ha='left', va='center', 
                fontsize=9, color='#666666')
        
        y_pos -= 0.3
    
    # Indexes
    index_box = FancyBboxPatch((1, 1), 8, 1.2, 
                              boxstyle="round,pad=0.1", 
                              facecolor='#f3e5f5', 
                              edgecolor='#7b1fa2', linewidth=2)
    ax.add_patch(index_box)
    ax.text(5, 1.8, 'INDEXES', ha='center', va='center', 
            fontsize=12, fontweight='bold', color='#7b1fa2')
    ax.text(2.5, 1.5, '• PRIMARY KEY: id', ha='left', va='center', 
            fontsize=10, color='#424242')
    ax.text(5, 1.5, '• UNIQUE: student_code', ha='left', va='center', 
            fontsize=10, color='#424242')
    ax.text(7.5, 1.5, '• UNIQUE: email', ha='left', va='center', 
            fontsize=10, color='#424242')
    ax.text(2.5, 1.2, '• INDEX: student_code', ha='left', va='center', 
            fontsize=10, color='#424242')
    ax.text(5, 1.2, '• INDEX: id', ha='left', va='center', 
            fontsize=10, color='#424242')
    
    plt.tight_layout()
    return fig

def create_api_flow_diagram():
    """Tạo diagram luồng API"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'API REQUEST FLOW DIAGRAM', 
            ha='center', va='center', fontsize=18, fontweight='bold', color='#1565c0')
    
    # Client
    client_box = FancyBboxPatch((0.5, 8), 1.5, 0.8, 
                               boxstyle="round,pad=0.1", 
                               facecolor='#e3f2fd', 
                               edgecolor='#1976d2', linewidth=2)
    ax.add_patch(client_box)
    ax.text(1.25, 8.4, 'Desktop App', ha='center', va='center', 
            fontsize=11, fontweight='bold', color='#1565c0')
    
    # FastAPI
    api_box = FancyBboxPatch((2.5, 8), 2, 0.8, 
                            boxstyle="round,pad=0.1", 
                            facecolor='#bbdefb', 
                            edgecolor='#1976d2', linewidth=2)
    ax.add_patch(api_box)
    ax.text(3.5, 8.4, 'FastAPI', ha='center', va='center', 
            fontsize=11, fontweight='bold', color='#1565c0')
    
    # Router
    router_box = FancyBboxPatch((5, 8), 2, 0.8, 
                               boxstyle="round,pad=0.1", 
                               facecolor='#90caf9', 
                               edgecolor='#1976d2', linewidth=2)
    ax.add_patch(router_box)
    ax.text(6, 8.4, 'Router', ha='center', va='center', 
            fontsize=11, fontweight='bold', color='#1565c0')
    
    # CRUD
    crud_box = FancyBboxPatch((7.5, 8), 2, 0.8, 
                             boxstyle="round,pad=0.1", 
                             facecolor='#64b5f6', 
                             edgecolor='#1976d2', linewidth=2)
    ax.add_patch(crud_box)
    ax.text(8.5, 8.4, 'CRUD', ha='center', va='center', 
            fontsize=11, fontweight='bold', color='#1565c0')
    
    # Database
    db_box = FancyBboxPatch((4, 6), 2, 0.8, 
                           boxstyle="round,pad=0.1", 
                           facecolor='#42a5f5', 
                           edgecolor='#1976d2', linewidth=2)
    ax.add_patch(db_box)
    ax.text(5, 6.4, 'SQLite DB', ha='center', va='center', 
            fontsize=11, fontweight='bold', color='#1565c0')
    
    # Arrows
    arrows = [
        ((2, 8.4), (2.5, 8.4), 'HTTP Request'),
        ((4.5, 8.4), (5, 8.4), 'Route to Handler'),
        ((7, 8.4), (7.5, 8.4), 'Business Logic'),
        ((8.5, 8), (5, 6.8), 'SQL Query'),
        ((5, 6), (8.5, 8), 'Data Response'),
        ((7.5, 8), (7, 8), 'Process Data'),
        ((5, 8), (4.5, 8), 'Return Response'),
        ((3.5, 8), (2, 8.4), 'JSON Response')
    ]
    
    for start, end, label in arrows:
        arrow = ConnectionPatch(start, end, "data", "data",
                              arrowstyle="->", shrinkA=5, shrinkB=5, 
                              mutation_scale=15, fc="black", lw=1.5)
        ax.add_patch(arrow)
        
        # Label position
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2
        ax.text(mid_x, mid_y + 0.1, label, ha='center', va='center', 
                fontsize=8, color='#424242')
    
    # Request/Response Details
    details_box = FancyBboxPatch((0.5, 4), 9, 1.5, 
                                boxstyle="round,pad=0.1", 
                                facecolor='#f3e5f5', 
                                edgecolor='#7b1fa2', linewidth=2)
    ax.add_patch(details_box)
    ax.text(5, 5.2, 'REQUEST/RESPONSE FLOW', ha='center', va='center', 
            fontsize=12, fontweight='bold', color='#7b1fa2')
    ax.text(2.5, 4.8, '1. Desktop App sends HTTP request', ha='center', va='center', 
            fontsize=10, color='#424242')
    ax.text(5, 4.8, '2. FastAPI receives & validates', ha='center', va='center', 
            fontsize=10, color='#424242')
    ax.text(7.5, 4.8, '3. Router calls appropriate handler', ha='center', va='center', 
            fontsize=10, color='#424242')
    ax.text(2.5, 4.4, '4. CRUD operations on database', ha='center', va='center', 
            fontsize=10, color='#424242')
    ax.text(5, 4.4, '5. Data returned & serialized', ha='center', va='center', 
            fontsize=10, color='#424242')
    ax.text(7.5, 4.4, '6. JSON response sent to client', ha='center', va='center', 
            fontsize=10, color='#424242')
    
    # Error Handling
    error_box = FancyBboxPatch((0.5, 2), 9, 1.5, 
                              boxstyle="round,pad=0.1", 
                              facecolor='#ffebee', 
                              edgecolor='#d32f2f', linewidth=2)
    ax.add_patch(error_box)
    ax.text(5, 3.2, 'ERROR HANDLING & VALIDATION', ha='center', va='center', 
            fontsize=12, fontweight='bold', color='#d32f2f')
    ax.text(2.5, 2.8, '• Pydantic schema validation', ha='center', va='center', 
            fontsize=10, color='#424242')
    ax.text(5, 2.8, '• SQLAlchemy constraint checks', ha='center', va='center', 
            fontsize=10, color='#424242')
    ax.text(7.5, 2.8, '• HTTP status codes', ha='center', va='center', 
            fontsize=10, color='#424242')
    ax.text(2.5, 2.4, '• Duplicate key prevention', ha='center', va='center', 
            fontsize=10, color='#424242')
    ax.text(5, 2.4, '• Data type validation', ha='center', va='center', 
            fontsize=10, color='#424242')
    ax.text(7.5, 2.4, '• Range validation (0-10 scores)', ha='center', va='center', 
            fontsize=10, color='#424242')
    
    plt.tight_layout()
    return fig

def main():
    """Tạo tất cả các diagram"""
    print("Tạo diagram kiến trúc backend...")
    
    # Tạo thư mục output
    import os
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Backend Architecture Diagram
    fig1 = create_backend_architecture_diagram()
    fig1.savefig(os.path.join(output_dir, "backend_architecture.png"), 
                 dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Đã tạo: backend_architecture.png")
    
    # 2. Database ERD Diagram
    fig2 = create_database_erd_diagram()
    fig2.savefig(os.path.join(output_dir, "database_erd.png"), 
                 dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Đã tạo: database_erd.png")
    
    # 3. API Flow Diagram
    fig3 = create_api_flow_diagram()
    fig3.savefig(os.path.join(output_dir, "api_flow.png"), 
                 dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Đã tạo: api_flow.png")
    
    print(f"\n🎉 Hoàn thành! Đã tạo 3 diagram trong thư mục {output_dir}/")
    print("📊 Các file đã tạo:")
    print("  - backend_architecture.png: Kiến trúc tổng thể backend")
    print("  - database_erd.png: Sơ đồ cơ sở dữ liệu")
    print("  - api_flow.png: Luồng xử lý API request")

if __name__ == "__main__":
    main()
