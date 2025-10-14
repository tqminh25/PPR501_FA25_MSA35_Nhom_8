"""
Main entry point cho ứng dụng EduManager Pro
"""

import os
# Ẩn các thông báo IMK không cần thiết trên macOS
os.environ['PYTHONWARNINGS'] = 'ignore'

from models.login_model import LoginModel
from views.login_view import LoginView
from presenters.login_presenter import LoginPresenter


def main():
    """Main function khởi chạy ứng dụng"""
    # Tạo Model
    model = LoginModel()
    
    # Tạo View và Presenter
    view = LoginView()
    presenter = LoginPresenter(view, model)
    view.presenter = presenter
    
    # Chạy ứng dụng
    view.mainloop()


if __name__ == "__main__":
    main()

