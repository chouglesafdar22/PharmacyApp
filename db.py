import sqlite3

# Function to create database and tables (with store_location and expiry_date)
def connect_db():
    connection = sqlite3.connect("pharmacy.db")
    cursor = connection.cursor()

    # Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # Medicines Table (without store_location and expiry_date at creation)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medicines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT,
        quantity INTEGER,
        price REAL,
        supplier TEXT
    )
    """)

    # Add store_location column if missing
    try:
        cursor.execute("ALTER TABLE medicines ADD COLUMN store_location TEXT;")
        print(" 'store_location' column added successfully.")
    except sqlite3.OperationalError:
        pass

    #  Add expiry_date column if missing
    try:
        cursor.execute("ALTER TABLE medicines ADD COLUMN expiry_date TEXT;")
        print(" 'expiry_date' column added successfully.")
    except sqlite3.OperationalError:
        pass

    # Customers Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT
    )
    """)

    # Suppliers Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS suppliers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        contact TEXT
    )
    """)

    # Add 'email' column to suppliers if missing (migration)
    try:
        cursor.execute("ALTER TABLE suppliers ADD COLUMN email TEXT;")
        print(" 'email' column added to suppliers.")
    except sqlite3.OperationalError:
        pass 

    # Bills Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        date TEXT,
        total_amount REAL,
        gst REAL,
        discount REAL,
        grand_total REAL,
        FOREIGN KEY (customer_id) REFERENCES customers(id)
    )
    """)

    connection.commit()
    connection.close()

# Dummy user for login testing
def add_dummy_user():
    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "admin123"))
    except sqlite3.IntegrityError:
        pass  
    conn.commit()
    conn.close()

# Medicine Search Function (with location & quantity)
def search_medicine_in_db(medicine_name):
    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medicines WHERE name LIKE ?", ('%' + medicine_name + '%',))
    result = cursor.fetchall()
    conn.close()
    return result

if __name__ == "__main__":
    connect_db()
    add_dummy_user()
    print("Database & Dummy User Ready.")



