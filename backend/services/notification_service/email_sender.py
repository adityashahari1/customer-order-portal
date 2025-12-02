import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from backend.shared.logger import get_logger

logger = get_logger(__name__)

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

def send_email(to_email: str, subject: str, content: str):
    if not SENDGRID_API_KEY:
        logger.warning("SENDGRID_API_KEY not set, skipping email")
        return

    message = Mail(
        from_email='noreply@customerorderportal.com',
        to_emails=to_email,
        subject=subject,
        html_content=content)
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        logger.info(f"Email sent to {to_email}, status code: {response.status_code}")
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
