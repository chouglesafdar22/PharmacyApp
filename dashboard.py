import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QMessageBox, QDesktopWidget
)
from db import search_medicine_in_db  
from manage_suppliers import SuppliersWindow  
from add_medicine import MedicineWindow  
from reports import ReportWindow
from billing import BillingWindow
from alert import AlertWindow

class DashboardWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Life+ Pharma Dashboard")
        self.setGeometry(100, 100, 1500, 750)
        self.setup_ui()
        self.center_window()

    def setup_ui(self):
        self.setStyleSheet("background-color: #d3d3d3;")  

        main_layout = QVBoxLayout()
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(8, 8, 8, 8)

        # Search Bar Section
        search_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search Medicine by Name...")
        self.search_input.setStyleSheet("padding: 8px; font-size: 45px; background-color: white;")

        search_button = QPushButton("Search")
        search_button.setStyleSheet("padding: 8px; font-size: 40px;")
        search_button.clicked.connect(self.search_medicine)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        main_layout.addLayout(search_layout)

        # Buttons Section
        btn_add_medicine = QPushButton("Medicines")
        btn_add_medicine.setStyleSheet("padding: 8px; font-size: 60px;")
        btn_add_medicine.clicked.connect(self.open_add_medicine)
        main_layout.addWidget(btn_add_medicine)

        btn_suppliers = QPushButton("Suppliers")
        btn_suppliers.setStyleSheet("padding: 8px; font-size: 60px;")
        btn_suppliers.clicked.connect(self.open_suppliers)  
        main_layout.addWidget(btn_suppliers)

        btn_billing = QPushButton("Billing")
        btn_billing.setStyleSheet("padding: 8px; font-size: 60px;")
        btn_billing.clicked.connect(self.open_billing)
        main_layout.addWidget(btn_billing)

        btn_reports = QPushButton("Reports")
        btn_reports.setStyleSheet("padding: 8px; font-size: 60px;")
        btn_reports.clicked.connect(self.open_reports)
        main_layout.addWidget(btn_reports)

        btn_alert = QPushButton("Alert")
        btn_alert.setStyleSheet("padding: 8px; font-size: 60px;")
        btn_alert.clicked.connect(self.open_alert)
        main_layout.addWidget(btn_alert)

        self.setLayout(main_layout)

    # Medicine Search Function
    def search_medicine(self):
        medicine_name = self.search_input.text().strip()

        if not medicine_name:
            QMessageBox.warning(self, "Input Required", "Please enter a name to search.")
            return

        try:
            result = search_medicine_in_db(medicine_name)  

            if result:
                msg = ""
                for med in result:
                    msg += (
                        f"Name: {med[1]}\n"
                        f"Category: {med[2]}\n"
                        f"Quantity: {med[3]}\n"
                        f"Price: {med[4]}\n"
                        f"Supplier: {med[5]}\n"
                        f"Store Location: {med[6]}\n"
                    )
                    if len(med) > 7:
                        msg += f"Expiry Date: {med[7]}\n"
                    msg += "\n"  
            else:
                msg = f"Medicine '{medicine_name}' is NOT AVAILABLE."

            QMessageBox.information(self, "Search Result", msg)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error searching medicine: {str(e)}")

    # Open Window
    def open_add_medicine(self):
        self.add_medicine_window = MedicineWindow()
        self.add_medicine_window.show()

    def open_suppliers(self):
        self.suppliers_window = SuppliersWindow()
        self.suppliers_window.show()

    def open_billing(self):
        self.billing_window = BillingWindow()
        self.billing_window.show()

    def open_reports(self):
        self.reports_window = ReportWindow()
        self.reports_window.show()

    def open_alert(self):
        self.alert_window = AlertWindow()
        self.alert_window.show()

    def center_window(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DashboardWindow()
    window.show()
    sys.exit(app.exec_())



