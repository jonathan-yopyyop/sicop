# Generated by Django 4.2.7 on 2024-01-11 03:45

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("contract", "0002_contract_cost_center_contract_third"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="contract",
            name="cost_center",
        ),
        migrations.RemoveField(
            model_name="contract",
            name="third",
        ),
    ]