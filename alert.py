import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox, QDesktopWidget, QHeaderView
)
from PyQt5.QtCore import Qt
from datetime import datetime, timedelta

class AlertWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Medicine Alerts")
        self.setGeometry(200, 200, 1200, 800)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.setup_ui()
        self.center_window()

    def setup_ui(self):
        self.setStyleSheet("background-color: #fffaf0;")
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Heading
        heading = QLabel("⚠️ Medicine Alerts")
        heading.setStyleSheet("font-size: 38px; font-weight: bold; color: #cc0000;")
        heading.setAlignment(Qt.AlignCenter)
        layout.addWidget(heading)

        # Expiring Medicines
        expiry_label = QLabel("🗓️ Expiring Medicines (within 30 days)")
        expiry_label.setStyleSheet("font-size: 28px; font-weight: bold; padding: 5px;")
        layout.addWidget(expiry_label)

        self.expiry_table = QTableWidget()
        self.expiry_table.setColumnCount(4)
        self.expiry_table.setHorizontalHeaderLabels(
            ["Medicine", "Expiry Date", "Quantity", "Store Location"]
        )
        self.expiry_table.setStyleSheet("font-size: 26px; background-color: white;")
        self.expiry_table.horizontalHeader().setStretchLastSection(True)
        self.expiry_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.expiry_table.setEditTriggers(QTableWidget.NoEditTriggers) 
        layout.addWidget(self.expiry_table)

        # Low Stock Medicines
        stock_label = QLabel("📉 Low Stock Medicines (Quantity ≤ 10)")
        stock_label.setStyleSheet("font-size: 28px; font-weight: bold; padding: 5px;")
        layout.addWidget(stock_label)

        self.stock_table = QTableWidget()
        self.stock_table.setColumnCount(4)
        self.stock_table.setHorizontalHeaderLabels(
            ["Medicine", "Expiry Date", "Quantity", "Store Location"]
        )
        self.stock_table.setStyleSheet("font-size: 26px; background-color: white;")
        self.stock_table.horizontalHeader().setStretchLastSection(True)
        self.stock_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.stock_table.setEditTriggers(QTableWidget.NoEditTriggers)  
        layout.addWidget(self.stock_table)

        # Refresh Button
        refresh_btn = QPushButton("Refresh Alerts")
        refresh_btn.setStyleSheet("font-size: 26px; padding: 14px; background-color: #17a2b8; color: white;")
        refresh_btn.clicked.connect(self.load_alerts)
        layout.addWidget(refresh_btn)

        self.setLayout(layout)
        self.load_alerts()

    def load_alerts(self):
        conn = sqlite3.connect("pharmacy.db")
        cursor = conn.cursor()
        today = datetime.now().date()
        expiry_limit = today + timedelta(days=30)

        # Expiring Medicines (Only within next 30 days, excluding already expired)
        cursor.execute("""
           SELECT name, expiry_date, quantity, store_location FROM medicines
           WHERE expiry_date IS NOT NULL AND expiry_date != ''
           AND expiry_date > ? AND expiry_date <= ?
        """, (today.strftime('%Y-%m-%d'), expiry_limit.strftime('%Y-%m-%d')))
        expiring = cursor.fetchall()
        self.populate_table(self.expiry_table, expiring)

        # Low Stock Medicines
        cursor.execute("""
           SELECT name, expiry_date, quantity, store_location FROM medicines
           WHERE quantity <= 10
        """)
        low_stock = cursor.fetchall()
        self.populate_table(self.stock_table, low_stock)

        conn.close()

    def populate_table(self, table, data):
        table.setRowCount(len(data))
        for row, item in enumerate(data):
            for col, value in enumerate(item):
                cell = QTableWidgetItem(str(value))
                cell.setTextAlignment(Qt.AlignCenter)
                table.setItem(row, col, cell)

    def center_window(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AlertWindow()
    window.show()
    sys.exit(app.exec_())

