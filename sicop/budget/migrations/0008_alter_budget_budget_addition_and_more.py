# Generated by Django 4.2.7 on 2023-11-16 18:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("budget", "0007_remove_budget_cost_center_budget_cost_centers"),
    ]

    operations = [
        migrations.AlterField(
            model_name="budget",
            name="budget_addition",
            field=models.FloatField(default=0, help_text="Budget addition", verbose_name="Budget addition"),
        ),
        migrations.AlterField(
            model_name="budget",
            name="budget_decrease",
            field=models.FloatField(default=0, help_text="Budget decrease", verbose_name="Budget decrease"),
        ),
        migrations.AlterField(
            model_name="budget",
            name="initial_value",
            field=models.FloatField(default=0, help_text="Initial value", verbose_name="Initial value"),
        ),
        migrations.AlterField(
            model_name="budget",
            name="unit_value",
            field=models.FloatField(default=0, help_text="Unit value", verbose_name="Unit value"),
        ),
    ]