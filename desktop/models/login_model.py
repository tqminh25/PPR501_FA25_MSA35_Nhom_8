"""
Login Model - Chứa business logic cho authentication
"""

import time
from typing import Tuple
from config.constants import API_BASE_URL, VALID_USERNAME, VALID_PASSWORD


class LoginModel:
    """Model chứa business logic và API calls cho login"""
    
    def __init__(self):
        self.api_base_url = API_BASE_URL
    
    def authenticate(self, username: str, password: str) -> Tuple[bool, str]:
        """
        Giả lập API call để xác thực
        Returns: (success: bool, message: str)
        """
        # Giả lập network delay
        time.sleep(0.5)
        
        # API simulation: chỉ usertest/123456 thành công
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            return True, "Đăng nhập thành công"
        else:
            return False, "Tên đăng nhập hoặc mật khẩu không đúng"
    
    def validate_credentials(self, username: str, password: str) -> Tuple[bool, str]:
        """Validate input trước khi gọi API"""
        if not username.strip():
            return False, "Vui lòng nhập tên đăng nhập"
        if not password:
            return False, "Vui lòng nhập mật khẩu"
        if len(username) < 3:
            return False, "Tên đăng nhập phải có ít nhất 3 ký tự"
        if len(password) < 6:
            return False, "Mật khẩu phải có ít nhất 6 ký tự"
        return True, ""
    
    def check_remember_me(self, remember: bool) -> str:
        """Xử lý logic ghi nhớ đăng nhập"""
        if remember:
            return " (đã ghi nhớ)"
        return ""



