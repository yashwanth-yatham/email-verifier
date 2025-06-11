#Python Bulk Email Verifier

This project provides a Python script to verify a list of email addresses in bulk using three steps:

1. Syntax Validation (Regex)
2. DNS MX Record Check
3. SMTP Email Verification

---

##Features

- Read email addresses from a CSV file
- Validate syntax using regex
- Check domain MX (Mail Exchange) records
- Perform SMTP verification (connects to mail server)
- Save results in a new CSV file
- Handles common exceptions gracefully

---
---

##Limitations

SMTP servers may use protections like greylisting or catch-all addresses

Some servers always return “valid” even for fake addresses

Avoid verifying too many emails quickly from the same IP to prevent blacklisting

---

##Requirements

- Python 3.7 or higher
- Install the required package:

```bash
pip install dnspython
