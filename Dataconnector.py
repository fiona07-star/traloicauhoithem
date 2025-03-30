import os

from Spydecat_K24406H.libs.JsonFileFactory import JsonFileFactory
from Spydecat_K24406H.libs.SecureDataconnector import SecureDataConnector
from Spydecat_K24406H.models.CBNV import Canbo
from Spydecat_K24406H.models.Khach import Khach
from Spydecat_K24406H.models.Nganh_hoc import Nganh_hoc


# Import mã hóa


class DataConnector:
    def __init__(self):
        """ Khởi tạo đối tượng và đặt đường dẫn file JSON """
        self.json_factory = JsonFileFactory()
        self.secure = SecureDataConnector()  # Thêm đối tượng bảo mật
        self.file_cbnv = os.path.join("..", "dataset", "cbnv.json")
        self.file_khach = os.path.join("..", "dataset", "khach.json")
        self.file_nganh_hoc = os.path.join("..", "dataset", "nganh_hoc.json")

    def get_all_cbnv(self):
        """ Đọc danh sách cán bộ từ file JSON """
        return self.json_factory.read_data(self.file_cbnv, Canbo)

    def login(self, email, password):
        """ Kiểm tra đăng nhập với mã hóa """
        cbnv_list = self.get_all_cbnv()

        for cb in cbnv_list:
            if self.secure._destrip_email(cb.email) == email:
                # Giải mã email rồi so sánh, sau đó kiểm tra mật khẩu
                if self.secure._destrip_password(password, cb.mat_khau['salt'], cb.mat_khau['hash']):
                    return cb  # Đăng nhập thành công
        return None  # Sai email hoặc mật khẩu

    def save_new_cbnv(self, cbnv):
        """ Thêm CBNV mới với mật khẩu mã hóa """
        all_cbnv = self.get_all_cbnv()

        # Mã hóa email và mật khẩu
        cbnv.email = self.secure._enstrip_email(cbnv.email)
        cbnv.mat_khau = self.secure._enstrip_password(cbnv.mat_khau)

        all_cbnv.append(cbnv)
        self.json_factory.write_data(all_cbnv, self.file_cbnv)

    def get_all_khach(self):
        """ Đọc danh sách khách từ file JSON """
        return self.json_factory.read_data(self.file_khach, Khach)

    def get_all_nganh_hoc(self):
        """ Đọc danh sách ngành học từ file JSON """
        return self.json_factory.read_data(self.file_nganh_hoc, Nganh_hoc)