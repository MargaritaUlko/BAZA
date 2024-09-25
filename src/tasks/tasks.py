import logging
from celery import Celery
import smtplib
from email.message import EmailMessage
from config import SMTP_USER, SMTP_USER2, SMTP_PASSWORD
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

celery = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
    include=['src.tasks.tasks']
)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# @celery.task

def send_email_report_dashboard():
    email = EmailMessage()
    email['Subject'] = "Маша жопка"
    email['From'] = SMTP_USER
    email['To'] = SMTP_USER2

    email.set_content('Это факт!!!! Маша писюнья')
    return email

# @celery.task

def show_email_report_dashboard():
    logger.info("Starting to send email...")
    # email = send_email_report_dashboard().delay()
    email = send_email_report_dashboard()
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)
    logger.info("Email sent.")
