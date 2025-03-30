from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow, QTableWidgetItem, QMessageBox, QHeaderView, QTableWidget, QCheckBox, QWidget, QHBoxLayout
)

from Spydecat_K24406H.libs.Dataconnector import DataConnector
from Spydecat_K24406H.libs.ExportTool import ExportTool
from Spydecat_K24406H.ui.MainWindowDanhsach import Ui_MainWindow_danh_sach


class MainWindowDanhSachExt(QMainWindow, Ui_MainWindow_danh_sach):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        self.dc = DataConnector()
        self.khach = self.dc.get_all_khach()
        self.parent = parent  # Lưu cửa sổ gốc

        self.setupSignalAndSlot()
        self.setupTable()
        self.load_data_to_table()

    def setupSignalAndSlot(self):
        self.actionExport_excel.triggered.connect(self.export_to_excel)
        self.actionReturn.triggered.connect(self.return_mainwindow)
        self.actionDelete_visitors.triggered.connect(self.delete_selected_customers)

    def setupTable(self):
        """Thiết lập bảng với 7 cột, cột cuối chứa checkbox."""
        self.tableWidgetDanhsach.setColumnCount(7)
        self.tableWidgetDanhsach.setHorizontalHeaderLabels([
            "Mã khách", "Tên", "SĐT", "Email", "Giới tính", "Năm sinh", "Chọn"
        ])
        header = self.tableWidgetDanhsach.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def add_checkbox_to_row(self, row):


        """Thêm checkbox vào cột cuối cùng của hàng."""
        checkbox = QCheckBox()
        checkbox.setStyleSheet("margin-left:50%;")  # Căn giữa checkbox
        self.tableWidgetDanhsach.setCellWidget(row, 6, checkbox)

    def delete_selected_customers(self):
        """Xóa khách hàng đã được tick checkbox."""
        selected_rows = []
        for row in range(self.tableWidgetDanhsach.rowCount()):
            cell_widget = self.tableWidgetDanhsach.cellWidget(row, 6)
            if cell_widget:
                checkbox = cell_widget.findChild(QCheckBox)
                if checkbox and checkbox.isChecked():
                    selected_rows.append(row)

        if not selected_rows:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn ít nhất một khách hàng để xóa!")
            return

        reply = QMessageBox.question(
            self, "Xác nhận", "Bạn có chắc chắn muốn xóa khách hàng đã chọn?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.No:
            return

        # Xóa các dòng đã chọn (xóa từ dưới lên để không bị lỗi index)
        for row in sorted(selected_rows, reverse=True):
            self.tableWidgetDanhsach.removeRow(row)

        QMessageBox.information(self, "Thông báo", "Đã xóa khách hàng thành công!")

    def load_data_to_table(self):
        """Hiển thị danh sách khách với checkbox chọn để xóa."""
        self.khach = self.dc.get_all_khach()
        self.tableWidgetDanhsach.clearContents()
        self.tableWidgetDanhsach.setRowCount(len(self.khach))

        for row, visitor in enumerate(self.khach):
            gioi_tinh = "Nam" if visitor.gioi_tinh in ["Nam", True] else "Nữ"

            items = [
                QTableWidgetItem(str(visitor.ma_nguoi_dung)),
                QTableWidgetItem(visitor.ten),
                QTableWidgetItem(str(visitor.sdt)),
                QTableWidgetItem(visitor.email),
                QTableWidgetItem(gioi_tinh),
                QTableWidgetItem(str(visitor.nam_sinh))
            ]

            for col, item in enumerate(items):
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tableWidgetDanhsach.setItem(row, col, item)

            self.add_checkbox_to_row(row)  # Thêm checkbox vào hàng

    def export_to_excel(self):
        """Xuất danh sách khách ra file Excel."""
        filename = "../dataset/danhsach_visitors.xlsx"
        extool = ExportTool()
        extool.export_danhsach_khach_to_excel(filename, self.khach)
        QMessageBox.information(self, "Thông báo", "Đã Export Excel thành công")

    def return_mainwindow(self):
        """Quay về cửa sổ chính."""
        if self.parent:
            self.parent.show()
        self.close()
