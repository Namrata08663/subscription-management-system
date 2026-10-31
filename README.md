# subscription-management-system
Subscription management system-Hackathon project 


import sqlite3

# STEP 1: Create database connection
conn = sqlite3.connect("subscription.db")

# STEP 2: Create cursor
cursor = conn.cursor()

# STEP 3: Create users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    phone TEXT
)
""")

conn.commit()
conn.close()

print("User database created successfully!")


# STEP 4: Register new user
def register_user(name, email, password, role, phone):

    conn = sqlite3.connect("subscription.db")
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO users (name, email, password, role, phone)
            VALUES (?, ?, ?, ?, ?)
        """, (name, email, password, role, phone))

        conn.commit()
        print("\nUser registered successfully!")

    except sqlite3.IntegrityError:
        print("\nThis email is already registered!")

    finally:
        conn.close()


# STEP 5: Get user information
print("\n===== CUSTOMER REGISTRATION =====")

name = input("Enter your name: ")
email = input("Enter your email: ")
password = input("Enter your password: ")
role = input("Enter your role (customer/staff/admin): ").lower()
phone = input("Enter your phone number: ")

# STEP 6: Call registration function
register_user(name, email, password, role, phone)
