import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_PORT = 1025
SMTP_SERVER = "localhost"

FROM_EMAIL = "mad2ap@example.com"

def send_mail(to, subject, body):
    msg = MIMEMultipart()
    msg['From'] = FROM_EMAIL
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.sendmail(FROM_EMAIL, to, msg.as_string())
    return "Mail sent successfully!"

if __name__ == "__main__":
    to = "user@gmail.com"
    subject = "Test Email"
    body = "<h1>This is a test email</h1><p>Hello, User!</p> <a href='http://localhost:5173'>Click here to vist app</a>"
    send_mail(to, subject, body)