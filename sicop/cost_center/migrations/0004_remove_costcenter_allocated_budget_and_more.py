# Generated by Django 4.2.5 on 2023-10-04 02:30

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("cost_center", "0003_delete_costcategory"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="costcenter",
            name="allocated_budget",
        ),
        migrations.RemoveField(
            model_name="costcenter",
            name="current_expenses",
        ),
    ]
