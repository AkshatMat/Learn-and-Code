import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 465))

def send_email(recipient: str, subject: str, body: str):
    try:
        if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
            print("Email configuration missing. Please check EMAIL_ADDRESS and EMAIL_PASSWORD in .env file")
            return False
            
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = recipient

        with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        print(f"Email sent successfully to {recipient}")
        return True
    except Exception as e:
        print(f"Failed to send email to {recipient}: {e}")
        return False
