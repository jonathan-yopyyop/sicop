# Generated by Django 4.2.7 on 2024-01-10 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("budget", "0043_budgetaddition_approval_observation_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="BudgetAddtionTransaction",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "status",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this record is active or not.",
                        verbose_name="status",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="Date time on which the object was created.",
                        verbose_name="created at",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True,
                        help_text="Date time on which the object was last updated.",
                        verbose_name="updated at",
                    ),
                ),
                (
                    "original_amount",
                    models.FloatField(default=0, help_text="Original amount", verbose_name="Original amount"),
                ),
                ("added_amount", models.FloatField(default=0, help_text="Added amount", verbose_name="Added amount")),
                ("new_amount", models.FloatField(default=0, help_text="New amount", verbose_name="New amount")),
                (
                    "addition_item",
                    models.ForeignKey(
                        help_text="addition item",
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="addition_item_budget_addition_transactions",
                        to="budget.budgetadditionitem",
                        verbose_name="addition item",
                    ),
                ),
                (
                    "budget",
                    models.ForeignKey(
                        help_text="Budget",
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="budget.budget",
                        verbose_name="Budget",
                    ),
                ),
            ],
            options={
                "verbose_name": "Budget Addition Transaction",
                "verbose_name_plural": "Budget Addition Transactions",
            },
        ),
    ]
