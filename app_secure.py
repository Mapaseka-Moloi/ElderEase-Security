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


        # FIX 1: PARAMETERISED QUERY
        # The ? placeholder is filled in safely by SQLite itself.
        # Whatever the user types is treated as a plain text value,
        # never as executable SQL code.
        # ' OR 1=1 -- typed as a username becomes the literal
        # string "' OR 1=1 --" — it won't match any username,
        # so the query returns nothing and login fails.
        cur.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        )
        user = cur.fetchone()
        conn.close()
 
        if user:
            # FIX 2: BCRYPT PASSWORD CHECK
            # We never compare plain text passwords.
            # bcrypt.checkpw() hashes the entered password and
            # compares it to the stored hash — if they match,
            # the password is correct. The original password
            # is never stored anywhere.
            stored_hash = dict(user)["password_hash"].encode("utf-8")
            password_correct = bcrypt.checkpw(
                password.encode("utf-8"),
                stored_hash
            )
 
            if password_correct:
                session["user"] = dict(user)["username"]
                return redirect(url_for("dashboard"))
 
        error = "Invalid username or password."
 
    return render_template("login.html", error=error)


# ------------------------------------------------------------------
# ROUTE 2: DASHBOARD (FIXED — SESSION CHECK)
# ------------------------------------------------------------------
@app.route("/dashboard")
def dashboard():
    # FIX 3: SESSION CHECK
    # If the user is not logged in, redirect to login immediately.
    # The page content is never shown to unauthenticated users.
    if not is_logged_in():
        return redirect(url_for("login"))
 
    conn = get_db()
    cur = conn.cursor()
    total = cur.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
    elderly = cur.execute("SELECT COUNT(*) FROM transactions WHERE sender_age >= 60").fetchone()[0]
    failed = cur.execute("SELECT COUNT(*) FROM transactions WHERE status = 'Failed'").fetchone()[0]
    conn.close()
 
    return render_template(
        "dashboard.html",
        username=session["user"],
        total=total,
        elderly=elderly,
        failed=failed,
        vulnerable=False
    )

 
# ------------------------------------------------------------------
# ROUTE 3: TRANSACTIONS (FIXED — SESSION CHECK)
# ------------------------------------------------------------------
@app.route("/transactions")
def transactions():
    # FIX 3: SESSION CHECK
    # Unauthenticated users cannot access transaction data.
    if not is_logged_in():
        return redirect(url_for("login"))
 
    conn = get_db()
    cur = conn.cursor()
    rows = cur.execute("SELECT * FROM transactions").fetchall()
    conn.close()
 
    return render_template(
        "transactions.html",
        transactions=rows,
        vulnerable=False
    )
 
