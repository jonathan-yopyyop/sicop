# Generated by Django 4.2.7 on 2024-04-02 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("budget", "0078_alter_provisioncartbudget_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="provisioncartbudgethistory",
            options={"verbose_name": "Provision history budget", "verbose_name_plural": "Provision history budgets"},
        ),
    ]