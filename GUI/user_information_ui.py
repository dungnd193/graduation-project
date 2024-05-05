from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import *
from PyQt5 import QtGui
import requests


class UpdateUserInfoWindow(QWidget):
    def __init__(self, user_id, parent = None):
        """constructor to create a new window with charactersitis after create object from class window"""
        super().__init__()
        self.user_id = user_id
        self.title = "Update user information"
        self.width = 400
        self.height = 450
        self.get_user_by_id(str(self.user_id))
        self.init_window()

    
    def get_user_by_id(self, user_id):
        url = "http://localhost:8000/users/"+str(self.user_id)
        params = {}
        params['user_id']=int(self.user_id)
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
