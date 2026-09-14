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
