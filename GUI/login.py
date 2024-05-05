from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import *
from PyQt5 import QtGui
from register import RegisterWindow
from subprocess import call
import sys
import requests


class ClickableLabel(QLabel):
    clicked = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        self.clicked.emit()

class LoginWindow(QWidget):
    def __init__(self, parent = None):
        """constructor to create a new window with charactersitis after create object from class window"""
        super().__init__()
        self.title = "Login to your application"
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
        
        pixmap = QPixmap(r"D:\dungnd\GraduationProject\Icons\login.webp")
        label_img = QLabel(self)
        label_img.setPixmap(pixmap)
        label_img.resize(837//2, 798//2)
        label_img.move(80, 60)
        label_img.setPixmap(pixmap.scaled(label_img.size(), Qt.IgnoreAspectRatio))
        #self.label.show()

        label_login = QLabel(self)
        label_login.move(630, 80)
        label_login.setText('Log In')
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
        self.lineEdit_password.returnPressed.connect(self.on_click)
    
        label_dont_have_acc = QLabel(self)
        label_dont_have_acc.move(575, 300)
        label_dont_have_acc.setText("Don't have an account?")
        label_dont_have_acc.setFont(QtGui.QFont("Microsoft YaHei UI Light", 9))
        label_dont_have_acc.setStyleSheet("color: black")
        
        label_register = ClickableLabel(self)
        label_register.move(710, 300)
        label_register.setText("Register now")
        label_register.setFont(QtGui.QFont("Microsoft YaHei UI Light", 9))
        label_register.setStyleSheet("color: #57a1f8")
        label_register.clicked.connect(self.on_label_register_clicked)

        self.login_btn = QPushButton("Log In", self)
        self.login_btn.setGeometry(QRect(550, 250, 260, 35))
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
        if username == "" or password == "":
            return QMessageBox.warning(self, "Login Failed", "Please fill your username and password", QMessageBox.Ok)
            
        body = {}
        body['username'] = username
        body['password'] = password
        url = "http://localhost:8000/login"
        response = requests.post(url, json=body)

        if response.status_code == 200:
            print("Login successful!")
            user = response.json()['user']
            self.close()
            call(["python", r"D:\dungnd\GraduationProject\GUI\main_ui.py", "--role", str(user['role_id']), "--user_id", str(user['id'])])
        else:
            QMessageBox.warning(self, "Login Failed", response.json()['detail'], QMessageBox.Ok)

    def on_label_register_clicked(self):
        self.register_window = RegisterWindow()
        self.register_window.show()
        self.close()
        

if __name__ == "__main__":
    AppStart = QApplication(sys.argv)
    AppStart.setStyle('Fusion')
    window = LoginWindow()
    sys.exit(AppStart.exec())