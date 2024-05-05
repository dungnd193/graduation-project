from PyQt5.QtWidgets import * 
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import *
from PyQt5 import QtGui
import sys

import requests

class AddModelWindow(QWidget):
    model_added = pyqtSignal()
    def __init__(self, parent = None):
        """constructor to create a new window with charactersitis after create object from class window"""
        super().__init__()
        self.title = "Add new model"
        self.top = 100
        self.left = 600
        self.width = 400
        self.height = 650
        self.init_window()

    def init_window(self):
        """initialize Main IFD window"""
        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon(r"D:\dungnd\GraduationProject\Icons\icons8-cbs-512.ico")) #icon Pic File name
        self.setFixedSize(self.width , self.height)
        self.center_window()

        label_model_name = QLabel(self)
        label_model_name.move(20, 10)
        label_model_name.setText('Model name')
        label_model_name.setFont(QtGui.QFont("Microsoft YaHei UI Light", 16))
        label_model_name.setStyleSheet("color: black;")
        
        self.lineEdit_model_name = QLineEdit(self)
        self.lineEdit_model_name.setGeometry(20, 40, 360, 30)
        self.lineEdit_model_name.setPlaceholderText('Your model name')
        self.lineEdit_model_name.setStyleSheet("color: black; background-color: white; padding-left: 4px; padding-right: 4px")

        label_model_path = QLabel(self)
        label_model_path.move(20, 90)
        label_model_path.setText('Path to your model')
        label_model_path.setFont(QtGui.QFont("Microsoft YaHei UI Light", 16))
        label_model_path.setStyleSheet("color: black;")
        
        self.lineEdit_model_path = QLineEdit(self)
        self.lineEdit_model_path.setGeometry(20, 120, 360, 30)
        self.lineEdit_model_path.setPlaceholderText('Path to your model')
        self.lineEdit_model_path.setStyleSheet("color: black; background-color: white; padding-left: 4px; padding-right: 4px")
        
        label_model_acc = QLabel(self)
        label_model_acc.move(20, 170)
        label_model_acc.setText('Accuracy')
        label_model_acc.setFont(QtGui.QFont("Microsoft YaHei UI Light", 16))
        label_model_acc.setStyleSheet("color: black;")
        
        self.lineEdit_model_acc = QLineEdit(self)
        self.lineEdit_model_acc.setGeometry(20, 200, 360, 30)
        self.lineEdit_model_acc.setPlaceholderText('Type your model accuracy')
        self.lineEdit_model_acc.setStyleSheet("color: black; background-color: white; padding-left: 4px; padding-right: 4px")
        
        label_model_precision = QLabel(self)
        label_model_precision.move(20, 250)
        label_model_precision.setText('Precision')
        label_model_precision.setFont(QtGui.QFont("Microsoft YaHei UI Light", 16))
        label_model_precision.setStyleSheet("color: black;")
        
        self.lineEdit_model_precision = QLineEdit(self)
        self.lineEdit_model_precision.setGeometry(20, 280, 360, 30)
        self.lineEdit_model_precision.setPlaceholderText('Type your model precision')
        self.lineEdit_model_precision.setStyleSheet("color: black; background-color: white; padding-left: 4px; padding-right: 4px")
        
        label_model_recall = QLabel(self)
        label_model_recall.move(20, 330)
        label_model_recall.setText('Recall')
        label_model_recall.setFont(QtGui.QFont("Microsoft YaHei UI Light", 16))
        label_model_recall.setStyleSheet("color: black;")
        
        self.lineEdit_model_recall = QLineEdit(self)
        self.lineEdit_model_recall.setGeometry(20, 360, 360, 30)
        self.lineEdit_model_recall.setPlaceholderText('Type your model recall')
        self.lineEdit_model_recall.setStyleSheet("color: black; background-color: white; padding-left: 4px; padding-right: 4px")
        
        label_model_f1_score = QLabel(self)
        label_model_f1_score.move(20, 410)
        label_model_f1_score.setText('F1 Score')
        label_model_f1_score.setFont(QtGui.QFont("Microsoft YaHei UI Light", 16))
        label_model_f1_score.setStyleSheet("color: black;")
        
        self.lineEdit_model_f1_score = QLineEdit(self)
        self.lineEdit_model_f1_score.setGeometry(20, 440, 360, 30)
        self.lineEdit_model_f1_score.setPlaceholderText('Type your model F1 score')
        self.lineEdit_model_f1_score.setStyleSheet("color: black; background-color: white; padding-left: 4px; padding-right: 4px")
        
        label_model_version = QLabel(self)
        label_model_version.move(20, 490)
        label_model_version.setText('Version')
        label_model_version.setFont(QtGui.QFont("Microsoft YaHei UI Light", 16))
        label_model_version.setStyleSheet("color: black;")
        
        self.lineEdit_model_version = QLineEdit(self)
        self.lineEdit_model_version.setGeometry(20, 520, 360, 30)
        self.lineEdit_model_version.setPlaceholderText('Type your model version')
        self.lineEdit_model_version.setStyleSheet("color: black; background-color: white; padding-left: 4px; padding-right: 4px")

        self.save_btn = QPushButton("Save model", self)
        self.save_btn.setGeometry(QRect(20, 580, 360, 30))
        self.save_btn.setStyleSheet("background-color: #57a1f8; color: white; border: none; font-size: 16px")
        self.save_btn.clicked.connect(self.on_click)
        self.show()
    
    def center_window(self):
        screen_geometry = QApplication.desktop().screenGeometry()
        top = (screen_geometry.height() - self.height) // 2
        left = (screen_geometry.width() - self.width) // 2
        self.setGeometry(left, top, self.width, self.height)
        
    def on_click(self):
        model_name = self.lineEdit_model_name.text()
        model_path = self.lineEdit_model_path.text().replace("//","////")
        model_acc = self.lineEdit_model_acc.text()
        model_precision = self.lineEdit_model_precision.text()
        model_recall = self.lineEdit_model_recall.text()
        model_f1_score = self.lineEdit_model_f1_score.text()
        model_version = self.lineEdit_model_version.text()

        url = "http://localhost:8000/models/"
        body = {}
        body['name']=model_name
        body['path']=model_path
        body['accuracy']=model_acc
        body['precision']=model_precision
        body['recall']=model_recall
        body['f1_score']=model_f1_score
        body['version']=model_version
        response = requests.post(url, json=body)
        if response.status_code == 201:
            QMessageBox.information(self, "Success", "New model added successfully!")
            self.model_added.emit()
            self.close()
        else:
            print("Add new model error:", response.json())

class ModelManagementWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.title = "User Management"
        self.width = 860
        self.height = 500
        self.get_all_models()
        self.init_window()

    def init_window(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon(r"D:\dungnd\GraduationProject\Icons\icons8-cbs-512.ico"))
        self.setFixedSize(self.width, self.height)
        self.center_window()

        label_model_management = QLabel(self)
        label_model_management.setText('Model Management')
        label_model_management.setFont(QtGui.QFont("Microsoft YaHei UI Light", 24))
        label_model_management.setStyleSheet("color: #57a1f8; font-weight: bold")
        self.center_label(label_model_management, 10)


        table_frame = QFrame(self)
        table_frame.setGeometry(30, 120, self.width-30*2, self.height-100)

        self.tableWidget = QTableWidget(table_frame)
        self.tableWidget.setColumnCount(8)  
        self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem("Id"))
        self.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem("Model name"))
        self.tableWidget.setHorizontalHeaderItem(2, QTableWidgetItem("Accuracy"))
        self.tableWidget.setHorizontalHeaderItem(3, QTableWidgetItem("Precision"))
        self.tableWidget.setHorizontalHeaderItem(4, QTableWidgetItem("Recall"))
        self.tableWidget.setHorizontalHeaderItem(5, QTableWidgetItem("F1 Score"))
        self.tableWidget.setHorizontalHeaderItem(6, QTableWidgetItem("Version"))
        self.tableWidget.setHorizontalHeaderItem(7, QTableWidgetItem("Path"))

        # Set column widths to fit content and disable manual resizing
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setStyleSheet("background-color: white; color: black;")

        self.tableWidget.setFixedWidth(self.width-60)
        self.tableWidget.setFixedHeight(self.height-150)
        self.tableWidget.verticalHeader().setVisible(False)

        # Insert rows
        for model in self.models:
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, QTableWidgetItem("ID"+str(model['id'])))
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, QTableWidgetItem(model['name']))
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 2, QTableWidgetItem(str(model['accuracy'])))
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 3, QTableWidgetItem(str(model['precision'])))
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 4, QTableWidgetItem(str(model['recall'])))
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 5, QTableWidgetItem(str(model['f1_score'])))
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 6, QTableWidgetItem(model['version']))
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 7, QTableWidgetItem(model['path']))

        self.tableWidget.setStyleSheet(
            "QTableWidget { background-color: #ffffff; border: 1px solid #d3d3d3; }"
            "QHeaderView::section { background-color: #f2f2f2; border: none; }"
            "QTableWidget::item { padding: 5px; }"
            "QTableWidget::item:selected { background-color: #3ca355; }"
        )

        scrollbar = self.tableWidget.horizontalScrollBar()
        scrollbar.setStyleSheet(
            "QScrollBar:horizontal {"
            "    border: none;"
            "    background: #f2f2f2;"
            "    height: 15px;"
            "    margin: 0px 20px 0 20px;"
            "}"
            "QScrollBar::handle:horizontal {"
            "    background: #d3d3d3;"
            "    min-width: 20px;"
            "}"
            
            "QScrollBar::add-line:horizontal {"
            "    border: none;"
            "    background: #b3b3b3;"
            "    width: 20px;"
            "    subcontrol-position: right;"
            "    subcontrol-origin: margin;"
            "}"
            "QScrollBar::sub-line:horizontal {"
            "    border: none;"
            "    background: #b3b3b3;"
            "    width: 20px;"
            "    subcontrol-position: left;"
            "    subcontrol-origin: margin;"
            "}"
            "QScrollBar::right-arrow:horizontal, QScrollBar::left-arrow:horizontal {"
            "    background: none;"
            "}"
            "QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {"
            "    background: none;"
            "}"
        )


        self.search_btn = QPushButton("Search by model name", self)
        self.search_btn.setGeometry(QRect(30, 60, 180, 40))
        self.search_btn.setStyleSheet("background-color: #57a1f8; color: white; border: none; font-size: 16px")

        self.search_btn.clicked.connect(self.search_by_model_name)
        
        self.search_box = QLineEdit(self)
        self.search_box.setGeometry(QRect(230, 60, 465, 40))
        self.search_box.setStyleSheet("font: 75 12pt \"MS Shell Dlg 2\";\n"
                                 "background-color: white;\n"
                                 "color: black;\n"
                                 "padding-left: 10px; padding-right: 10px;")
        
        self.add_new_model_btn = QPushButton("Add new model", self)
        self.add_new_model_btn.setGeometry(QRect(712, 60, 120, 40))
        self.add_new_model_btn.setStyleSheet("background-color: #57a1f8; color: white; border: none; font-size: 16px")
        self.add_new_model_btn.clicked.connect(self.open_add_model_window)

        self.show()

    def center_label(self, label, y):
        label.adjustSize()
        label.move((self.width - label.width()) // 2, y)

    def center_window(self):
        screen_geometry = QApplication.desktop().screenGeometry()
        top = (screen_geometry.height() - self.height) // 2
        left = (screen_geometry.width() - self.width) // 2
        self.setGeometry(left, top, self.width, self.height)

    def get_all_models(self):
        url = "http://localhost:8000/models/"
        response = requests.get(url)
        if response.status_code == 200:
            self.models = response.json()
        else:
            print("Get all models error:", response.json())

    def open_add_model_window(self):
        self.add_model_window = AddModelWindow()
        self.add_model_window.model_added.connect(self.refresh_table_data)
        self.add_model_window.show()

    def refresh_table_data(self):
        self.tableWidget.setRowCount(0)
        self.get_all_models()

        # Insert rows with the latest model data
        for model in self.models:
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
            self.tableWidget.setItem(row_position, 0, QTableWidgetItem("ID" + str(model['id'])))
            self.tableWidget.setItem(row_position, 1, QTableWidgetItem(model['name']))
            self.tableWidget.setItem(row_position, 2, QTableWidgetItem(str(model['accuracy'])))
            self.tableWidget.setItem(row_position, 3, QTableWidgetItem(str(model['precision'])))
            self.tableWidget.setItem(row_position, 4, QTableWidgetItem(str(model['recall'])))
            self.tableWidget.setItem(row_position, 5, QTableWidgetItem(str(model['f1_score'])))
            self.tableWidget.setItem(row_position, 6, QTableWidgetItem(model['version']))
            self.tableWidget.setItem(row_position, 7, QTableWidgetItem(model['path']))

    def search_by_model_name(self):
        model_name = self.search_box.text()
        url = "http://localhost:8000/models/search/"
        params = {}
        params['name']=model_name
        response = requests.get(url, params=params)
        if response.status_code == 200:
            # Clear existing rows in the table
            self.tableWidget.setRowCount(0)
            
            # Insert rows for the searched users
            models = response.json()
            for model in models:
                row_position = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row_position)
                self.tableWidget.setItem(row_position, 0, QTableWidgetItem("ID" + str(model['id'])))
                self.tableWidget.setItem(row_position, 1, QTableWidgetItem(model['name']))
                self.tableWidget.setItem(row_position, 2, QTableWidgetItem(str(model['accuracy'])))
                self.tableWidget.setItem(row_position, 3, QTableWidgetItem(str(model['precision'])))
                self.tableWidget.setItem(row_position, 4, QTableWidgetItem(str(model['recall'])))
                self.tableWidget.setItem(row_position, 5, QTableWidgetItem(str(model['f1_score'])))
                self.tableWidget.setItem(row_position, 6, QTableWidgetItem(model['version']))
                self.tableWidget.setItem(row_position, 7, QTableWidgetItem(model['path']))
        else:
            print("Get all models error:", response.json())
if __name__ == "__main__":
    AppStart = QApplication(sys.argv)
    AppStart.setStyle('Fusion')
    window = ModelManagementWindow()
    sys.exit(AppStart.exec())
