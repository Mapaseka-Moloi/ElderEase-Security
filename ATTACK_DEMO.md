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