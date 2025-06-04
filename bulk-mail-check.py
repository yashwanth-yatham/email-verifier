import csv
import re
import dns.resolver
import smtplib
import socket

def is_valid_syntax(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None

def get_mx_records(domain):
    try:
        answers = dns.resolver.resolve(domain, 'MX')
        return [r.exchange.to_text() for r in answers]
    except Exception as e:
        return []

def is_valid_domain(domain):
    try:
        socket.gethostbyname(domain)
        return True
    except socket.gaierror:
        return False

def verify_email_smtp(email, from_address='yashwanth@aasaan.app'):
    domain = email.split('@')[-1]
    
    if not is_valid_domain(domain):
        return False, "Domain resolution failed"

    mx_hosts = get_mx_records(domain)
    if not mx_hosts:
        return False, "No MX records found"

    for host in mx_hosts:
        try:
            server = smtplib.SMTP(timeout=10)
            server.connect(host)
            server.helo()
            server.mail(from_address)
            code, message = server.rcpt(email)
            server.quit()

            if code == 250:
                return True, "Email address is valid"
            elif code == 550:
                return False, "Email address does not exist"
            else:
                return False, f"SMTP response: {code} {message.decode()}"
        except (socket.timeout, smtplib.SMTPException, socket.gaierror) as e:
            continue  # Try next MX record

    return False, "Unable to verify with any MX server"

def process_emails_from_csv(input_file='emails.csv', output_file='email_verification_results.csv'):
    results = []

    with open(input_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            email = row.get('email', '').strip()
            if not email:
                continue

            syntax_valid = is_valid_syntax(email)
            if syntax_valid:
                smtp_valid, reason = verify_email_smtp(email)
            else:
                smtp_valid = False
                reason = "Invalid syntax"

            results.append({
                'email': email,
                'syntax_valid': syntax_valid,
                'smtp_valid': smtp_valid,
                'reason': reason
            })
            print(f"Checked: {email}, Syntax: {syntax_valid}, SMTP: {smtp_valid}, Reason: {reason}")

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['email', 'syntax_valid', 'smtp_valid', 'reason']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"\n✅ Finished processing. Results saved to '{output_file}'.")

process_emails_from_csv('emails.csv')
