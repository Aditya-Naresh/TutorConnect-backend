from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import send_mails_to_user
from .models import User


@receiver(post_save, sender=User)
def send_signup_email_on_signup(sender, instance, created, **kwargs):
    if created:
        print("Sending mail")
        send_mails_to_user.delay(instance.id)
