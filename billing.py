import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QMessageBox, QDesktopWidget, QListWidget, QListWidgetItem, QScrollArea
)
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import tempfile
import webbrowser

GST_RATE = 5 

class BillingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Billing System")
        self.setGeometry(200, 200, 1500, 915)
        self.setup_ui()
        self.center_window()

    def setup_ui(self):
        self.setStyleSheet("background-color: #f0f0f0;")
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(8, 8, 8, 8)

        # Customer Details
        self.customer_name_input = QLineEdit()
        self.customer_name_input.setPlaceholderText("Customer Name")
        self.customer_name_input.setStyleSheet("font-size: 27px; padding: 9px; background-color: white;")
        layout.addWidget(self.customer_name_input)

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Phone Number (optional)")
        self.phone_input.setStyleSheet("font-size: 27px; padding: 9px; background-color: white;")
        layout.addWidget(self.phone_input)

        # Search Bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search Medicine...")
        self.search_input.setStyleSheet("font-size: 25px; padding: 8px; background-color: white;")
        self.search_input.textChanged.connect(self.filter_medicine_list)
        layout.addWidget(self.search_input)

        # Medicines List
        self.medicine_list = QListWidget()
        self.medicine_list.setSelectionMode(QListWidget.MultiSelection)
        layout.addWidget(self.medicine_list)
        self.load_medicines()  

        fetch_button = QPushButton("Fetch Prices and Stocks")
        fetch_button.setStyleSheet("font-size: 25px; padding: 8px;")
        fetch_button.clicked.connect(self.fetch_selected_medicines)
        layout.addWidget(fetch_button)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        layout.addWidget(self.scroll_area)

        self.scroll_content = QWidget()
        self.scroll_area.setWidget(self.scroll_content)

        self.quantities_layout = QVBoxLayout(self.scroll_content)
        self.quantities_layout.setContentsMargins(0, 0, 0, 0)
        self.quantities_layout.setSpacing(8)

        # Discount & Totals
        self.discount_input = QLineEdit()
        self.discount_input.setPlaceholderText("Discount (%)")
        self.discount_input.setStyleSheet("font-size: 27px; padding: 9px; background-color: white;")
        layout.addWidget(self.discount_input)

        calc_button = QPushButton("Calculate Total")
        calc_button.setStyleSheet("font-size: 25px; padding: 8px;")
        calc_button.clicked.connect(self.calculate_total)
        layout.addWidget(calc_button)

        self.subtotal_label = QLabel("Subtotal: ₹0")
        self.subtotal_label.setStyleSheet("font-size: 24px;")
        layout.addWidget(self.subtotal_label)

        self.gst_label = QLabel(f"GST ({GST_RATE}%): ₹0")
        self.gst_label.setStyleSheet("font-size: 24px;")
        layout.addWidget(self.gst_label)

        self.grand_total_label = QLabel("Grand Total: ₹0")
        self.grand_total_label.setStyleSheet("font-size: 25px; font-weight: bold;")
        layout.addWidget(self.grand_total_label)

        save_button = QPushButton("Save and Print Bill")
        save_button.setStyleSheet("font-size: 26px; padding:8px; background-color: #4caf50; color: white;")
        save_button.clicked.connect(self.save_and_print_bill)
        layout.addWidget(save_button)

        self.setLayout(layout)

    # Load & Filter Medicines
    def load_medicines(self):
        self.medicine_list.clear()
        conn = sqlite3.connect("pharmacy.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM medicines")
        medicines = cursor.fetchall()
        conn.close()

        self.all_medicines = [med[0] for med in medicines]
        for name in self.all_medicines:
            self.medicine_list.addItem(name)

    def filter_medicine_list(self):
        keyword = self.search_input.text().strip().lower()
        selected_names = [item.text() for item in self.medicine_list.selectedItems()]

        self.medicine_list.clear()
        for name in self.all_medicines:
            if keyword in name.lower():
                item = QListWidgetItem(name)
                self.medicine_list.addItem(item)
                if name in selected_names:
                    item.setSelected(True)

    # Fetch Selected Medicines
    def fetch_selected_medicines(self):
        self.selected_meds = []
        while self.quantities_layout.count():
            child = self.quantities_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for item in self.medicine_list.selectedItems():
            name = item.text()
            conn = sqlite3.connect("pharmacy.db")
            cursor = conn.cursor()
            cursor.execute("SELECT price, quantity FROM medicines WHERE name = ?", (name,))
            result = cursor.fetchone()
            conn.close()

            if result:
                price, stock = result
                label = QLabel(f"{name} - Price: ₹{price}, Stock: {stock}")
                label.setStyleSheet("font-size: 26px;")
                self.quantities_layout.addWidget(label)

                quantity_input = QLineEdit()
                quantity_input.setPlaceholderText("Quantity")
                quantity_input.setStyleSheet("font-size: 28px; padding: 8px; background-color: white;")
                self.quantities_layout.addWidget(quantity_input)

                self.selected_meds.append({
                    "name": name, "price": price, "stock": stock, "quantity_input": quantity_input
                })

    # Calculate Totals
    def calculate_total(self):
        try:
            subtotal = 0
            for med in self.selected_meds:
                quantity = int(med["quantity_input"].text().strip())
                if quantity <= 0 or quantity > med["stock"]:
                    QMessageBox.warning(self, "Input Error", f"Invalid quantity for {med['name']}")
                    return
                subtotal += med["price"] * quantity
                med["quantity"] = quantity

            gst_amount = subtotal * GST_RATE / 100
            discount = float(self.discount_input.text().strip() or 0)
            discount_amount = (subtotal + gst_amount) * (discount / 100)
            grand_total = (subtotal + gst_amount) - discount_amount

            self.subtotal_label.setText(f"Subtotal: ₹{subtotal:.2f}")
            self.gst_label.setText(f"GST ({GST_RATE}%): ₹{gst_amount:.2f}")
            self.grand_total_label.setText(f"Grand Total: ₹{grand_total:.2f}")

            self.subtotal = subtotal
            self.gst_amount = gst_amount
            self.discount = discount
            self.discount_amount = discount_amount
            self.grand_total = grand_total

        except ValueError:
            QMessageBox.warning(self, "Input Error", "Enter valid quantities & discount.")

    # save & print bill
    def save_and_print_bill(self):
        try:
            if not hasattr(self, "grand_total"):
                QMessageBox.warning(self, "Error", "Please calculate total before saving.")
                return

            customer_name = self.customer_name_input.text().strip()
            if not customer_name:
                QMessageBox.warning(self, "Input Error", "Customer name required.")
                return

            conn = sqlite3.connect("pharmacy.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO bills (customer_id, date, total_amount, gst, discount, grand_total)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (None, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                  self.subtotal, self.gst_amount, self.discount, self.grand_total))
            conn.commit()

            for med in self.selected_meds:
                cursor.execute("""
                    UPDATE medicines SET quantity = quantity - ?
                    WHERE name = ?
                """, (med["quantity"], med["name"]))
            conn.commit()
            conn.close()

            self.generate_pdf_bill(customer_name)

            # Reset UI
            self.customer_name_input.clear()
            self.phone_input.clear()
            self.discount_input.clear()
            self.subtotal_label.setText("Subtotal: ₹0")
            self.gst_label.setText(f"GST ({GST_RATE}%): ₹0")
            self.grand_total_label.setText("Grand Total: ₹0")
            self.medicine_list.clearSelection()
            while self.quantities_layout.count():
                child = self.quantities_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error saving bill: {str(e)}")

    # generating pdf
    def generate_pdf_bill(self, customer_name):
        styles = getSampleStyleSheet()
        story = []

        story.append(Paragraph("<b>Life+ Pharma Bill</b>", styles['Title']))
        story.append(Paragraph(f"Customer: {customer_name}", styles['Normal']))
        story.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        story.append(Spacer(1, 20))

        data = [["Medicine", "Qty", "Price ₹", "Total ₹"]]
        for med in self.selected_meds:
            total = med["price"] * med["quantity"]
            data.append([med["name"], str(med["quantity"]), f"{med['price']:.2f}", f"{total:.2f}"])

        data.append(["", "", "Subtotal", f"{self.subtotal:.2f}"])
        data.append(["", "", f"GST ({GST_RATE}%)", f"{self.gst_amount:.2f}"])
        data.append(["", "", f"Discount ({self.discount}%)", f"{self.discount_amount:.2f}"])
        data.append(["", "", "Grand Total", f"{self.grand_total:.2f}"])

        table = Table(data, colWidths=[200, 50, 80, 80])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#4caf50")),
            ('TEXTCOLOR',(0,0),(-1,0),colors.white),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('ALIGN',(1,1),(-1,-1),'CENTER'),
            ('BACKGROUND',(0,1),(-1,-1),colors.whitesmoke)
        ]))
        story.append(table)
        story.append(Spacer(1, 50))
        story.append(Paragraph("<b>Stamp or Sign: Life+ Pharma</b>", styles['Normal']))

        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        doc = SimpleDocTemplate(tmp_file.name, pagesize=A4)
        doc.build(story)

        webbrowser.open_new(tmp_file.name)

    # center window
    def center_window(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BillingWindow()
    window.show()
    sys.exit(app.exec_())




