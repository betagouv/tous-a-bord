# Generated by Django 3.2.18 on 2023-07-13 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("public_website", "0008_apicall_habilitation"),
    ]

    operations = [
        migrations.AlterField(
            model_name="habilitation",
            name="token",
            field=models.TextField(),
        ),
    ]
