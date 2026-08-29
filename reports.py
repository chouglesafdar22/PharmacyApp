import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QMessageBox, QTableWidget, QTableWidgetItem, QDesktopWidget, QHeaderView, QScrollArea
)
from PyQt5.QtCore import Qt
from datetime import datetime, timedelta

class ReportWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Billing Reports")
        self.setGeometry(200, 200, 1200, 800)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.setup_ui()
        self.center_window()

    def setup_ui(self):
        self.setStyleSheet("background-color: #f8f9fa;")
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Heading
        heading_label = QLabel("Life+ Pharma Billing Reports")
        heading_label.setStyleSheet("font-size: 38px; font-weight: bold; color: #333;")
        heading_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(heading_label)

        # Search Section
        search_layout = QHBoxLayout()
        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText("Enter Date (YYYY-MM-DD)")
        self.date_input.setStyleSheet("font-size: 26px; padding: 10px; background-color: white;")
        search_layout.addWidget(self.date_input)

        search_button = QPushButton("Search Bills")
        search_button.setStyleSheet("font-size: 26px; padding: 10px; background-color: #007bff; color: white;")
        search_button.clicked.connect(self.search_bills)
        search_layout.addWidget(search_button)

        refresh_button = QPushButton("Refresh All")
        refresh_button.setStyleSheet("font-size: 26px; padding: 10px; background-color: #28a745; color: white;")
        refresh_button.clicked.connect(self.load_all_bills)
        search_layout.addWidget(refresh_button)

        main_layout.addLayout(search_layout)

        self.bills_table = QTableWidget()
        self.bills_table.setColumnCount(5)
        self.bills_table.setHorizontalHeaderLabels(["Date", "Total ₹", "GST ₹", "Discount %", "Grand Total ₹"])
        self.bills_table.setStyleSheet("font-size: 26px; background-color: white;")
        self.bills_table.horizontalHeader().setStretchLastSection(True)
        self.bills_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.bills_table.setEditTriggers(QTableWidget.NoEditTriggers)  
        self.bills_table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.bills_table.setMinimumHeight(400) 
        self.bills_table.setMaximumHeight(600) 

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.table_container = QWidget()
        table_layout = QVBoxLayout(self.table_container)
        table_layout.addWidget(self.bills_table)
        self.scroll_area.setWidget(self.table_container)
        main_layout.addWidget(self.scroll_area)

        # Sales Summary Section
        summary_layout = QHBoxLayout()
        self.today_sales_label = QLabel("Today's Sales: ₹0")
        self.week_sales_label = QLabel("Weekly Sales: ₹0")
        self.month_sales_label = QLabel("Monthly Sales: ₹0")
        for label in (self.today_sales_label, self.week_sales_label, self.month_sales_label):
            label.setStyleSheet("font-size: 26px; font-weight: bold; padding: 10px;")
            summary_layout.addWidget(label)
        main_layout.addLayout(summary_layout)

        self.setLayout(main_layout)
        self.load_all_bills() 

    def load_all_bills(self):
        conn = sqlite3.connect("pharmacy.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT date, total_amount, gst, discount, grand_total
            FROM bills
            ORDER BY DATE(date) DESC, id DESC
        """)
        bills = cursor.fetchall()
        conn.close()
        self.populate_table(bills)
        self.load_sales_summary()

    def search_bills(self):
        date = self.date_input.text().strip()
        if not date:
            QMessageBox.warning(self, "Input Error", "Please enter a date.")
            return

        conn = sqlite3.connect("pharmacy.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT date, total_amount, gst, discount, grand_total
            FROM bills
            WHERE date LIKE ?
            ORDER BY DATE(date) DESC, id DESC
        """, (f"{date}%",))
        bills = cursor.fetchall()
        conn.close()
        if not bills:
            QMessageBox.information(self, "No Data", "No bills found for the given date.")
        self.populate_table(bills)
        self.load_sales_summary()

    def populate_table(self, bills):
        self.bills_table.setRowCount(len(bills))
        for row, bill in enumerate(bills):
            for col, value in enumerate(bill):
                if col != 0: 
                    value = f"{float(value):.2f}"
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.bills_table.setItem(row, col, item)

        self.bills_table.resizeColumnsToContents()
        self.bills_table.horizontalHeader().setStretchLastSection(True)

    def load_sales_summary(self):
        conn = sqlite3.connect("pharmacy.db")
        cursor = conn.cursor()
        today = datetime.now().strftime('%Y-%m-%d')
        month_start = datetime.now().replace(day=1).strftime('%Y-%m-%d')

        # Today's Sales
        cursor.execute("SELECT SUM(grand_total) FROM bills WHERE date LIKE ?", (f"{today}%",))
        today_sales = cursor.fetchone()[0] or 0

        # Weekly Sales
        week_sales = 0
        for i in range(7):
            day = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            cursor.execute("SELECT SUM(grand_total) FROM bills WHERE date LIKE ?", (f"{day}%",))
            result = cursor.fetchone()[0]
            if result:
                week_sales += result

        # Monthly Sales
        cursor.execute("SELECT SUM(grand_total) FROM bills WHERE date >= ?", (month_start,))
        month_sales = cursor.fetchone()[0] or 0
        conn.close()

        self.today_sales_label.setText(f"Today's Sales: ₹{today_sales:.2f}")
        self.week_sales_label.setText(f"Weekly Sales: ₹{week_sales:.2f}")
        self.month_sales_label.setText(f"Monthly Sales: ₹{month_sales:.2f}")

    def center_window(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ReportWindow()
    window.show()
    sys.exit(app.exec_())


