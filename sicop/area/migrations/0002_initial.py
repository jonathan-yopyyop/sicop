# Generated by Django 4.2.7 on 2023-11-16 20:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("area", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="areamember",
            name="user",
            field=models.ForeignKey(
                help_text="User",
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="User",
            ),
        ),
    ]
