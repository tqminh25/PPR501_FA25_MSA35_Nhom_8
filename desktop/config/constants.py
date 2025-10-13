"""
Constants và cấu hình cho ứng dụng
"""

# API Configuration
API_BASE_URL = "http://127.0.0.1:8000"
API_TIMEOUT = 15  # seconds, align with desktop usage

# Authentication
VALID_USERNAME = "usertest"
VALID_PASSWORD = "123456"  # Updated password

# Window Configuration
MIN_WINDOW_WIDTH = 400
MIN_WINDOW_HEIGHT = 300
MIN_APP_WIDTH = 1000
MIN_APP_HEIGHT = 600

# Layout Configuration
HEADER_HEIGHT = 120  # pixels
SIDEBAR_WIDTH_PERCENT = 0.3  # 30% of window width
SIDEBAR_COLLAPSED_WIDTH = 60  # pixels when collapsed
SIDEBAR_EXPANDED_WIDTH_PERCENT = 0.25  # 25% when expanded
CONTENT_PADDING = 10

# Colors
COLORS = {
    'primary': '#4f46e5',
    'primary_hover': '#4338ca',
    'secondary': '#10b981',
    'background': 'white',
    'card_bg': 'white',
    'text_primary': '#2c3e50',
    'text_secondary': '#64748b',
    'border': '#e2e8f0',
    'success': '#10b981',
    'error': '#ef4444',
    'warning': '#f59e0b',
    'accent': '#06b6d4',
    'light_blue': '#dbeafe',
    'light_green': '#dcfce7',
    'light_purple': '#ede9fe'
}

# Fonts
FONTS = {
    'default': ('Helvetica', 12),
    'title': ('Helvetica', 16, 'bold'),
    'header': ('Helvetica', 14, 'bold'),
    'menu': ('Helvetica', 11),
    'content': ('Helvetica', 14)
}

# Menu Items
MENU_ITEMS = [
    ("📊", "Dashboard", "dashboard"),
    ("👥", "Quản lý học sinh", "students"),
    ("📝", "Quản lý điểm", "grades"),
    ("📚", "Quản lý lớp học", "classes"),
    ("📋", "Báo cáo", "reports"),
    ("🚪", "Đăng xuất", "logout"),
]
