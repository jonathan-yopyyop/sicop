# Generated by Django 4.2.7 on 2024-02-21 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("budget", "0070_commitment_total_released"),
    ]

    operations = [
        migrations.AddField(
            model_name="provisioncartbudget",
            name="alreaday_taked_amount",
            field=models.FloatField(
                default=0, help_text="Alreaday taked amount", verbose_name="Alreaday taked amount"
            ),
        ),
    ]