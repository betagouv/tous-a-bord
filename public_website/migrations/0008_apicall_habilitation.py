# Generated by Django 3.2.18 on 2023-03-29 15:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("public_website", "0007_habilitation_group"),
    ]

    operations = [
        migrations.AddField(
            model_name="apicall",
            name="habilitation",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="uses",
                to="public_website.habilitation",
            ),
            preserve_default=False,
        ),
    ]
