from django.core.management.base import BaseCommand

from public_website.utils import sms_provider


class Command(BaseCommand):
    help = "Send sms notifications"

    def add_arguments(self, parser):
        parser.add_argument("number")

    def handle(self, *args, **options):
        sms_provider.send_notification_sms(options["number"])
        self.stdout.write(self.style.SUCCESS("SMS sent."))
