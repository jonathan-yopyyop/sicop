# Generated by Django 5.0 on 2023-12-18 20:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("budget", "0022_budgetdecreasetransaction_requiered_amount"),
    ]

    operations = [
        migrations.AddField(
            model_name="budget",
            name="budget_decrease_control",
            field=models.FloatField(default=0, help_text="Budget decrease", verbose_name="Budget decrease"),
        ),
    ]
