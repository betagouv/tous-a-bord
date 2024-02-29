from django.core.management.base import BaseCommand

from public_website.models import User


class Command(BaseCommand):
    help = "Make all users admin"

    def handle(self, *args, **options):
        todo = [u for u in User.objects.all() if not u.is_superuser]
        for u in todo:
            u.is_staff = True
            u.is_admin = True
            u.is_superuser = True
            u.save()

        self.stdout.write(self.style.SUCCESS(f"{len(todo)} users were made admins."))
