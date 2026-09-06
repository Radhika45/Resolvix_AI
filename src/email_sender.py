import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from src.logger import logger

load_dotenv()

def send_customer_email(recipient_email: str, subject: str, body: str) -> bool:
    """
    Sends an automated email response to the extracted customer email address
    using radhika581arora@gmail.com as the sender.
    """
    if not recipient_email or recipient_email.lower() in ["not found", "unknown", "none"]:
        logger.error("Skipping email dispatch: No valid recipient email provided.")
        return False

    # Sender setup
    sender_email = os.getenv("SMTP_USERNAME", "radhika581arora@gmail.com")
    smtp_password = os.getenv("SMTP_PASSWORD")
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))

    if not smtp_password:
        logger.error("SMTP_PASSWORD is missing from environment variables.")
        return False

    try:
        # Create message container
        msg = MIMEMultipart()
        msg["From"] = f"Customer Support <{sender_email}>"
        msg["To"] = recipient_email
        msg["Subject"] = subject

        # Attach email body
        msg.attach(MIMEText(body, "plain", "utf-8"))

        # Connect to Gmail SMTP server
        logger.info(f"Connecting to SMTP server {smtp_server}:{smtp_port}...")
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure connection
            server.login(sender_email, smtp_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())

        logger.info(f"Email successfully delivered from {sender_email} to {recipient_email}!")
        return True

    except Exception as e:
        logger.error(f"Failed to deliver email to {recipient_email} via SMTP: {str(e)}")
        return False