from PyQt5.QtWidgets import * 
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import *
from PyQt5 import QtGui
import sys
import requests

class ButtonCellWidget(QWidget):
    def __init__(self, user_id, parent=None):
        super().__init__(parent)
        self.user_id = user_id  # Store the user ID
        layout = QHBoxLayout()
        self.active_button = QPushButton("Active")
        self.active_button.setStyleSheet("background-color: #4bcd00; color: white; border: none; padding: 3px")

        self.deactivate_button = QPushButton("Deactivate")
        self.deactivate_button.setStyleSheet("background-color: #d13645; color: white; border: none; padding: 3px")

        spacer_left = QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
        spacer_right = QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)

        layout.addItem(spacer_left)
        layout.addWidget(self.active_button)
        layout.addWidget(self.deactivate_button)
        layout.addItem(spacer_right)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)  # Adjust spacing between buttons
        self.setLayout(layout)

class UserManagementWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.title = "User Management"
        self.width = 860
        self.height = 500
        self.file_path = ""
        self.get_all_users()
        self.init_window()

    def get_all_users(self):
        url = "http://localhost:8000/users/"
        response = requests.get(url)
        if response.status_code == 200:
            self.users = response.json()
        else:
            print("Get all users error:", response.json())

    def init_window(self):
        # self.setStyleSheet('background-color: #1e2d44;')
        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon(r"D:\dungnd\GraduationProject\Icons\icons8-cbs-512.ico"))
        self.setFixedSize(self.width, self.height)
        self.center_window()
        
        label_user_management = QLabel(self)
        label_user_management.move(310, 10)
        label_user_management.setText('User Management')
        label_user_management.setFont(QtGui.QFont("Microsoft YaHei UI Light", 24))
        label_user_management.setStyleSheet("color: #57a1f8; font-weight: bold")
        self.center_label(label_user_management, 10)


        table_frame = QFrame(self)
        table_frame.setGeometry(30, 120, 800, 600)

        self.tableWidget = QTableWidget(table_frame)
        self.tableWidget.setColumnCount(6)  # Adjusted to 5 columns
        self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem("Id"))
        self.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem("Username"))
        self.tableWidget.setHorizontalHeaderItem(2, QTableWidgetItem("Email"))
        self.tableWidget.setHorizontalHeaderItem(3, QTableWidgetItem("Phone Number"))
        self.tableWidget.setHorizontalHeaderItem(4, QTableWidgetItem("Status"))
        self.tableWidget.setHorizontalHeaderItem(5, QTableWidgetItem("Action"))

        self.tableWidget.setColumnWidth(0, 30)  
        self.tableWidget.setColumnWidth(1, 120)  
        self.tableWidget.setColumnWidth(2, 200)  
        self.tableWidget.setColumnWidth(3, 120)  
        self.tableWidget.setColumnWidth(4, 100)  
        self.tableWidget.setColumnWidth(5, 224)

        header = self.tableWidget.horizontalHeader()
        header.setStyleSheet("background-color: white; color: black;")
        # header.setSectionResizeMode(QHeaderView.ResizeToContents)
        # header.setMinimumSectionSize(300)
        # header.setSectionResizeMode(4, QHeaderView.Fixed)  # Prevent resizing of the last column

        self.tableWidget.setFixedWidth(self.width-60)
        self.tableWidget.setFixedHeight(self.height-150)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Insert rows
        for idx, user in enumerate(self.users):
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, QTableWidgetItem(str(user['id'])))
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, QTableWidgetItem(user['username']))
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 2, QTableWidgetItem(user['email']))
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 3, QTableWidgetItem(user['phone_number']))
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 4, QTableWidgetItem(user['status']))

            # Create buttons in the Actions column
            button_widget = ButtonCellWidget("ID"+str(user['id']))  # Pass user ID as parameter
            self.tableWidget.setCellWidget(idx, 5, button_widget)

            # Connect button signals to slots
            button_widget.active_button.clicked.connect(lambda _, id=user['id']: self.on_active_button_clicked(id))
            button_widget.deactivate_button.clicked.connect(lambda _, id=user['id']: self.on_deactivate_button_clicked(id))

        for idx in range(5):
            self.tableWidget.horizontalHeaderItem(idx).setTextAlignment(Qt.AlignCenter)
            for row in range(self.tableWidget.rowCount()):
                item = self.tableWidget.item(row, idx)
                if item is not None:
                    item.setTextAlignment(Qt.AlignCenter)

        self.tableWidget.setStyleSheet(
            "QTableWidget { background-color: #ffffff; border: 1px solid #d3d3d3; }"
            "QHeaderView::section { background-color: #f2f2f2; border: none; }"
            "QTableWidget::item { padding: 5px; }"
            "QTableWidget::item:selected { background-color: #3ca355; }"
        )


        self.search_btn = QPushButton("Search by Username", self)
        self.search_btn.setGeometry(QRect(30, 60, 180, 40))
        self.search_btn.setStyleSheet("background-color: #57a1f8; color: white; border: none; font-size: 16px")
        self.search_btn.clicked.connect(self.search_by_username)
        
        self.search_box = QLineEdit(self)
        self.search_box.setGeometry(QRect(230, 60, 600, 41))
        self.search_box.setMinimumWidth(540)
        self.search_box.setMinimumHeight(40)
        self.search_box.setStyleSheet("font: 75 12pt \"MS Shell Dlg 2\";\n"
                                 "background-color: white;\n"
                                 "color: black;\n"
                                 "padding-left: 10px; padding-right: 10px;")

        self.show()

    def center_label(self, label, y):
        label.adjustSize()
        label.move((self.width - label.width()) // 2, y)

    def center_window(self):
        screen_geometry = QApplication.desktop().screenGeometry()
        top = (screen_geometry.height() - self.height) // 2
        left = (screen_geometry.width() - self.width) // 2
        self.setGeometry(left, top, self.width, self.height)

    def search_by_username(self):
        username = self.search_box.text()
        url = "http://localhost:8000/users/search/"
        params = {}
        params['username']=username
        response = requests.get(url, params=params)
        if response.status_code == 200:
            # Clear existing rows in the table
            self.tableWidget.setRowCount(0)
            
            # Insert rows for the searched users
            users = response.json()
            for idx, user in enumerate(users):
                self.tableWidget.insertRow(self.tableWidget.rowCount())
                self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, QTableWidgetItem(str(user['id'])))
                self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, QTableWidgetItem(user['username']))
                self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 2, QTableWidgetItem(user['email']))
                self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 3, QTableWidgetItem(user['phone_number']))
                self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 4, QTableWidgetItem(user['status']))

                # Create buttons in the Actions column
                button_widget = ButtonCellWidget("ID"+str(user['id']))  # Pass user ID as parameter
                self.tableWidget.setCellWidget(idx, 5, button_widget)

                # Connect button signals to slots
                button_widget.active_button.clicked.connect(lambda _, id=user['id']: self.on_active_button_clicked(id))
                button_widget.deactivate_button.clicked.connect(lambda _, id=user['id']: self.on_deactivate_button_clicked(id))
                # button_widget.update_button.clicked.connect(lambda _, id=user['id']: self.on_update_button_clicked(id))
        else:
            print("Get all users error:", response.json())

    def update_status_in_ui(self, user_id, status):
    # Find the row index of the user in the table
        for row in range(self.tableWidget.rowCount()):
            if self.tableWidget.item(row, 0).text() == str(user_id):
                # Update the status in the corresponding QTableWidgetItem
                self.tableWidget.item(row, 4).setText(status)
                break

    def on_active_button_clicked(self, user_id):
        url = "http://localhost:8000/users/"+str(user_id)+"/status"
        body = {}
        body['status'] = "ACTIVE"
        
        reply = QMessageBox.question(self, 'Confirmation', f"Do you want to activate user ID: {user_id}?", 
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            response = requests.put(url, json=body)
            if response.status_code == 200:
                self.update_status_in_ui(user_id, "ACTIVE")
            else:
                print("Update user status error:", response.json())
        else:
            pass

    def on_deactivate_button_clicked(self, user_id):
        url = "http://localhost:8000/users/"+str(user_id)+"/status"
        body = {}
        body['status'] = "DEACTIVED"

        reply = QMessageBox.question(self, 'Confirmation', f"Do you want to deactivate user ID: {user_id}?", 
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            response = requests.put(url, json=body)
            if response.status_code == 200:
                self.update_status_in_ui(user_id, "DEACTIVED")
            else:
                print("Update user status error:", response.json())
        else:
            pass
if __name__ == "__main__":
    AppStart = QApplication(sys.argv)
    AppStart.setStyle('Fusion')
    window = UserManagementWindow()
    sys.exit(AppStart.exec())
