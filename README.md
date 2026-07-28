# ElderEase Security — Ethical Hacking & Vulnerability Assessment

## Overview

This project is a cybersecurity extension of the ElderEase Transfers data engineering pipeline. It takes the same concept — a financial transaction system used by elderly and low-literacy users — and asks a different question:

**"If this system were real, how easily could it be attacked, and how do we fix it?"**

The project demonstrates three real-world vulnerabilities found in financial systems, attacks each one live, then applies security fixes and proves the attacks no longer work. This is called a **penetration test** (or pen test) — ethical hacking performed on your own system to find weaknesses before a real attacker does.

---

## The Two Versions

| Version | File | Description |
|---|---|---|
| Vulnerable | `app_vulnerable.py` | Deliberately insecure version of the system |
| Secure | `app_secure.py` | Hardened version with all vulnerabilities patched |

Both versions run as a local web application. The vulnerable version is intentionally broken — it exists only to demonstrate attacks. The secure version shows the fixes applied and proves each attack now fails.

---

## The Three Vulnerabilities Demonstrated

### 1. SQL Injection
**What it is:** An attacker types malicious SQL code into an input field (e.g. a search box or login form), tricking the database into returning data it shouldn't — or bypassing authentication entirely.

**Why it matters for ElderEase:** The transaction database holds sensitive data: names, ages, amounts sent, and receiver details for hundreds of elderly users. A SQL injection attack could expose all of it in seconds.

**Demo:** Attacker types `' OR '1'='1` into the login field and gets in without a valid password.

**Fix:** Use parameterised queries — the database treats user input as plain text, never as executable code.

---

### 2. Sensitive Data Exposure
**What it is:** Private data (passwords, ID numbers, financial details) is stored in plain text in the database, so anyone who gains access to the database file can read everything immediately.

**Why it matters for ElderEase:** Elderly users' transaction amounts, receiver names, and personal details sitting unencrypted is a serious privacy violation — especially for a vulnerable population.

**Demo:** Open the database file directly and read plain-text passwords and sensitive transaction data.

**Fix:** Hash passwords using bcrypt. Sensitive fields are never stored in plain text.

---

### 3. Broken Authentication
**What it is:** The system has no proper session management — once you're "logged in," there's nothing stopping someone from accessing any page directly by typing the URL, even without credentials.

**Why it matters for ElderEase:** An admin dashboard showing all elderly users' transaction history should never be accessible without a valid, verified login — but without session management, any URL is publicly accessible.

**Demo:** Navigate directly to `/admin/transactions` without logging in and view all transaction data.

**Fix:** Implement Flask session management with login-required decorators on protected routes.

---

## Tech Stack

- **Python 3** — core language
- **Flask** — lightweight web framework (creates the local web app to attack)
- **SQLite** — database storing transaction data
- **bcrypt** — password hashing library used in the secure version

---

## How to Run

### Install dependencies
```bash
pip3 install -r requirements.txt
```

### Run the vulnerable version (for demonstrating attacks)
```bash
python3 app_vulnerable.py
```
Open your browser and go to: `http://localhost:5000`

### Run the secure version (for demonstrating fixes)
```bash
python3 app_secure.py
```
Open your browser and go to: `http://localhost:5000`

⚠️ Never run both at the same time — they use the same port.

---

## Project Structure

```
elderease-security/
│
├── app_vulnerable.py       ← deliberately insecure app (for attack demos)
├── app_secure.py           ← hardened app (for fix demos)
├── setup_db.py             ← creates the database with sample data
├── requirements.txt        ← Python dependencies
└── templates/              ← HTML pages for the web app
    ├── login.html
    ├── dashboard.html
    └── transactions.html
```

---

## Honest Scope

This is a **local demonstration environment** — nothing here is deployed to the internet or connected to real financial data. The vulnerable app is intentionally broken for educational purposes only. All attacks are performed against a system I built and own, on a local machine, which is the definition of ethical hacking.

---

## Connection to ElderEase Transfers

This project directly extends the data engineering pipeline built in [ElderEase Transfers](https://github.com/Mapaseka-Moloi/ElderEase-transfers). That project proved *where* the friction is for elderly users using data. This project asks: *if that system were built, how secure would it be?* Together they form a complete picture — from data pipeline to security audit.

---

## Future Work

- Demonstrate Cross-Site Scripting (XSS) vulnerability
- Add rate limiting to prevent brute force login attacks
- Implement HTTPS (SSL/TLS) for data in transit

---

## Author

Mapaseka — WeThinkCode_ Cybersecurity Elective Project