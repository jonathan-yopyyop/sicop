# Generated by Django 4.2.7 on 2024-01-23 01:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("budget", "0060_remove_commitment_approval_observation_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="commitmentrealeaseitems",
            name="budget_amount",
            field=models.FloatField(
                blank=True, default=0, help_text="Budget amount", null=True, verbose_name="Budget amount"
            ),
        ),
    ]