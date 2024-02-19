# Generated by Django 4.2.7 on 2024-01-14 14:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("budget", "0051_remove_commitmentrelease_total_to_released_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="commitment",
            name="tax_amount",
            field=models.FloatField(
                blank=True, default=0, help_text="Tax amount", null=True, verbose_name="Tax amount"
            ),
        ),
    ]
