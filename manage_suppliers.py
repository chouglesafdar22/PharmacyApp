import sys
import sqlite3
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout,
    QMessageBox, QDesktopWidget, QHBoxLayout
)

class SuppliersWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manage Suppliers")
        self.setGeometry(200, 200, 600, 550)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint) 
        self.setup_ui()
        self.center_window()

    def setup_ui(self):
        self.setStyleSheet("background-color: #f0f0f0;")
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(8, 8, 8, 8)

        # Add Supplier Section
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Supplier Name")
        self.name_input.setStyleSheet("font-size: 25px; padding: 10px; background-color: white;")
        layout.addWidget(self.name_input)

        self.contact_input = QLineEdit()
        self.contact_input.setPlaceholderText("Phone Number")
        self.contact_input.setStyleSheet("font-size: 25px; padding: 10px; background-color: white;")
        layout.addWidget(self.contact_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.email_input.setStyleSheet("font-size: 25px; padding: 10px; background-color: white;")
        layout.addWidget(self.email_input)

        btn_layout = QHBoxLayout()

        save_button = QPushButton("Save Supplier")
        save_button.setStyleSheet("padding: 15px; font-size: 22px; background:#28a745; color:white;")
        save_button.clicked.connect(self.save_supplier)
        btn_layout.addWidget(save_button)

        update_button = QPushButton("Update Supplier")
        update_button.setStyleSheet("padding: 15px; font-size: 22px; background:#ffc107; color:black;")
        update_button.clicked.connect(self.update_supplier)
        btn_layout.addWidget(update_button)

        layout.addLayout(btn_layout)

        search_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search Supplier by Name")
        self.search_input.setStyleSheet("font-size: 25px; padding: 10px; background-color: white;")
        search_layout.addWidget(self.search_input)

        search_button = QPushButton("Search")
        search_button.setStyleSheet("padding: 10px; font-size: 22px; background:#007bff; color:white;")
        search_button.clicked.connect(self.search_supplier)
        search_layout.addWidget(search_button)

        delete_button = QPushButton("Delete")
        delete_button.setStyleSheet("padding: 10px; font-size: 22px; background:#dc3545; color:white;")
        delete_button.clicked.connect(self.delete_supplier)
        search_layout.addWidget(delete_button)

        layout.addLayout(search_layout)

        self.setLayout(layout)

    def save_supplier(self):
        name = self.name_input.text().strip()
        contact = self.contact_input.text().strip()
        email = self.email_input.text().strip()

        if not name:
            QMessageBox.warning(self, "Input Error", "Supplier All Details are required.")
            return

        try:
            conn = sqlite3.connect("pharmacy.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO suppliers (name, contact, email) 
                VALUES (?, ?, ?)
            """, (name, contact, email))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Success", "Supplier added successfully!")
            self.clear_fields()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add supplier: {str(e)}")

    def search_supplier(self):
        name = self.search_input.text().strip()

        if not name:
            QMessageBox.warning(self, "Input Error", "Please enter supplier name to search.")
            return

        try:
            conn = sqlite3.connect("pharmacy.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM suppliers WHERE name LIKE ?", ('%' + name + '%',))
            result = cursor.fetchone()
            conn.close()

            if result:
                _, db_name, contact, email = result
                self.name_input.setText(db_name)
                self.contact_input.setText(contact)
                self.email_input.setText(email)
            else:
                QMessageBox.information(self, "No Result", "No matching suppliers found.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to search supplier: {str(e)}")

    def update_supplier(self):
        name = self.name_input.text().strip()
        contact = self.contact_input.text().strip()
        email = self.email_input.text().strip()

        if not name:
            QMessageBox.warning(self, "Error", "Load a supplier first before updating.")
            return

        try:
            conn = sqlite3.connect("pharmacy.db")
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE suppliers 
                SET contact=?, email=? 
                WHERE name=?
            """, (contact, email, name))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Updated", "Supplier updated successfully!")
            self.clear_fields()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update supplier: {str(e)}")

    def delete_supplier(self):
        name = self.search_input.text().strip()

        if not name:
            QMessageBox.warning(self, "Input Error", "Please enter supplier name to delete.")
            return

        try:
            conn = sqlite3.connect("pharmacy.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM suppliers WHERE name = ?", (name,))
            conn.commit()
            rows_deleted = cursor.rowcount
            conn.close()

            if rows_deleted > 0:
                QMessageBox.information(self, "Deleted", f"{rows_deleted} supplier(s) deleted successfully!")
                self.clear_fields()
            else:
                QMessageBox.information(self, "No Match", "No supplier found with that name.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete supplier: {str(e)}")

    def clear_fields(self):
        self.name_input.clear()
        self.contact_input.clear()
        self.email_input.clear()
        self.search_input.clear()

    def center_window(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SuppliersWindow()
    window.show()
    sys.exit(app.exec_())


