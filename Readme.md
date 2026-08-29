# Pharmacy Management System

A desktop application built to manage common pharmacy operations such as medicine inventory, suppliers, billing, stock alerts, and sales reports.

The application provides a single interface for handling day-to-day pharmacy tasks instead of maintaining separate manual records.

## Features

- Admin login and access control
- Add and manage medicines
- Search and update medicine records
- Track medicine stock and expiry dates
- Manage supplier information
- Create and manage customer bills
- Automatic GST and discount calculations
- Bill printing
- Low-stock alerts
- Medicine expiry alerts
- Daily, weekly, and monthly sales reports
- SQLite database for storing application data

## Tech Stack

- **Python**
- **PyQt5** — Desktop GUI
- **SQLite** — Database
- **Visual Studio** — Development environment

## Application Modules

### Login

Provides the login interface for authorized access to the application.

### Dashboard

Acts as the main area of the application and provides access to the different pharmacy management modules.

### Medicine Management

Allows medicines to be added, updated, deleted, and searched. Stock and expiry information can also be maintained.

### Supplier Management

Provides functionality for managing supplier records and searching existing suppliers.

### Billing

Handles the billing process, including medicine selection, quantity, GST, discounts, total calculation, and bill generation.

### Alerts

Displays important inventory information such as low-stock medicines and medicines approaching expiry.

### Reports

Provides sales reports that can be used to review pharmacy activity over different time periods.

## Project Structure

```text
PharmacyApp/
│
├── add_medicine.py
├── alert.py
├── billing.py
├── dashboard.py
├── db.py
├── delete.py
├── login.py
├── main.py
├── manage_suppliers.py
├── reports.py
│
├── PharmacyApp.pyproj
├── PharmacyApp.sln
├── .gitignore
└── README.md