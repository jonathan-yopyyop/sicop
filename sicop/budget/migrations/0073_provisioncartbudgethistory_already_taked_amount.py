# Generated by Django 4.2.7 on 2024-02-21 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("budget", "0072_remove_provisioncartbudget_alreaday_taked_amount"),
    ]

    operations = [
        migrations.AddField(
            model_name="provisioncartbudgethistory",
            name="already_taked_amount",
            field=models.FloatField(
                default=0, help_text="Alreaday taked amount", verbose_name="Alreaday taked amount"
            ),
        ),
    ]
