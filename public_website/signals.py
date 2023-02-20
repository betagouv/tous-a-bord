from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import User
from public_website.utils import obfuscate, email_provider



@receiver(post_save, sender=User)
def notify_team_that_user_is_created(
    instance: User, created: bool, **_
):
    if not created:
        return
    email_provider.send_user_creation_email(obfuscate.obfuscate_email(instance.email))
