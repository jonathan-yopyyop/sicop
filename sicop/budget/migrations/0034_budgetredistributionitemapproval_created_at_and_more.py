# Generated by Django 4.2.7 on 2023-12-26 13:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("budget", "0033_budgetredistributionitemapproval"),
    ]

    operations = [
        migrations.AddField(
            model_name="budgetredistributionitemapproval",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True,
                default=datetime.datetime(2023, 12, 26, 13, 14, 50, 898953, tzinfo=datetime.timezone.utc),
                help_text="Date time on which the object was created.",
                verbose_name="created at",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="budgetredistributionitemapproval",
            name="status",
            field=models.BooleanField(
                default=True, help_text="Designates whether this record is active or not.", verbose_name="status"
            ),
        ),
        migrations.AddField(
            model_name="budgetredistributionitemapproval",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True, help_text="Date time on which the object was last updated.", verbose_name="updated at"
            ),
        ),
    ]
