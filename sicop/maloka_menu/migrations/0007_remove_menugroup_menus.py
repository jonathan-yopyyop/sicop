# Generated by Django 4.2.7 on 2024-03-20 03:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("maloka_menu", "0006_menugroup_created_at_menugroup_status_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="menugroup",
            name="menus",
        ),
    ]
