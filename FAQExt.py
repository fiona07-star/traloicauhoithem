from PyQt6.QtWidgets import QListWidgetItem, QLabel, QListWidget
from Spydecat_K24406H.ui.FAQ import Ui_MainWindow_FAQ

class FAQExt(Ui_MainWindow_FAQ):
    def __init__(self):
        super().__init__()
        self.cauhoi = []  # Danh sách câu hỏi và câu trả lời

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.khoi_tao_du_lieu()
        self.listWidgetcauhoi.itemSelectionChanged.connect(self.hien_cau_tra_loi)

        # Đảm bảo QLabel có thể xuống dòng
        self.labelcautraloi.setWordWrap(True)

    def showWindow(self):
        self.MainWindow.show()

    def khoi_tao_du_lieu(self):
        """Khởi tạo danh sách câu hỏi và câu trả lời"""
        self.cauhoi = [
            ("Trường Đại học Kinh tế – Luật là trường công lập hay dân lập?",
             "Trường Đại học Kinh tế – Luật là đại học công lập và là đơn vị thành viên của Đại học Quốc gia TP.HCM"),
            ("Trường có hỗ trợ chỗ ở, KTX cho sinh viên không? Mức phí như thế nào?",
             "Là sinh viên hệ chính quy hay quốc tế đều được hỗ trợ vào ở KTX ĐHQG với chi phí rất sinh viên"),
            ("Trường có khu vực nhà thi đấu thể thao không?",
             "Nhà trường có khu tập luyện thể dục thể thao trang bị hiện đại theo tiêu chuẩn quốc tế. Đã đưa vào sử dụng từ ngày 06/2/2023 với tổng mức đầu tư gần 8 tỷ đồng bao gồm các hạng mục: sân bóng đá, bóng rổ, bóng chuyền, cầu lông, cùng các công trình phụ trợ khác. "),
            ("Trường có địa điểm tự học cho sinh viên không?",
             "Trường có bố trí không gian khu tự học thư viện, không gian ngoại ngữ và khởi nghiệp, khu tự học dưới sảnh tòa nhà điều hành học tập với tổng diện tích sàn khoảng 3.000 m2"),
            ("Học và thi tại trường đại học kinh tế luật có khó lắm ko?",
             "Tuỳ vào khả năng và nhận thức của mỗi người mà việc học và thi ở bậc đại học sẽ nhận thấy khó hay dễ."),
            ("Sinh viên tốt nghiệp trường có phải thi chứng chỉ ngoại ngữ quốc tế",
             "Các chứng chỉ quốc tế gợi ý (quy đổi tương đương) là IELTS, TOEIC, CAE, TOEFL IBT. Tùy theo hệ đào tạo mà chuẩn đầu ra yêu cầu năng lực ngoại ngữ khác nhau, nhưng tối thiểu là điểm 5.0 cho chứng chỉ IELTS (hoặc tương đương)."),
            ("Sinh viên ra trường có dễ kiếm được việc làm hay không?",
             "Trên 90% sinh viên ra Trường có việc làm, trên 98% cựu sinh viên hài lòng chất lượng đào tạo của Trường và trên 95% doanh nghiệp rất hài lòng về chất lượng sinh viên UEL."),
            ("Ngoài học phí, sinh viên còn phải đóng thêm các khoản phí nào nữa khi theo học tại trường?",
             "Một số khoản thu ngoài học phí như: Học giáo dục quốc phòng, học tiếng Anh tăng cường, bảo hiểm y tế, bảo hiểm tai nạn tự nguyện, …"),
            ("Học phí của Trường Đại học Kinh tế – Luật (UEL) như thế nào?", "Học phí dự kiến năm học 2024-2025 – Chương trình tiếng Việt: 27.5 triệu / năm học – Chương trình tiếng Anh: 57.6 triệu / năm học, Học phí Trường Đại học Kinh tế – Luật tăng theo lộ trình hàng năm từ 10 %đến 15 % "),
             ("Tổng số tín chỉ của các chương trình đào tạo của trường là bao nhiêu?", "130 tín chỉ. Trường hợp sinh viên học lại, học cải thiện, học song ngành ngoài chương trình đào tạo, tích lũy kiến thức thì học phí của các học phần này sẽ tính theo số tín chỉ học, chi tiết đơn giá của mỗi tín chỉ Phòng Tài chính sẽ thông báo vào mỗi học kỳ."),
            ("Trường Đại học Kinh tế – Luật (UEL) có chính sách hỗ trợ học phí cho sinh viên khó khăn không?","Đối với SV khó khăn, UEL có thực hiện các chính sách hỗ trợ tài chính – Miễn giảm học phí – Trợ cấp xã hội – Chính sách giáo dục dành cho SV dân tộc / khuyết tật thuộc hộ nghèo / cận nghèo – Vay vốn học tập từ Ngân hàng chính sách xã hội – Vay vốn ưu đãi học tập dành cho SV ĐHQG-HCM – Gia hạn học phí")]

        # Thêm câu hỏi vào listWidget
        for cau, _ in self.cauhoi:
            self.listWidgetcauhoi.addItem(QListWidgetItem(cau))

    def hien_cau_tra_loi(self):
        """Hiển thị câu trả lời khi chọn câu hỏi"""
        selected_items = self.listWidgetcauhoi.selectedItems()
        if not selected_items:
            return

        selected_question = selected_items[0].text()

        for question, answer in self.cauhoi:
            if question == selected_question:
                self.labelcautraloi.setText(answer)  # Hiển thị câu trả lời trong QLabel
                return
