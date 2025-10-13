# EduManager Pro - MVP Architecture

Ứng dụng quản lý giáo dục được xây dựng theo kiến trúc MVP (Model-View-Presenter) với Python và Tkinter.

## 📁 Cấu trúc thư mục

```
Python Study/
├── main.py                 # Entry point
├── README.md              # Hướng dẫn
├── models/                # Business Logic Layer
│   ├── __init__.py
│   └── login_model.py     # Login business logic
├── views/                 # Presentation Layer
│   ├── __init__.py
│   ├── login_view.py      # Login UI
│   └── app_view.py        # Main App UI
├── presenters/            # Control Layer
│   ├── __init__.py
│   └── login_presenter.py # Login control logic
├── config/                # Configuration
│   ├── __init__.py
│   ├── constants.py       # Constants và config
│   └── styles.py          # UI styles
└── utils/                 # Utilities
    ├── __init__.py
    └── window_utils.py    # Window utilities
```

## 🏗️ Kiến trúc MVP

### Model Layer (`models/`)
- **Chức năng**: Chứa business logic và data access
- **Responsibility**: Xử lý dữ liệu, API calls, validation
- **Files**: `login_model.py`

### View Layer (`views/`)
- **Chức năng**: UI components và user interface
- **Responsibility**: Hiển thị dữ liệu, nhận input từ user
- **Files**: `login_view.py`, `app_view.py`

### Presenter Layer (`presenters/`)
- **Chức năng**: Điều khiển logic giữa Model và View
- **Responsibility**: Xử lý events, điều phối data flow
- **Files**: `login_presenter.py`

## 🚀 Cách chạy

```bash
python main.py
```

## 🔐 Đăng nhập

- **Username**: `usertest`
- **Password**: `123456`

## 📋 Tính năng

### Login Screen
- ✅ Form đăng nhập với validation
- ✅ Show/hide password
- ✅ Remember me checkbox
- ✅ Loading state
- ✅ Error handling

### Main App
- ✅ Header với thông tin user
- ✅ Sidebar navigation
- ✅ Content area responsive
- ✅ Logout functionality

## 🎨 UI Features

- ✅ White background theme
- ✅ Responsive layout
- ✅ Modern design
- ✅ Cross-platform compatibility

## 👥 Làm việc nhóm

### Thêm tính năng mới:
1. **Model**: Thêm business logic vào `models/`
2. **View**: Tạo UI components trong `views/`
3. **Presenter**: Điều khiển logic trong `presenters/`
4. **Config**: Cập nhật constants trong `config/`

### Ví dụ thêm trang mới:
```python
# 1. Thêm vào constants.py
MENU_ITEMS.append(("📊", "Tên trang", "page_name"))

# 2. Thêm method trong app_view.py
def _show_page_name(self):
    # UI implementation
    pass

# 3. Cập nhật navigation trong _navigate_to_page()
```

## 🔧 Development

### Dependencies
- Python 3.7+
- tkinter (built-in)
- typing (built-in)

### Code Style
- Follow PEP 8
- Type hints
- Docstrings
- Separation of concerns

## 📝 Notes

- Sử dụng MVP pattern để tách biệt concerns
- Dễ dàng test từng component riêng biệt
- Scalable architecture cho team development
- Clean code và maintainable



