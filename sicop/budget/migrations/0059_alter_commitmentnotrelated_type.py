# Generated by Django 4.2.7 on 2024-01-18 02:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("budget", "0058_alter_commitmentnotrelated_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="commitmentnotrelated",
            name="type",
            field=models.CharField(
                blank=True,
                choices=[("CT", "Contract"), ("PO", "Purchase order"), ("CO", "Consumption"), ("LG", "Legalization")],
                help_text="Type",
                max_length=2,
                null=True,
                verbose_name="Type",
            ),
        ),
    ]
