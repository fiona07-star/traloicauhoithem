import os
import json
import hashlib
import base64
from dotenv import load_dotenv


class SecureDataConnector:
    def __init__(self):
        load_dotenv()
        self.PEPPER = os.getenv('SECRET_PEPPER', 'default_pepper_value')  # Pepper từ biến môi trường
        self.SALT_LENGTH = 16  # Độ dài salt ngẫu nhiên

        # Đường dẫn file
        self.file_cbnv = os.path.join("dataset", "cbnv_secure.json")

        # Tạo file nếu chưa tồn tại
        if not os.path.exists(self.file_cbnv):
            self._init_secure_file()

    def _generate_salt(self):
        """Tạo salt ngẫu nhiên"""
        return os.urandom(self.SALT_LENGTH).hex()

    def _enstrip_password(self, password: str, salt: str = None) -> dict:
        """
        Mã hóa mật khẩu (Enstrip)
        Trả về dict chứa salt và password đã băm
        """
        salt = salt or self._generate_salt()
        combined = f"{self.PEPPER}{password}{salt}".encode('utf-8')
        hashed = hashlib.pbkdf2_hmac('sha256', combined, bytes.fromhex(salt), 100000)
        return {
            'salt': salt,
            'hash': base64.b64encode(hashed).decode('utf-8')
        }

    def _destrip_password(self, password: str, salt: str, stored_hash: str) -> bool:
        """Xác minh mật khẩu (Destrip)"""
        if not salt or not stored_hash:
            return False
        combined = f"{self.PEPPER}{password}{salt}".encode('utf-8')
        hashed = hashlib.pbkdf2_hmac('sha256', combined, bytes.fromhex(salt), 100000)
        return base64.b64encode(hashed).decode('utf-8') == stored_hash

    def _enstrip_email(self, email: str) -> str:
        """Mã hóa email (Enstrip)"""
        return base64.b64encode(email.encode('utf-8')).decode('utf-8')

    def _destrip_email(self, encoded_email: str) -> str:
        """Giải mã email (Destrip)"""
        return base64.b64decode(encoded_email.encode('utf-8')).decode('utf-8')

    def _init_secure_file(self):
        """Khởi tạo file với dữ liệu mẫu đã mã hóa"""
        sample_data = [
            {
                "ma_nguoi_dung": "C1",
                "ten": "Au Tu Ngoc",
                "email": self._enstrip_email("atn@gmail.com"),
                "mat_khau": self._enstrip_password("123"),
                "phong_ban": "Phòng CTSV"
            }
        ]
        with open(self.file_cbnv, 'w') as f:
            json.dump(sample_data, f, indent=4)

    def login(self, email: str, password: str) -> dict:
        """Xác thực đăng nhập an toàn"""
        try:
            with open(self.file_cbnv, 'r') as f:
                users = json.load(f)

            encoded_email = self._enstrip_email(email)
            user = next((u for u in users if u['email'] == encoded_email), None)

            if not user or 'mat_khau' not in user:
                return None

            if self._destrip_password(password, user['mat_khau']['salt'], user['mat_khau']['hash']):
                return {
                    'ma_nguoi_dung': user['ma_nguoi_dung'],
                    'ten': user['ten'],
                    'email': email,  # Trả về email gốc
                    'phong_ban': user['phong_ban']
                }
                return None
        except Exception as e:
            print(f"Lỗi đăng nhập: {str(e)}")
            return None

    def add_user(self, user_data: dict):
        """Thêm người dùng mới với dữ liệu đã mã hóa"""
        try:
            with open(self.file_cbnv, 'r+') as f:
                users = json.load(f)
                user_data['email'] = self._enstrip_email(user_data['email'])
                user_data['mat_khau'] = self._enstrip_password(user_data['mat_khau'])
                users.append(user_data)
                f.seek(0)
                json.dump(users, f, indent=4)
                f.truncate()
            return True
        except Exception as e:
            print(f"Lỗi thêm người dùng: {str(e)}")
            return False