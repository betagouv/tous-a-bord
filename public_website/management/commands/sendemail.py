from django.core.management.base import BaseCommand

from public_website.utils import email_provider


class Command(BaseCommand):
    help = "Send email notifications"

    def add_arguments(self, parser):
        parser.add_argument("email")
        parser.add_argument("--name", default=None)

    def handle(self, *args, **options):
        email_provider.send_notification_email(options["email"], options["name"])
        self.stdout.write(self.style.SUCCESS("Email sent."))
