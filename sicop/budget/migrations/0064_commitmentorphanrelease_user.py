# Generated by Django 4.2.7 on 2024-02-03 01:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("budget", "0063_commitmentorphanrelease_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="commitmentorphanrelease",
            name="user",
            field=models.ForeignKey(
                default="",
                help_text="User",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_commitment_orphan_release",
                to=settings.AUTH_USER_MODEL,
                verbose_name="User",
            ),
            preserve_default=False,
        ),
    ]