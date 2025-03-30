import os
import webbrowser

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QListWidgetItem, QTableWidgetItem, QMessageBox, QApplication, QHeaderView, QMainWindow

from Spydecat_K24406H.libs.Dataconnector import DataConnector
from Spydecat_K24406H.libs.ExportTool import ExportTool
from Spydecat_K24406H.ui.FAQExt import FAQExt
from Spydecat_K24406H.ui.MainWindowKhach import Ui_MainWindow_khach_xem_diem


class MainWindowKhachExt(Ui_MainWindow_khach_xem_diem):
    def __init__(self):
            self.dc = DataConnector()
            self.all_nganh_hoc = ExportTool().import_bang_diem_from_excel("../dataset/Bangdiem.xlsx")
            self.nganh_hoc = self.all_nganh_hoc  # Khởi tạo `self.nganh_hoc` trước khi sử dụng
            self.chuyen_nganh = self.dc.get_chuyen_nganh_by_nganh_hoc(
            self.nganh_hoc[0].ten_nganh if self.nganh_hoc else "")
            self.selected_nganh = None

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow=MainWindow
        self.setupSignalAndSlot()  # Đảm bảo các nút được kết nối
        self.show_chuyen_nganh_gui()
        self.show_nganh_hoc_gui()


    def showWindow(self):
        """Hiển thị cửa sổ"""
        self.MainWindow.show()

    def setupSignalAndSlot(self):
        """Kết nối sự kiện với các phương thức xử lý"""
        self.listWidgetNganh.itemSelectionChanged.connect(self.filter_nganh)
        self.tableWidget.itemSelectionChanged.connect(self.show_detail_nganh)
        self.pushButtonThoat.clicked.connect(self.process_exit)
        self.pushButtonTimhieuthem.clicked.connect(self.tim_hieu_them)
        self.pushButtonLienhetuvan.clicked.connect(self.lien_he_tu_van)
        self.actionHint.triggered.connect(self.thong_tin_chi_tiet)
    def show_chuyen_nganh_gui(self):
        self.listWidgetNganh.clear()
        self.listWidgetNganh.addItem("Tất cả ngành học")

        unique_nganh = set(nganh.ten_nganh for nganh in self.all_nganh_hoc)
        print("Danh sách ngành học:", unique_nganh)  # Kiểm tra dữ liệu có tồn tại không

        for ten_nganh in unique_nganh:
            self.listWidgetNganh.addItem(QListWidgetItem(ten_nganh))

    def show_nganh_hoc_gui(self):
        """Hiển thị danh sách ngành học lên tableWidget"""
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(len(self.nganh_hoc))

        # 🔹 Tự động điều chỉnh kích thước cột theo nội dung
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        for row, nganh in enumerate(self.nganh_hoc):
            col_ten_nganh = QTableWidgetItem(nganh.ten_nganh)
            col_chuyen_nganh = QTableWidgetItem(nganh.chuyen_nganh)
            col_ma_tuyen_sinh = QTableWidgetItem(nganh.ma_tuyen_sinh)
            col_chi_tieu = QTableWidgetItem(str(nganh.chi_tieu))
            col_pt1a = QTableWidgetItem(str(nganh.phuong_thuc_1a))
            col_pt1b = QTableWidgetItem(str(nganh.phuong_thuc_1b))
            col_pt2 = QTableWidgetItem(str(nganh.phuong_thuc_2))
            col_pt3 = QTableWidgetItem(str(nganh.phuong_thuc_3))

            items = [col_ten_nganh, col_chuyen_nganh, col_ma_tuyen_sinh, col_chi_tieu, col_pt1a, col_pt1b, col_pt2,
                     col_pt3]

            for col, item in enumerate(items):
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  # 🔹 Căn giữa nội dung
                self.tableWidget.setItem(row, col, item)

        # 🔹 Tự động điều chỉnh chiều cao hàng theo nội dung
        self.tableWidget.resizeRowsToContents()
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        print("TableWidget đã được cập nhật với dữ liệu mới.")
    def filter_nganh(self):
        """Lọc danh sách ngành học dựa vào lựa chọn trên listWidget"""
        current_item = self.listWidgetNganh.currentItem()
        if not current_item:
            return

        ten_nganh = current_item.text()
        print(f"Ngành được chọn: {ten_nganh}")

        if ten_nganh == "Tất cả ngành học":
            self.nganh_hoc = self.all_nganh_hoc
        else:
            self.nganh_hoc = [nganh for nganh in self.all_nganh_hoc if nganh.ten_nganh == ten_nganh]

        self.show_nganh_hoc_gui()

    def show_detail_nganh(self):
        """Hiển thị thông tin chi tiết của ngành học được chọn"""
        index = self.tableWidget.currentRow()
        if index < 0 or index >= len(self.nganh_hoc):
            return

        nganh = self.nganh_hoc[index]
        self.lineEditNganhtuyensinh.setText(nganh.ten_nganh)
        self.lineEditChuyennganh.setText(nganh.chuyen_nganh)
        self.lineEditMatuyensinh.setText(nganh.ma_tuyen_sinh)
        self.lineEditChitieu.setText(str(nganh.chi_tieu))
        self.lineEditPT1A.setText(str(nganh.phuong_thuc_1a))
        self.lineEditPT1B.setText(str(nganh.phuong_thuc_1b))
        self.lineEditPT2.setText(str(nganh.phuong_thuc_2))
        self.lineEditPT3.setText(str(nganh.phuong_thuc_3))



    def process_exit(self):
        """Xác nhận và thoát chương trình"""
        msgbox = QMessageBox(self.MainWindow)
        msgbox.setText("Bạn có chắc muốn thoát không?")
        msgbox.setWindowTitle("Xác nhận thoát")
        msgbox.setIcon(QMessageBox.Icon.Warning)
        buttons = QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        msgbox.setStandardButtons(buttons)
        if msgbox.exec() == QMessageBox.StandardButton.Yes:
            QApplication.quit()

    def tim_hieu_them(self):
        """Mở trang web tìm hiểu thêm"""
        webbrowser.open("https://tuyensinh.uel.edu.vn/dao-tao/dai-hoc-chinh-quy/")

    def lien_he_tu_van(self):
        # Nếu đã nhập đủ, chuyển qua MainWindowKhachExt
        self.MainWindow.hide()  # Ẩn cửa sổ đăng nhập

        # Tạo cửa sổ mới
        self.main_window = QMainWindow()
        self.new_window = FAQExt()  # Không truyền tham số
        self.new_window.setupUi(self.main_window)
        self.main_window.show()
    def thong_tin_chi_tiet(self):
        file_hint = "HINT.pdf"
        current_path = os.getcwd()
        file_hint = f"{current_path}/../dataset/{file_hint}"
        webbrowser.open_new(file_hint)