from celery import shared_task
from .utils import send_verification_email
import logging

# Set up logger
logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_mails_to_user(self, user_id):
    """
    Celery task to send a verification email to a user.
    This task will retry up to 3 times with a 60-second delay if it fails.
    """
    logger.info("Task Started for user_id: %s", user_id)
    try:
        send_verification_email(user_id)
        logger.info("Email sent successfully to user_id: %s", user_id)
        return f"Email sent to user {user_id} successfully."

    except Exception as e:
        # Log any errors that occur during the email sending process
        logger.error("Error sending email to user_id: %s, Error: %s", user_id, e)

        # Retry the task if an error occurs
        raise self.retry(exc=e)
