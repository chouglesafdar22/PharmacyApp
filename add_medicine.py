import sys
import sqlite3
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QLineEdit, QPushButton, QVBoxLayout, QMessageBox,
    QApplication, QDesktopWidget, QHBoxLayout
)


class MedicineWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manage Medicines")
        self.setGeometry(150, 150, 600, 650)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.setup_ui()
        self.center_window()

    def setup_ui(self):
        self.setStyleSheet("background-color: #f0f0f0;")
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)

        # Search field
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter Medicine Name to Search")
        self.search_input.setStyleSheet("font-size: 25px; padding: 10px; background-color: white;")
        layout.addWidget(self.search_input)

        search_btn = QPushButton("Search Medicine")
        search_btn.setStyleSheet("padding: 12px; font-size: 24px; background-color:#007bff; color:white;")
        search_btn.clicked.connect(self.search_medicine)
        layout.addWidget(search_btn)

        # Input Fields
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name")
        self.name_input.setStyleSheet("font-size: 25px; padding: 10px; background-color: white;")
        layout.addWidget(self.name_input)

        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("Category")
        self.category_input.setStyleSheet("font-size: 25px; padding: 10px; background-color: white;")
        layout.addWidget(self.category_input)

        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Quantity")
        self.quantity_input.setStyleSheet("font-size: 25px; padding: 10px; background-color: white;")
        layout.addWidget(self.quantity_input)

        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Price")
        self.price_input.setStyleSheet("font-size: 25px; padding: 10px; background-color: white;")
        layout.addWidget(self.price_input)

        self.supplier_input = QLineEdit()
        self.supplier_input.setPlaceholderText("Supplier")
        self.supplier_input.setStyleSheet("font-size: 25px; padding: 10px; background-color: white;")
        layout.addWidget(self.supplier_input)

        self.store_location_input = QLineEdit()
        self.store_location_input.setPlaceholderText("Store Location")
        self.store_location_input.setStyleSheet("font-size: 25px; padding: 10px; background-color: white;")
        layout.addWidget(self.store_location_input)

        self.expiry_date_input = QLineEdit()
        self.expiry_date_input.setPlaceholderText("Expiry Date (YYYY-MM-DD)")
        self.expiry_date_input.setStyleSheet("font-size: 25px; padding: 10px; background-color: white;")
        layout.addWidget(self.expiry_date_input)

        # Buttons Layout
        btn_layout = QHBoxLayout()

        save_button = QPushButton("Add New")
        save_button.setStyleSheet("padding: 15px; font-size: 22px; background:#28a745; color:white;")
        save_button.clicked.connect(self.save_medicine)
        btn_layout.addWidget(save_button)

        update_button = QPushButton("Update")
        update_button.setStyleSheet("padding: 15px; font-size: 22px; background:#ffc107; color:black;")
        update_button.clicked.connect(self.update_medicine)
        btn_layout.addWidget(update_button)

        delete_button = QPushButton("Delete")
        delete_button.setStyleSheet("padding: 15px; font-size: 22px; background:#dc3545; color:white;")
        delete_button.clicked.connect(self.delete_medicine)
        btn_layout.addWidget(delete_button)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def save_medicine(self):
        name = self.name_input.text().strip()
        category = self.category_input.text().strip()
        quantity = self.quantity_input.text().strip()
        price = self.price_input.text().strip()
        supplier = self.supplier_input.text().strip()
        store_location = self.store_location_input.text().strip()
        expiry_date = self.expiry_date_input.text().strip()

        if not name or not quantity or not price or not expiry_date:
            QMessageBox.warning(self, "Input Error", "All Details are required.")
            return

        try:
            conn = sqlite3.connect("pharmacy.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO medicines (name, category, quantity, price, supplier, store_location, expiry_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, category, int(quantity), float(price), supplier, store_location, expiry_date))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Success", "Medicine added successfully!")
            self.clear_fields()  

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add: {str(e)}")

    def search_medicine(self):
        name = self.search_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Error", "Enter a medicine name to search.")
            return

        conn = sqlite3.connect("pharmacy.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM medicines WHERE name=?", (name,))
        row = cursor.fetchone()
        conn.close()

        if row:
            _, db_name, category, quantity, price, supplier, store_location, expiry_date = row
            self.name_input.setText(db_name)
            self.category_input.setText(category)
            self.quantity_input.setText(str(quantity))
            self.price_input.setText(str(price))
            self.supplier_input.setText(supplier)
            self.store_location_input.setText(store_location)
            self.expiry_date_input.setText(expiry_date)
        else:
            QMessageBox.information(self, "Not Found", "Medicine not found.")

    def update_medicine(self):
        name = self.name_input.text().strip()
        category = self.category_input.text().strip()
        quantity = self.quantity_input.text().strip()
        price = self.price_input.text().strip()
        supplier = self.supplier_input.text().strip()
        store_location = self.store_location_input.text().strip()
        expiry_date = self.expiry_date_input.text().strip()

        if not name:
            QMessageBox.warning(self, "Error", "Search and load a medicine first!")
            return

        try:
            conn = sqlite3.connect("pharmacy.db")
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE medicines
                SET category=?, quantity=?, price=?, supplier=?, store_location=?, expiry_date=?
                WHERE name=?
            """, (category, int(quantity), float(price), supplier, store_location, expiry_date, name))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Updated", "Medicine updated successfully!")
            self.clear_fields()  

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update: {str(e)}")

    def delete_medicine(self):
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Error", "Search and load a medicine first!")
            return

        reply = QMessageBox.question(self, "Confirm Delete", f"Delete {name}?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No:
            return

        try:
            conn = sqlite3.connect("pharmacy.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM medicines WHERE name=?", (name,))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Deleted", "Medicine deleted successfully!")
            self.clear_fields() 

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete: {str(e)}")

    def clear_fields(self):
        """Clear all input fields"""
        self.name_input.clear()
        self.category_input.clear()
        self.quantity_input.clear()
        self.price_input.clear()
        self.supplier_input.clear()
        self.store_location_input.clear()
        self.expiry_date_input.clear()
        self.search_input.clear() 

    def center_window(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MedicineWindow()
    window.show()
    sys.exit(app.exec_())

