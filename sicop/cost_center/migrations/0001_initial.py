# Generated by Django 4.2.5 on 2023-09-25 12:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("area", "0004_rename_areamembers_areamember_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="CostCategory",
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
                    "name",
                    models.CharField(
                        help_text="Cost Category name", max_length=150, unique=True, verbose_name="Cost Category name"
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="Cost Category description",
                        null=True,
                        verbose_name="Cost Category description",
                    ),
                ),
            ],
            options={
                "verbose_name": "Cost Category",
                "verbose_name_plural": "Cost Categories",
            },
        ),
        migrations.CreateModel(
            name="CostCenter",
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
                    "cost_center_id",
                    models.CharField(
                        help_text="Cost Center ID", max_length=150, unique=True, verbose_name="Cost Center ID"
                    ),
                ),
                (
                    "name",
                    models.CharField(help_text="Cost Center name", max_length=150, verbose_name="Cost Center name"),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="Cost Center description",
                        null=True,
                        verbose_name="Cost Center description",
                    ),
                ),
                (
                    "allocated_budget",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        help_text="Allocated Budget",
                        max_digits=20,
                        verbose_name="Allocated Budget",
                    ),
                ),
                (
                    "current_expenses",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        help_text="Current Expenses",
                        max_digits=20,
                        verbose_name="Current Expenses",
                    ),
                ),
                (
                    "area",
                    models.ForeignKey(
                        blank=True,
                        help_text="Area",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="area.area",
                        verbose_name="Area",
                    ),
                ),
                (
                    "cost_category",
                    models.ForeignKey(
                        blank=True,
                        help_text="Cost Category",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cost_center.costcategory",
                        verbose_name="Cost Category",
                    ),
                ),
            ],
            options={
                "verbose_name": "Cost Center",
                "verbose_name_plural": "Cost Centers",
            },
        ),
    ]
