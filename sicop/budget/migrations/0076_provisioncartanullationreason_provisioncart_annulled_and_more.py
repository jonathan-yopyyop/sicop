# Generated by Django 4.2.7 on 2024-03-23 15:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("budget", "0075_rename_apprived_by_provisioncartapproval_approved_by"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProvisionCartAnullationReason",
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
                ("name", models.CharField(help_text="Name", max_length=255, verbose_name="Name")),
                (
                    "description",
                    models.TextField(blank=True, help_text="Description", null=True, verbose_name="Description"),
                ),
            ],
            options={
                "verbose_name": "Provision Cart Anullation Reason",
                "verbose_name_plural": "Provision Cart Anullations Reason",
            },
        ),
        migrations.AddField(
            model_name="provisioncart",
            name="annulled",
            field=models.BooleanField(default=False, help_text="Annulled", verbose_name="Annulled"),
        ),
        migrations.CreateModel(
            name="ProvisionCartAnullation",
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
                    "observation",
                    models.TextField(blank=True, help_text="Observation", null=True, verbose_name="Observation"),
                ),
                (
                    "anulled_by",
                    models.ForeignKey(
                        help_text="Anulled by",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="anulled_by_fk",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Anulled by",
                    ),
                ),
                (
                    "provision_cart",
                    models.ForeignKey(
                        help_text="Provision Cart",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="provision_cart_anullations",
                        to="budget.provisioncart",
                        verbose_name="Provision Cart",
                    ),
                ),
                (
                    "reason",
                    models.ForeignKey(
                        help_text="Reason",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reason_fk",
                        to="budget.provisioncartanullationreason",
                        verbose_name="Reason",
                    ),
                ),
            ],
            options={
                "verbose_name": "Provision Cart Anullation",
                "verbose_name_plural": "Provision Cart Anullations",
            },
        ),
    ]