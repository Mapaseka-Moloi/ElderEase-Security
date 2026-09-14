ecure · PY
"""
SECURE VERSION — ElderEase Admin App
======================================
This version fixes all three vulnerabilities from app_vulnerable.py.
 
FIX 1: SQL INJECTION -> PARAMETERISED QUERIES
----------------------------------------------
Instead of jamming user input into the SQL string directly,
we use placeholders (?) and pass the values separately.
The database treats them as plain text, never as SQL code.
No matter what the user types, it cannot become SQL.
 
FIX 2: SENSITIVE DATA EXPOSURE -> BCRYPT HASHING
--------------------------------------------------
Passwords are never stored in plain text.
We store a bcrypt hash instead. Even if someone steals the
database file, they get unreadable strings — the original
password cannot be recovered from a bcrypt hash.
 
FIX 3: BROKEN AUTHENTICATION -> SESSION CHECKS
-----------------------------------------------
Every protected route now checks that the user is actually
logged in before allowing access. If not logged in, they
are redirected back to the login page immediately.
"""


from flask import Flask, request, redirect, url_for, render_template, session
import sqlite3
import bcrypt
 
app = Flask(__name__)
app.secret_key = "elderease-super-secret-key-2025-not-guessable"
DB = "elderease_secure.db"
 
def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn
 
# FIX 3: a reusable helper that checks if the user is logged in
# we call this at the top of every protected route

def is_logged_in():
    return "user" in session


# ------------------------------------------------------------------
# ROUTE 1: LOGIN (FIXED — PARAMETERISED QUERIES + BCRYPT)
# ------------------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def login():
    error = None
 
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
 
        conn = get_db()
        cur = conn.cursor()