# Generated by Django 4.2.7 on 2024-03-20 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("maloka_menu", "0008_menu_group"),
    ]

    operations = [
        migrations.AddField(
            model_name="menuoption",
            name="url_complement",
            field=models.CharField(
                default="/", help_text="URL complement", max_length=250, verbose_name="URL complement"
            ),
        ),
    ]