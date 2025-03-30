import os
import sys
import webbrowser
import pandas as pd
import plotly.express as px
import numpy as np

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QHeaderView, QCheckBox
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
        self.actionPie_chart.triggered.connect(self.create_pie_chart)

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

        #if not selected_rows:
            #QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn ít nhất một khách hàng để xóa!")
            #return

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

    def create_pie_chart(self):
        """Tạo biểu đồ thống kê giới tính và nhóm tuổi của khách hàng trên trình duyệt."""
        file_path = r"D:\Spydecat_Doancuoiky\Spydecat_K24406H\dataset\danhsach_visitors.xlsx"

        try:
            df = pd.read_excel(file_path)
            df['Giới tính'] = df['Giới tính'].str.strip().str.capitalize()
            df['Năm sinh'] = pd.to_numeric(df['Năm sinh'], errors='coerce')

            conditions = [
                df['Năm sinh'].between(2007, 2009, inclusive='both'),
                df['Năm sinh'].notna()
            ]
            choices = ['Cấp 3 (2007-2009)', 'Khác']
            df['Nhóm tuổi'] = np.select(conditions, choices, default='Không xác định')

            stats = df.groupby(['Giới tính', 'Nhóm tuổi'], observed=True).size().reset_index(name='Số lượng')
            stats['Tỷ lệ'] = (stats['Số lượng'] / stats['Số lượng'].sum() * 100).round(1)

            color_palette = {
                'Nam': '#4E79A7',
                'Nữ': '#F28E2B',
                'Cấp 3 (2007-2009)': '#59A14F',
                'Khác': '#B07AA1',
                'Không xác định': '#FF9DA7'
            }

            fig = px.sunburst(
                stats,
                path=['Giới tính', 'Nhóm tuổi'],
                values='Số lượng',
                title='<b>PHÂN BỔ KHÁCH ĐÃ TRUY CẬP THEO GIỚI TÍNH VÀ ĐỘ TUỔI</b>',
                color='Nhóm tuổi',
                color_discrete_map=color_palette,
                width=800,
                height=800,
                branchvalues='total'
            )

            fig.update_traces(
                textinfo="label+percent parent+value",
                texttemplate='<b>%{label}</b><br>%{percentParent:.1f}% (%{value})',
                marker=dict(line=dict(color='white', width=1))
            )

            # Lưu biểu đồ dưới dạng file HTML
            output_file = "temp_chart.html"
            fig.write_html(output_file)

            # Mở file HTML trong trình duyệt
            webbrowser.open("file://" + os.path.abspath(output_file))

        except Exception as e:
            print(f"Lỗi: {e}")



