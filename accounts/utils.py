from django.conf import settings
from django.core.mail import EmailMessage, BadHeaderError
from smtplib import SMTPException
import logging

logger = logging.getLogger(__name__)

def send_normal_email(data):
    try:
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            from_email=settings.EMAIL_HOST_USER,
            to=[data['to_email']]
        )
        
        email.send(fail_silently=False)
        logger.info("Email sent successfully to %s", data['to_email'])
        
    except BadHeaderError:
        logger.error("Invalid header found when sending email.")
        
    except SMTPException as e:
        logger.error("SMTPException occurred: %s", e)
        
    except Exception as e:
        logger.error("An unexpected error occurred: %s", e)
