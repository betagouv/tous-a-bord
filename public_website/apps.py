from django.apps import AppConfig


class public_websiteConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "public_website"

    def ready(self):
        import public_website.signals
