from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import User
from public_website.utils.email_provider import send_user_creation_email


@receiver(post_save, sender=User)
def notify_team_that_user_is_created(
    instance: User, created: bool, **_
):
    if not created:
        return
    send_user_creation_email(instance.get_email_field_name())
    