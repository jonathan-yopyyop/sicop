# Generated by Django 4.2.6 on 2023-10-08 03:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="status",
            field=models.BooleanField(default=True, verbose_name="Status"),
        ),
    ]
