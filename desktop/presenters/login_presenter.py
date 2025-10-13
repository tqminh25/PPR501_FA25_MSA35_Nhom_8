"""
Login Presenter - Điều khiển logic giữa View và Model
"""

import threading
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from views.login_view import ILoginView
    from models.login_model import LoginModel


class LoginPresenter:
    """Presenter điều khiển logic giữa View và Model"""
    
    def __init__(self, view: 'ILoginView', model: 'LoginModel'):
        self.view = view
        self.model = model
    
    def on_login_clicked(self):
        """Xử lý sự kiện đăng nhập"""
        # Lấy thông tin từ view
        username, password, remember = self.view.get_credentials()
        
        # Validate input
        is_valid, error_message = self.model.validate_credentials(username, password)
        if not is_valid:
            self.view.show_error(error_message)
            return
        
        # Hiển thị loading
        self.view.show_loading(True)
        
        # Gọi API (giả lập async)
        self._authenticate_async(username, password, remember)
    
    def _authenticate_async(self, username: str, password: str, remember: bool):
        """Giả lập async API call"""
        def authenticate():
            success, message = self.model.authenticate(username, password)
            
            # Update UI trong main thread
            self.view.after(0, lambda: self._handle_auth_result(success, message, username, remember))
        
        # Chạy trong background thread (giả lập)
        thread = threading.Thread(target=authenticate)
        thread.daemon = True
        thread.start()
    
    def _handle_auth_result(self, success: bool, message: str, username: str, remember: bool):
        """Xử lý kết quả authentication"""
        self.view.show_loading(False)
        
        if success:
            remember_text = self.model.check_remember_me(remember)
            self.view.show_success(username, remember_text)
        else:
            self.view.show_error(message)



