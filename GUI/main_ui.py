from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import *
from PyQt5 import QtGui
import requests
from user_management_ui import UserManagementWindow
from subprocess import call
import sys
import argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument('--role', type=str,  help='User role', required=True)
parser.add_argument('--user_id', type=str,  help='User id', required=True)
role_id = int(parser.parse_args().role)
user_id = parser.parse_args().user_id

ADMIN = 1
USER = 2

print('role: ADMIN' if role_id==ADMIN else 'role: USER')


class UpdateUserInfoWindow(QWidget):
    def __init__(self, parent = None):
        """constructor to create a new window with charactersitis after create object from class window"""
        super().__init__()
        self.title = "Update user information"
        self.width = 400
        self.height = 450
        self.get_user_by_id(user_id)
        self.init_window()

    
    def get_user_by_id(self, user_id):
        url = "http://localhost:8000/users/"+user_id
        params = {}
        params['user_id']=int(user_id)
        response = requests.get(url, params=params)
        if response.status_code == 200:
            self.user = response.json()
        else:
            print("Get all users error:", response.json())


    def init_window(self):
        """initialize Main IFD window"""
        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon(r"D:\dungnd\GraduationProject\Icons\icons8-cbs-512.ico")) #icon Pic File name
        self.setFixedSize(self.width , self.height)
        self.center_window()

        label_username = QLabel(self)
        label_username.move(20, 10)
        label_username.setText('Username')
        label_username.setFont(QtGui.QFont("Microsoft YaHei UI Light", 16))
        label_username.setStyleSheet("color: black;")
        
        self.lineEdit_username = QLineEdit(self)
        self.lineEdit_username.setGeometry(20, 40, 360, 30)
        self.lineEdit_username.setPlaceholderText('Your username')
        self.lineEdit_username.setStyleSheet("color: black; background-color: white; padding-left: 4px; padding-right: 4px")
        self.lineEdit_username.setText(self.user['username'])
        self.lineEdit_username.setReadOnly(True) 

        label_password = QLabel(self)
        label_password.move(20, 90)
        label_password.setText('Password')
        label_password.setFont(QtGui.QFont("Microsoft YaHei UI Light", 16))
        label_password.setStyleSheet("color: black;")
        
        self.lineEdit_password = QLineEdit(self)
        self.lineEdit_password.setGeometry(20, 120, 360, 30)
        self.lineEdit_password.setPlaceholderText('Your password')
        self.lineEdit_password.setStyleSheet("color: black; background-color: white; padding-left: 4px; padding-right: 4px")
        self.lineEdit_password.setEchoMode(QLineEdit.Password)
        
        label_email = QLabel(self)
        label_email.move(20, 170)
        label_email.setText('Email')
        label_email.setFont(QtGui.QFont("Microsoft YaHei UI Light", 16))
        label_email.setStyleSheet("color: black;")
        
        self.lineEdit_email = QLineEdit(self)
        self.lineEdit_email.setGeometry(20, 200, 360, 30)
        self.lineEdit_email.setPlaceholderText('Your email')
        self.lineEdit_email.setStyleSheet("color: black; background-color: white; padding-left: 4px; padding-right: 4px")
        self.lineEdit_email.setText(self.user['email'])
        
        label_phone_number = QLabel(self)
        label_phone_number.move(20, 250)
        label_phone_number.setText('Phone Number')
        label_phone_number.setFont(QtGui.QFont("Microsoft YaHei UI Light", 16))
        label_phone_number.setStyleSheet("color: black;")
        
        self.lineEdit_phone_number = QLineEdit(self)
        self.lineEdit_phone_number.setGeometry(20, 280, 360, 30)
        self.lineEdit_phone_number.setPlaceholderText('Your phone number')
        self.lineEdit_phone_number.setStyleSheet("color: black; background-color: white; padding-left: 4px; padding-right: 4px")
        self.lineEdit_phone_number.setText(self.user['phone_number'])
        
        self.save_btn = QPushButton("Save my information", self)
        self.save_btn.setGeometry(QRect(20, 400, 360, 30))
        self.save_btn.setStyleSheet("background-color: #57a1f8; color: white; border: none; font-size: 16px")
        self.save_btn.clicked.connect(self.on_click)
        self.show()
    
    def center_window(self):
        screen_geometry = QApplication.desktop().screenGeometry()
        top = (screen_geometry.height() - self.height) // 2
        left = (screen_geometry.width() - self.width) // 2
        self.setGeometry(left, top, self.width, self.height)
        
    def on_click(self):
        url = "http://localhost:8000/users/"+str(self.user['id'])
        password = self.lineEdit_password.text()
        email = self.lineEdit_email.text()
        phone_number = self.lineEdit_phone_number.text()

        if password == "" or email == "" or phone_number == "":
            QMessageBox.warning(self, "Warning", "Please fill in all fields.")
        else:
            self.user['password'] = password
            self.user['email'] = email
            self.user['phone_number'] = phone_number
                
            response = requests.put(url, json=self.user)
            if response.status_code == 200:
                self.close()
                QMessageBox.information(self, "Success", "User information updated successfully!")
            else:
                print("Update user infor error:", response.json())


