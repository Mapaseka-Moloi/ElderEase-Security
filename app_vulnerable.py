"""
VULNERABLE VERSION — ElderEase Admin App
=========================================
VULNERABILITY 1: SQL INJECTION
  Username: ' OR 1=1 --
  Password: anything

VULNERABILITY 2: SENSITIVE DATA EXPOSURE
  Open elderease_vulnerable.db — passwords are plain text

VULNERABILITY 3: BROKEN AUTHENTICATION
  Go to http://localhost:5000/transactions without logging in

WARNING: Intentionally insecure. Local demo only.
"""

from flask import Flask, request, redirect, url_for, render_template, session
import sqlite3

app = Flask(__name__)
app.secret_key = "notsecret"
DB = "elderease_vulnerable.db"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cur = conn.cursor()

        # VULNERABILITY: user input goes directly into the SQL string
        # Normal: username=admin, password=password123
        #   -> WHERE username = 'admin' AND password = 'password123'
        #   -> finds the user, login works
        #
        # Attack: username = ' OR 1=1 --
        #   -> WHERE username = '' OR 1=1 --' AND password = '...'
        #   -> 1=1 is always true, -- comments out the password check
        #   -> returns all users, attacker logs in as the first one

        query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"

        print(f"\n[VULNERABLE] Query executed:\n{query}\n")

        user = cur.execute(query).fetchone()
        conn.close()

        if user:
            session["user"] = dict(user)["username"]
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid username or password."

    return render_template("login.html", error=error)

@app.route("/dashboard")
def dashboard():
    # VULNERABILITY 3: NO SESSION CHECK
    conn = get_db()
    cur = conn.cursor()
    total = cur.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
    elderly = cur.execute("SELECT COUNT(*) FROM transactions WHERE sender_age >= 60").fetchone()[0]
    failed = cur.execute("SELECT COUNT(*) FROM transactions WHERE status = 'Failed'").fetchone()[0]
    conn.close()
    username = session.get("user", "Unknown (not logged in)")
    return render_template("dashboard.html", username=username, total=total, elderly=elderly, failed=failed, vulnerable=True)

@app.route("/transactions")
def transactions():
    # VULNERABILITY 3: NO SESSION CHECK
    conn = get_db()
    cur = conn.cursor()
    rows = cur.execute("SELECT * FROM transactions").fetchall()
    conn.close()
    return render_template("transactions.html", transactions=rows, vulnerable=True)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    print("=" * 55)
    print("  ELDEREASE VULNERABLE APP — FOR DEMO PURPOSES ONLY")
    print("  Running at: http://localhost:5000")
    print("=" * 55)
    print("\nVulnerabilities in this version:")
    print("  1. SQL Injection on login form")
    print("  2. Plain text passwords in database")
    print("  3. No session checks on protected routes")
    print("\nSQL Injection attack — use this as username:")
    print("  ' OR 1=1 --")
    print("  (any password)\n")
    app.run(debug=True, port=5000)