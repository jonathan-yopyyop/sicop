# Generated by Django 5.0 on 2023-12-13 23:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("budget", "0014_rename_budettransaction_budgetdecreasetransaction_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="provisioncart",
            name="observation",
            field=models.TextField(blank=True, help_text="Observation", null=True, verbose_name="Observation"),
        ),
    ]