# Generated by Django 4.2.5 on 2023-09-25 12:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Contractor",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("first_name", models.CharField(help_text="First name", max_length=150, verbose_name="First name")),
                ("last_name", models.CharField(help_text="Last name", max_length=150, verbose_name="Last name")),
                ("email", models.EmailField(help_text="Email", max_length=254, verbose_name="Email")),
                ("phone", models.CharField(help_text="Phone", max_length=150, verbose_name="Phone")),
                (
                    "address",
                    models.CharField(
                        blank=True, help_text="Address", max_length=150, null=True, verbose_name="Address"
                    ),
                ),
                ("dni", models.CharField(help_text="DNI", max_length=150, unique=True, verbose_name="DNI")),
                (
                    "contractor_type",
                    models.CharField(
                        choices=[("1", "Natural Person"), ("2", "Legal Person")],
                        help_text="Contractor type",
                        max_length=150,
                        verbose_name="Contractor type",
                    ),
                ),
            ],
            options={
                "verbose_name": "Contractor",
                "verbose_name_plural": "Contractors",
            },
        ),
        migrations.CreateModel(
            name="ContractorFile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("file", models.FileField(help_text="File", upload_to="contractor_files", verbose_name="File")),
                (
                    "contractor",
                    models.ForeignKey(
                        help_text="Contractor",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contractor.contractor",
                        verbose_name="Contractor",
                    ),
                ),
            ],
            options={
                "verbose_name": "Contractor File",
                "verbose_name_plural": "Contractor Files",
            },
        ),
    ]
