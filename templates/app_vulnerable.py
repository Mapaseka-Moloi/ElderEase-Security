
App vulnerable · PY
"""
VULNERABLE VERSION — ElderEase Admin App
=========================================
This version of the app contains THREE deliberate security
vulnerabilities for demonstration purposes.
 
VULNERABILITY 1: SQL INJECTION
--------------------------------
The login form builds its SQL query using string formatting,
directly inserting whatever the user types into the query.
An attacker can type malicious SQL code into the login field
and bypass authentication entirely — no password needed.
 
Attack to demonstrate:
  Username: ' OR '1'='1' --
  Password: anything
 
VULNERABILITY 2: SENSITIVE DATA EXPOSURE
-----------------------------------------
Passwords are stored in plain text in the database.
Anyone who gains access to the database file can read
every password immediately — no cracking needed.
 
Attack to demonstrate:
  Open elderease_vulnerable.db and read the users table.
 
VULNERABILITY 3: BROKEN AUTHENTICATION
----------------------------------------
The /dashboard and /transactions routes have NO session checks.
Anyone can navigate directly to these URLs without logging in
and view all sensitive transaction data.
 
Attack to demonstrate:
  Go directly to http://localhost:5000/transactions
  without logging in first.
 
WARNING: This app is intentionally insecure.
Never use this code in a real system.
Run on localhost only, never deploy to the internet.
"""


from flask import Flask, request, redirect, url_for, render_template, session
import sqlite3
 
app = Flask(__name__)
app.secret_key = "notsecret"  # VULNERABILITY: weak secret key
 
DB = "elderease_vulnerable.db"
 
def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


# ------------------------------------------------------------------
# ROUTE 1: LOGIN (VULNERABLE TO SQL INJECTION)
# ------------------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def login():
    error = None
 
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
 
        conn = get_db()
        cur = conn.cursor()
 

        # VULNERABILITY 1: SQL INJECTION
        # We are building the query by jamming the user's input
        # directly into the SQL string using an f-string.
        # Whatever the user types becomes part of the SQL command.
        #
        # Normal login:
        #   username = admin, password = password123
        #   query = "SELECT * FROM users WHERE username = 'admin'
        #            AND password = 'password123'"
        #
        # SQL injection attack:
        #   username = ' OR '1'='1' --
        #   password = anything
        #   query = "SELECT * FROM users WHERE username = ''
        #            OR '1'='1' --' AND password = 'anything'"
        #   The -- comments out the rest of the query.
        #   '1'='1' is always true, so the WHERE clause is always
        #   true, so the database returns ALL users — and the
        #   attacker is logged in as the first one.

        query = f"""
            SELECT * FROM users
            WHERE username = '{username}'
            AND password = '{password}'
        """
 
        print(f"\n[VULNERABLE] Query executed:\n{query}\n")
 
        user = cur.execute(query).fetchone()
        conn.close()
 
        if user:
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid username or password."
 
    return render_template("login.html", error=error)


# ------------------------------------------------------------------
# ROUTE 2: DASHBOARD (NO SESSION CHECK — BROKEN AUTHENTICATION)
# ------------------------------------------------------------------
@app.route("/dashboard")
def dashboard():
    # VULNERABILITY 3: BROKEN AUTHENTICATION
    # There is NO check here that the user is actually logged in.
    # Anyone can type http://localhost:5000/dashboard directly
    # into their browser and access this page without credentials.
 
    conn = get_db()
    cur = conn.cursor()
    total = cur.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
    elderly = cur.execute("SELECT COUNT(*) FROM transactions WHERE sender_age >= 60").fetchone()[0]
    failed = cur.execute("SELECT COUNT(*) FROM transactions WHERE status = 'Failed'").fetchone()[0]
    conn.close()
 
    username = session.get("user", "Unknown (not logged in)")
 
    return render_template(
        "dashboard.html",
        username=username,
        total=total,
        elderly=elderly,
        failed=failed,
        vulnerable=True
    )


# ------------------------------------------------------------------
# ROUTE 3: TRANSACTIONS (NO SESSION CHECK — BROKEN AUTHENTICATION)
# ------------------------------------------------------------------
@app.route("/transactions")
def transactions():
    # VULNERABILITY 3 (again): No session check.
    # Anyone can access all transaction records directly
    # by navigating to http://localhost:5000/transactions
    # without ever logging in.
 
    conn = get_db()
    cur = conn.cursor()
    rows = cur.execute("SELECT * FROM transactions").fetchall()
    conn.close()
 
    return render_template(
        "transactions.html",
        transactions=rows,
        vulnerable=True
    )