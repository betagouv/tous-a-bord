# Generated by Django 4.2.10 on 2024-03-19 15:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("public_website", "0012_alter_import_user_alter_item_import_instance"),
    ]

    operations = [
        migrations.CreateModel(
            name="Export",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="exports",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]