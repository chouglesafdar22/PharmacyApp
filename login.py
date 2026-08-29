import sys
import sqlite3
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QDesktopWidget
)
from db import connect_db, add_dummy_user 
from dashboard import DashboardWindow  

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Life+ Pharma Login")
        self.setGeometry(100, 100, 600, 325)  
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.setup_ui()
        self.center_window() 

    def setup_ui(self):
        self.setStyleSheet("background-color: #d3d3d3;")  

        layout = QVBoxLayout()
        layout.setSpacing(10)  
        layout.setContentsMargins(5, 5, 5, 5) 

        # Username Field
        self.label_username = QLabel("Username:")
        font = self.label_username.font()
        font.setPointSize(25)  
        self.label_username.setFont(font)

        self.input_username = QLineEdit()
        self.input_username.setStyleSheet("background-color: white; padding: 2px; font-size: 20px;")  
        layout.addWidget(self.label_username)
        layout.addWidget(self.input_username)

        # Password Field
        self.label_password = QLabel("Password:")
        self.label_password.setFont(font)

        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)
        self.input_password.setStyleSheet("background-color: white; padding: 2px; font-size: 20px;")
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)

        # Login Button
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)
        self.login_button.setStyleSheet("padding: 10px 20px; font-size: 23px;")
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def center_window(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def login(self):
        username = self.input_username.text()
        password = self.input_password.text()

        # Check if fields are empty
        if not username or not password:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Both are required.")
            msg.setWindowTitle("Missing Information")
            msg.setStyleSheet("font-size: 23px;")
            msg.setFixedSize(500, 500)
            msg.exec_()
            return  

        # Check login from database
        conn = sqlite3.connect("pharmacy.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        result = cursor.fetchone()
        conn.close()

        if result:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setText(f"Welcome, {username}!")
            msg.setWindowTitle("Login Success")
            msg.setStyleSheet("font-size: 25px;")
            msg.setFixedSize(500, 500)
            msg.exec_()

            self.dashboard = DashboardWindow()
            self.dashboard.show()
            self.close()
        else:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Invalid username or password.")
            msg.setWindowTitle("Login Failed")
            msg.setStyleSheet("font-size: 25px;")
            msg.setFixedSize(500, 500)
            msg.exec_()

if __name__ == "__main__":
    connect_db()
    add_dummy_user()
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())






