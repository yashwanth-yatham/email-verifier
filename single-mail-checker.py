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
        print(f"MX lookup failed: {e}")
        return []

def verify_email_smtp(email, from_address='yashwanth@aasaan.app'):
    domain = email.split('@')[1]
    mx_hosts = get_mx_records(domain)

    if not mx_hosts:
        return False, "No MX records found"

    for host in mx_hosts:
        try:
            server = smtplib.SMTP(timeout=10)
            server.set_debuglevel(0)  # Change to 1 for debugging
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
        except (socket.timeout, smtplib.SMTPServerDisconnected, smtplib.SMTPConnectError) as e:
            return False, f"Connection failed: {e}"

    return False, "Unable to verify with any MX server"

# Example usage
email = "yashwanth@lightbooks.io"
if is_valid_syntax(email):
    valid, reason = verify_email_smtp(email)
    print(f"Result: {valid}, Reason: {reason}")
else:
    print("Invalid email syntax")
