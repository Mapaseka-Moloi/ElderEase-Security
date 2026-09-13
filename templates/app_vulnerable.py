
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

