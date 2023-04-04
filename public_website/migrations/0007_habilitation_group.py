# Generated by Django 3.2.18 on 2023-03-29 12:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("public_website", "0006_habilitation"),
    ]

    operations = [
        migrations.AddField(
            model_name="habilitation",
            name="group",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="habilitation",
                to="auth.group",
            ),
            preserve_default=False,
        ),
    ]
