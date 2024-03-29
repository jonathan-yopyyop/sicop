# Generated by Django 4.2.7 on 2023-11-16 20:56

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ExpenseConcept",
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
                    "code",
                    models.SlugField(blank=True, help_text="Code", max_length=150, null=True, verbose_name="Code"),
                ),
                ("name", models.CharField(help_text="Name", max_length=150, verbose_name="Name")),
            ],
            options={
                "verbose_name": "Expense Concept",
                "verbose_name_plural": "Expense Concepts",
            },
        ),
    ]
