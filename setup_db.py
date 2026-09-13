"""
DATABASE SETUP
==============
This script creates the database for both the vulnerable and secure
versions of the ElderEase app. It creates two tables:

1. users — admin accounts that can log in to the system
2. transactions — elderly user transaction records

IMPORTANT: This script creates TWO versions of the database:
- elderease_vulnerable.db  (plain text passwords — intentionally insecure)
- elderease_secure.db      (hashed passwords — properly secured)

This way both apps have their own database and we can demonstrate
the difference clearly in the demo.
"""

import sqlite3
import bcrypt

# ------------------------------------------------------------------
# SAMPLE DATA
# ------------------------------------------------------------------

users = [
    ("admin", "password123"),
    ("staff", "letmein"),
    ("manager", "admin2024"),
]

transactions = [
    ("Nomvula Dlamini", 71, "Lwazi Dlamini", 254.23, "Cash Send (In-Store)", "Shoprite Diepsloot", 4.1, "2025-05-28 09:14:00", "Completed", 1),
    ("Petrus Mokoena", 68, "Tumi Mokoena", 180.00, "Cash Send (In-Store)", "Shoprite Alex", 6.3, "2025-05-27 11:32:00", "Failed", 1),
    ("Agnes Sithole", 74, "Refilwe Sithole", 300.00, "ATM Cash Send", "Shoprite Tembisa", 8.7, "2025-05-26 08:55:00", "Completed", 0),
    ("Johannes van Wyk", 70, "Andile van Wyk", 150.00, "Cash Send (In-Store)", "Shoprite Soweto", 9.2, "2025-05-28 10:20:00", "Completed", 1),
    ("Beauty Nkosi", 66, "Nkosana Nkosi", 220.50, "Cash Send (In-Store)", "Shoprite Diepsloot", 5.4, "2025-05-25 14:10:00", "Pending", 1),
    ("Thabo Molefe", 28, "Lerato Molefe", 1200.00, "Bank App Transfer", "Shoprite Bramley", 2.1, "2025-05-20 16:45:00", "Completed", 0),
    ("Sarah Botha", 24, "Bongani Botha", 850.00, "EFT", "Checkers Midrand", 1.8, "2025-05-22 09:00:00", "Completed", 0),
    ("Kagiso Tau", 31, "Mandla Ndlovu", 500.00, "Bank App Transfer", "Pick n Pay Sandton", 3.2, "2025-05-23 13:30:00", "Completed", 0),
    ("Samuel Mahlangu", 73, "Boitumelo Mahlangu", 175.00, "Cash Send (In-Store)", "Shoprite Soshanguve", 11.5, "2025-05-28 08:00:00", "Failed", 1),
    ("Maria Khumalo", 69, "Sibusiso Khumalo", 90.00, "Cash Send (In-Store)", "Shoprite Alex", 7.8, "2025-05-27 15:20:00", "Completed", 1),
]

# ------------------------------------------------------------------
# BUILD VULNERABLE DATABASE (plain text passwords)
# ------------------------------------------------------------------
print("Creating vulnerable database...")
conn_v = sqlite3.connect("elderease_vulnerable.db")
cur_v = conn_v.cursor()

cur_v.execute("DROP TABLE IF EXISTS users")
cur_v.execute("DROP TABLE IF EXISTS transactions")

cur_v.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
""")

cur_v.execute("""
    CREATE TABLE transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender_name TEXT,
        sender_age INTEGER,
        receiver_name TEXT,
        amount REAL,
        method TEXT,
        location TEXT,
        distance_km REAL,
        timestamp TEXT,
        status TEXT,
        needed_assistance INTEGER
    )
""")

for username, password in users:
    cur_v.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, password)
    )

for t in transactions:
    cur_v.execute("""
        INSERT INTO transactions
        (sender_name, sender_age, receiver_name, amount, method, location, distance_km, timestamp, status, needed_assistance)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, t)

conn_v.commit()
conn_v.close()
print("  elderease_vulnerable.db created with plain text passwords")

# ------------------------------------------------------------------
# BUILD SECURE DATABASE (hashed passwords)
# ------------------------------------------------------------------
print("Creating secure database...")
conn_s = sqlite3.connect("elderease_secure.db")
cur_s = conn_s.cursor()

cur_s.execute("DROP TABLE IF EXISTS users")
cur_s.execute("DROP TABLE IF EXISTS transactions")

cur_s.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password_hash TEXT NOT NULL
    )
""")

cur_s.execute("""
    CREATE TABLE transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender_name TEXT,
        sender_age INTEGER,
        receiver_name TEXT,
        amount REAL,
        method TEXT,
        location TEXT,
        distance_km REAL,
        timestamp TEXT,
        status TEXT,
        needed_assistance INTEGER
    )
""")

for username, password in users:
    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")
    cur_s.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        (username, password_hash)
    )

for t in transactions:
    cur_s.execute("""
        INSERT INTO transactions
        (sender_name, sender_age, receiver_name, amount, method, location, distance_km, timestamp, status, needed_assistance)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, t)

conn_s.commit()
conn_s.close()
print("  elderease_secure.db created with bcrypt hashed passwords")

# ------------------------------------------------------------------
# VERIFICATION
# ------------------------------------------------------------------
print("\nVerification:")

conn_v = sqlite3.connect("elderease_vulnerable.db")
rows = conn_v.execute("SELECT username, password FROM users").fetchall()
print("\n  Vulnerable DB — passwords (PLAIN TEXT — this is the problem):")
for row in rows:
    print(f"    {row[0]:<12} {row[1]}")
conn_v.close()

conn_s = sqlite3.connect("elderease_secure.db")
rows = conn_s.execute("SELECT username, password_hash FROM users").fetchall()
print("\n  Secure DB — passwords (HASHED — cannot be reversed):")
for row in rows:
    print(f"    {row[0]:<12} {row[1][:40]}...")
conn_s.close()

print("\nBoth databases ready.")