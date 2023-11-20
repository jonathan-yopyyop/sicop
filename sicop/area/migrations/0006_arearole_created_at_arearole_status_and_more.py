# Generated by Django 4.2.7 on 2023-11-08 18:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("area", "0005_arearole"),
    ]

    operations = [
        migrations.AddField(
            model_name="arearole",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True,
                default=datetime.datetime(2023, 11, 8, 18, 29, 34, 556240, tzinfo=datetime.timezone.utc),
                help_text="Date time on which the object was created.",
                verbose_name="created at",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="arearole",
            name="status",
            field=models.BooleanField(
                default=True, help_text="Designates whether this record is active or not.", verbose_name="status"
            ),
        ),
        migrations.AddField(
            model_name="arearole",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True, help_text="Date time on which the object was last updated.", verbose_name="updated at"
            ),
        ),
    ]