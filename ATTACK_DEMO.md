ElderEase Security — Attack Demo Cheat Sheet

This document is your step-by-step guide for the live demo. Follow it in order. Each attack has three parts:

Show the vulnerability exists
Demonstrate the attack
Show the fix blocks it

SETUP (do this before the demo starts)
bash
# 1. Create both databases
python setup_db.py

# 2. Have two terminal tabs ready:
#    Tab 1: python app_vulnerable.py  (port 5000)
#    Tab 2: ready to run app_secure.py

Open your browser at http://localhost:5000

ATTACK 1 — SQL Injection
Step 1: Run the vulnerable app
bash
python app_vulnerable.py

Step 2: Show normal login works
Username: admin
Password: password123
✅ Login succeeds — show the dashboard

Step 3: Log out, then demonstrate the attack
Username: ' OR 1=1 --
Password: wrongpassword
✅ Login succeeds WITHOUT a valid password

password
Step 4: Show WHY it worked (point at the terminal)

The terminal prints the actual query that ran:

sql
SELECT * FROM users WHERE username = '' OR 1=1 --' AND password = 'wrongpassword'

Explain: 1=1 is always true, -- comments out the password check. The database returned a user without checking the password at all.

Step 5: Switch to the secure app and show it's blocked
bash
# Ctrl+C to stop vulnerable app, then:
python app_secure.py
Username: ' OR 1=1 --
Password: wrongpassword
❌ Login fails — "Invalid username or password"

ATTACK 2 — Sensitive Data Exposure
Step 1: Show the vulnerable database (plain text passwords)

Open a new terminal and run:

bash
python -c "
import sqlite3
conn = sqlite3.connect('elderease_vulnerable.db')
rows = conn.execute('SELECT username, password FROM users').fetchall()
for row in rows:
    print(row)
conn.close()
"

Output will show:

('admin', 'password123')
('staff', 'letmein')
('manager', 'admin2024')

Step 2: Show the secure database (hashed passwords)
bash
python -c "
import sqlite3
conn = sqlite3.connect('elderease_secure.db')
rows = conn.execute('SELECT username, password_hash FROM users').fetchall()
for row in rows:
    print(row[0], row[1][:40], '...')
conn.close()
"

Output will show:

admin $2b$12$YPQ6lfv9sek/H/ixlr1PT. ...
staff $2b$12$wdp5Lbpd4HMoQ1PZTxYpCe ...
manager $2b$12$DoUIKv/Nnibdoc40WZ10G ...
