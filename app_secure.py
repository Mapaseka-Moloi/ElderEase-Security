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