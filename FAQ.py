# Form implementation generated from reading ui file 'D:\Spydecat_Doancuoiky\Spydecat_K24406H\ui\FAQ.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow_FAQ(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1065, 810)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(80, 0, 881, 71))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(18)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.label.setFont(font)
        self.label.setStyleSheet("background-color: rgb(255, 85, 0);\n"
"font: 75 18pt \"Times New Roman\";\n"
"color: rgb(0, 0, 0);")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.groupBox = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(20, 80, 531, 681))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.groupBox.setFont(font)
        self.groupBox.setStyleSheet("background-color: rgb(1, 22, 158);\n"
"font: 75 16pt \"Times New Roman\";\n"
"color: rgb(255, 255, 255);")
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.listWidgetcauhoi = QtWidgets.QListWidget(parent=self.groupBox)
        self.listWidgetcauhoi.setObjectName("listWidgetcauhoi")
        self.listWidgetcauhoi.setStyleSheet("""
            QListWidget::item {
                padding: 5px;
                color: white;
            }
            QListWidget::item:selected {
                background-color: white;
                color: black;
                font-weight: bold;
            }
        """)
        self.verticalLayout.addWidget(self.listWidgetcauhoi)
        self.groupBox_2 = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(570, 80, 441, 681))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setStyleSheet("background-color: rgb(1, 22, 158);\n"
"color: rgb(255, 255, 255);\n"
"font: 16pt \"Times New Roman\";")
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelcautraloi = QtWidgets.QLabel(parent=self.groupBox_2)
        self.labelcautraloi.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.labelcautraloi.setText("")
        self.labelcautraloi.setObjectName("labelcautraloi")
        self.horizontalLayout.addWidget(self.labelcautraloi)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1065, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "FAQ"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">FAQ: Hỏi đáp chung về trường Đại học Kinh tế - Luật</span></p></body></html>"))
        self.groupBox.setTitle(_translate("MainWindow", "Câu hỏi thường gặp:"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Câu trả lời:"))
