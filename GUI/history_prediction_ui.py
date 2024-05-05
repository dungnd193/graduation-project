from PyQt5.QtWidgets import * 
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import *
from PyQt5 import QtGui
import sys
import requests
import argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument('--role', type=str,  help='User role', required=True)
parser.add_argument('--user_id', type=str,  help='User id', required=True)
role_id = int(parser.parse_args().role)
user_id = parser.parse_args().user_id

ADMIN = 1
USER = 2



class HistoryPredictionWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.title = "History prediction"
        self.width = 860
        self.height = 500
        if role_id == ADMIN:
            self.get_all_hist()
        if role_id == USER:
            self.get_hist_by_user_id(user_id)
        self.init_window()

    def init_window(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon(r"D:\dungnd\GraduationProject\Icons\icons8-cbs-512.ico"))
        self.setFixedSize(self.width, self.height)
        self.center_window()
        
        label_history_prediction = QLabel(self)
        label_history_prediction.setText('History prediction')
        label_history_prediction.setFont(QtGui.QFont("Microsoft YaHei UI Light", 24))
        label_history_prediction.setStyleSheet("color: #57a1f8; font-weight: bold")
        self.center_label(label_history_prediction, 10)

        table_frame = QFrame(self)
        table_frame.setGeometry(30, 120-60, self.width-60, self.height-150+60)

        self.tableWidget = QTableWidget(table_frame)
        self.tableWidget.setColumnCount(7)  
        self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem("Id"))
        self.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem("User Id"))
        self.tableWidget.setHorizontalHeaderItem(2, QTableWidgetItem("Model Id"))
        self.tableWidget.setHorizontalHeaderItem(3, QTableWidgetItem("Input Image Path"))
        self.tableWidget.setHorizontalHeaderItem(4, QTableWidgetItem("Output Image Path"))
        self.tableWidget.setHorizontalHeaderItem(5, QTableWidgetItem("Label"))
        self.tableWidget.setHorizontalHeaderItem(6, QTableWidgetItem("Accuracy"))

        # Set column widths to fit content and disable manual resizing
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  
        header.setStyleSheet("background-color: white; color: black;")

        self.tableWidget.setFixedWidth(self.width-60)
        self.tableWidget.setFixedHeight(self.height-150+60)
        self.tableWidget.verticalHeader().setVisible(False)
        # self.tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Insert rows
        for history in self.history:
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, QTableWidgetItem("ID"+str(history['id'])))
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, QTableWidgetItem(str(history['user_id'])))
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 2, QTableWidgetItem(str(history['model_id'])))
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 3, QTableWidgetItem(str(history['input_img_path'])))
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 4, QTableWidgetItem(str(history['output_img_path'])))
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 5, QTableWidgetItem(str(history['label'])))
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 6, QTableWidgetItem(str(history['accuracy'])))

        self.tableWidget.setStyleSheet(
            "QTableWidget { background-color: #ffffff; border: 1px solid #d3d3d3; }"
            "QHeaderView::section { background-color: #f2f2f2; border: none; }"
            "QTableWidget::item { padding: 5px; }"
            "QTableWidget::item:selected { background-color: #3ca355; }"
        )


        # self.search_btn = QPushButton("Search by path", self)
        # self.search_btn.setGeometry(QRect(30, 60, 180, 40))
        # self.search_btn.setStyleSheet("background-color: #57a1f8; color: white; border: none; font-size: 16px")
        # self.search_btn.clicked.connect(self.search_by_username)
        
        # self.search_box = QLineEdit(self)
        # self.search_box.setGeometry(QRect(230, 60, 600, 41))
        # self.search_box.setMinimumWidth(540)
        # self.search_box.setMinimumHeight(40)
        # self.search_box.setStyleSheet("font: 75 12pt \"MS Shell Dlg 2\";\n"
        #                          "background-color: white;\n"
        #                          "color: black;\n"
        #                          "padding-left: 10px; padding-right: 10px;")

        self.show()

    def center_label(self, label, y):
        label.adjustSize()
        label.move((self.width - label.width()) // 2, y)

    def center_window(self):
        screen_geometry = QApplication.desktop().screenGeometry()
        top = (screen_geometry.height() - self.height) // 2
        left = (screen_geometry.width() - self.width) // 2
        self.setGeometry(left, top, self.width, self.height)

    def get_all_hist(self):
        url = "http://localhost:8000/history/"
        response = requests.get(url)
        if response.status_code == 200:
            self.history = response.json()
        else:
            print("Get all history error:", response.json())

    def get_hist_by_user_id(self, user_id):
        url = "http://localhost:8000/history/" + str(user_id)
        response = requests.get(url)
        if response.status_code == 200:
            self.history = response.json()
        else:
            print("Get all history error:", response.json())

if __name__ == "__main__":
    AppStart = QApplication(sys.argv)
    AppStart.setStyle('Fusion')
    window = HistoryPredictionWindow()
    sys.exit(AppStart.exec())
