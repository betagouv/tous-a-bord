# Generated by Django 3.2.17 on 2023-02-14 10:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("public_website", "0003_rename_peid_apicall_queried_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="apicall",
            old_name="url",
            new_name="uri",
        ),
    ]
