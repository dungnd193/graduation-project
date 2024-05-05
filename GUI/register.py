from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import *
from PyQt5 import QtGui
from subprocess import call
import requests
import sys

class ClickableLabel(QLabel):
    clicked = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        self.clicked.emit()

class RegisterWindow(QWidget):
    def __init__(self, parent = None):
        """constructor to create a new window with charactersitis after create object from class window"""
        super().__init__()
        self.title = "Register your account"
        self.width = 925
        self.height = 500
        self.file_path = ""
        self.init_window()

    def init_window(self):
        """initialize Main IFD window"""

        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon(r"D:\dungnd\GraduationProject\Icons\icons8-cbs-512.ico")) #icon Pic File name
        self.setFixedSize(self.width , self.height)
        self.center_window()

        pixmap = QPixmap(r"D:\dungnd\GraduationProject\Icons\registration.webp")
        label_img = QLabel(self)
        label_img.setPixmap(pixmap)
        label_img.resize(834//2, 877//2)
        label_img.move(80, 20)
        label_img.setPixmap(pixmap.scaled(label_img.size(), Qt.IgnoreAspectRatio))
        #self.label.show()

        label_login = QLabel(self)
        label_login.move(630, 80)
        label_login.setText('Register')
        label_login.setFont(QtGui.QFont("Microsoft YaHei UI Light", 24))
        label_login.setStyleSheet("color: #57a1f8;")

        label_username = QLabel(self)
        label_username.move(530, 150)
        label_username.setText('Username')
        label_username.setFont(QtGui.QFont("Microsoft YaHei UI Light", 12))
        label_username.setStyleSheet("color: black;")
        
        self.lineEdit_username = QLineEdit(self)
        self.lineEdit_username.setGeometry(650, 150, 180, 30)
        self.lineEdit_username.setPlaceholderText(' Please enter your username')

        label_password = QLabel(self)
        label_password.move(530, 200)
        label_password.setText('Password')
        label_password.setFont(QtGui.QFont("Microsoft YaHei UI Light", 12))
        label_password.setStyleSheet("color: black;")
        
        self.lineEdit_password = QLineEdit(self)
        self.lineEdit_password.setGeometry(650, 200, 180, 30)
        self.lineEdit_password.setPlaceholderText(' Please enter your password')
        self.lineEdit_password.setEchoMode(QLineEdit.Password)
     
        label_email = QLabel(self)
        label_email.move(530, 250)
        label_email.setText('Email')
        label_email.setFont(QtGui.QFont("Microsoft YaHei UI Light", 12))
        label_email.setStyleSheet("color: black;")
        
        self.lineEdit_email = QLineEdit(self)
        self.lineEdit_email.setGeometry(650, 250, 180, 30)
        self.lineEdit_email.setPlaceholderText(' Please enter your email')
        self.lineEdit_email.setEchoMode(QLineEdit.Password)
        
        label_phone_number = QLabel(self)
        label_phone_number.move(530, 300)
        label_phone_number.setText('Phone Number')
        label_phone_number.setFont(QtGui.QFont("Microsoft YaHei UI Light", 12))
        label_phone_number.setStyleSheet("color: black;")
        
        self.lineEdit_phone_number = QLineEdit(self)
        self.lineEdit_phone_number.setGeometry(650, 300, 180, 30)
        self.lineEdit_phone_number.setPlaceholderText(' Please enter your phone number')
        self.lineEdit_phone_number.setEchoMode(QLineEdit.Password)

        label_dont_have_acc = QLabel(self)
        label_dont_have_acc.move(575, 400)
        label_dont_have_acc.setText("Already have an account?")
        label_dont_have_acc.setFont(QtGui.QFont("Microsoft YaHei UI Light", 9))
        label_dont_have_acc.setStyleSheet("color: black")
        
        label_register = ClickableLabel(self)
        label_register.move(720, 400)
        label_register.setText("Log In now")
        label_register.setFont(QtGui.QFont("Microsoft YaHei UI Light", 9))
        label_register.setStyleSheet("color: #57a1f8")
        label_register.clicked.connect(self.on_label_register_clicked)

        self.login_btn = QPushButton("Register", self)
        self.login_btn.setGeometry(QRect(550, 350, 260, 35))
        self.login_btn.setStyleSheet("background-color: #57a1f8; color: white; border: none")
        self.login_btn.clicked.connect(self.on_click)
        self.show()

    def center_window(self):
            screen_geometry = QApplication.desktop().screenGeometry()
            top = (screen_geometry.height() - self.height) // 2
            left = (screen_geometry.width() - self.width) // 2
            self.setGeometry(left, top, self.width, self.height)

    def on_click(self):
        username = self.lineEdit_username.text()
        password = self.lineEdit_password.text()
        email = self.lineEdit_email.text()
        phone_number = self.lineEdit_phone_number.text()
        if username == "" or password == "" or email == "" or phone_number == "":
            return QMessageBox.warning(self, "Register Failed", "Please fill your information", QMessageBox.Ok)
            
        body = {}
        body['username'] = username
        body['password'] = password
        body['email'] = email
        body['phone_number'] = phone_number
        body['role_id'] = 2
        body['status'] = 'ACTIVE'

        url = "http://localhost:8000/users/"
        response = requests.post(url, json=body)

        if response.status_code == 201:
            QMessageBox.information(self, "Registration Successful", "You have successfully registered!")
            self.close()
            call(["python", r"D:\dungnd\GraduationProject\GUI\login.py"])
        else:
            print("Register failed:", response.json())

    def on_label_register_clicked(self):
        self.close()
        call(["python", r"D:\dungnd\GraduationProject\GUI\login.py"])
        

if __name__ == "__main__":
    AppStart = QApplication(sys.argv)
    AppStart.setStyle('Fusion')
    window = RegisterWindow()
    sys.exit(AppStart.exec())