class MainWindow(QWidget):
    def __init__(self, parent = None):
        """constructor to create a new window with charactersitis after create object from class window"""
        super().__init__()
        self.title = "Dashboard"
        self.top = 50
        self.left = 350
        self.width = 400
        self.height = 550
        self.init_window()

    def init_window(self):
        """initialize Main IFD window"""

        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon(r"D:\dungnd\GraduationProject\Icons\icons8-cbs-512.ico")) #icon Pic File name
        self.setFixedSize(self.width , self.height)
        self.center_window()

        label_dashboard = QLabel(self)
        # label_dashboard.move(130, 30)
        label_dashboard.setText('Dashboard')
        label_dashboard.setFont(QtGui.QFont("Microsoft YaHei UI Light", 24))
        label_dashboard.setStyleSheet("color: #57a1f8; font-weight: bold")
        label_dashboard.setAlignment(Qt.AlignHCenter)
        self.center_label(label_dashboard, 30)

        pixmap = QPixmap(r"D:\dungnd\GraduationProject\Icons\bg.webp")
        self.label = QLabel(self)
        self.label.setPixmap(pixmap)
        self.label.resize(int(800//2.3), int(480//2.3))
        self.label.move(26, 90)
        self.label.setPixmap(pixmap.scaled(self.label.size(), Qt.IgnoreAspectRatio))
        self.label.show()

        if role_id == ADMIN:
            user_management_btn = QPushButton('User Management', self)
            user_management_btn.setGeometry(26, 310, self.width-26*2, 35)
            user_management_btn.setFont(QtGui.QFont("Microsoft YaHei UI Light", 14))
            user_management_btn.setStyleSheet("background-color: #57a1f8; color: white; border: none; border-radius: 3px; padding-top: 2px; padding-bottom: 4px")
            user_management_btn.clicked.connect(self.on_user_management_btn_click)
            
            model_management_btn = QPushButton('Model Management', self)
            model_management_btn.setGeometry(26, 355, self.width-26*2, 35)
            model_management_btn.setFont(QtGui.QFont("Microsoft YaHei UI Light", 14))
            model_management_btn.setStyleSheet("background-color: #57a1f8; color: white; border: none; border-radius: 3px; padding-top: 2px; padding-bottom: 4px")
            model_management_btn.clicked.connect(self.on_model_management_btn_click)
        
        if role_id == USER:
            update_information_btn = QPushButton('Update User Information', self)
            update_information_btn.setGeometry(26, 310, self.width-26*2, 35)
            update_information_btn.setFont(QtGui.QFont("Microsoft YaHei UI Light", 14))
            update_information_btn.setStyleSheet("background-color: #57a1f8; color: white; border: none; border-radius: 3px; padding-top: 2px; padding-bottom: 4px")
            update_information_btn.clicked.connect(self.on_update_information_btn_click)
            
            predict_image_btn = QPushButton('Predict image', self)
            predict_image_btn.setGeometry(26, 355, self.width-26*2, 35)
            predict_image_btn.setFont(QtGui.QFont("Microsoft YaHei UI Light", 14))
            predict_image_btn.setStyleSheet("background-color: #57a1f8; color: white; border: none; border-radius: 3px; padding-top: 2px; padding-bottom: 4px")
            predict_image_btn.clicked.connect(self.on_predict_image_btn_click)
        
        view_prediction_hist_btn = QPushButton('View prediction history', self)
        view_prediction_hist_btn.setGeometry(26, 400, self.width-26*2, 35)
        view_prediction_hist_btn.setFont(QtGui.QFont("Microsoft YaHei UI Light", 14))
        view_prediction_hist_btn.setStyleSheet("background-color: #57a1f8; color: white; border: none; border-radius: 3px; padding-top: 2px; padding-bottom: 4px")
        view_prediction_hist_btn.clicked.connect(self.on_view_prediction_hist_btn_click)
        
        logout_btn = QPushButton('Log Out', self)
        logout_btn.setGeometry(26, 445, self.width-26*2, 35)
        logout_btn.setFont(QtGui.QFont("Microsoft YaHei UI Light", 14))
        logout_btn.setStyleSheet("background-color: #57a1f8; color: white; border: none; border-radius: 3px; padding-top: 2px; padding-bottom: 4px")
        logout_btn.clicked.connect(self.on_logout_btn_click)

        self.show()

    def center_label(self, label, y):
        label.adjustSize()
        label.move((self.width - label.width()) // 2, y)

    def center_window(self):
        screen_geometry = QApplication.desktop().screenGeometry()
        top = (screen_geometry.height() - self.height) // 2
        left = (screen_geometry.width() - self.width) // 2
        self.setGeometry(left, top, self.width, self.height)

    def on_update_information_btn_click(self):
        self.update_user_window = UpdateUserInfoWindow()
        self.update_user_window.show()

    def on_user_management_btn_click(self):
        user_management_window = UserManagementWindow()
        user_management_window.show()
    
    def on_view_prediction_hist_btn_click(self):
        call(["python", r"D:\dungnd\GraduationProject\GUI\history_prediction_ui.py", "--user_id", str(user_id), "--role", str(role_id)])
    
    def on_model_management_btn_click(self):
        call(["python", r"D:\dungnd\GraduationProject\GUI\model_management_ui.py"])

    def on_predict_image_btn_click(self):
        call(["python", r"D:\dungnd\GraduationProject\GUI\forgery_image_detection_ui.py", "--user_id", str(user_id)])
    
    def on_logout_btn_click(self):
        self.close()
        call(["python", r"D:\dungnd\GraduationProject\GUI\login.py"])

if __name__ == "__main__":
    AppStart = QApplication(sys.argv)
    AppStart.setStyle('Fusion')
    window = MainWindow()
    sys.exit(AppStart.exec())