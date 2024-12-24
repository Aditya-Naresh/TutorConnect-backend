from django.conf import settings
from django.core.mail import EmailMessage, BadHeaderError
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from smtplib import SMTPException
import logging
from django.contrib.auth import get_user_model
import environ

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env()

logger = logging.getLogger(__name__)

frontend = env("FRONTEND")

User = get_user_model()


def send_normal_email(data):
    try:
        email = EmailMessage(
            subject=data["email_subject"],
            body=data["email_body"],
            from_email=settings.EMAIL_HOST_USER,
            to=[data["to_email"]],
        )

        email.send(fail_silently=False)
        logger.info("Email sent successfully to %s", data["to_email"])

    except BadHeaderError:
        logger.error("Invalid header found when sending email.")

    except SMTPException as e:
        logger.error("SMTPException occurred: %s", e)

    except Exception as e:
        logger.error("An unexpected error occurred: %s", e)


def send_verification_email(user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        logger.error("User with id %s does not exist.", user_id)
        return

    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    verified_link = f"{frontend}/verify-email/{uid}/{token}"
    full_name = user.get_full_name()
    message = f"""
    Hi {full_name},

    Please click the link below to verify your email address:
    {verified_link}

    If you did not request this, please ignore this email.

    Thank you!
    """

    email = EmailMessage(
        subject="Email Confirmation",
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email],
    )
    email.send(fail_silently=False)
