# Generated by Django 4.2.7 on 2024-01-10 23:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("integration", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Contract",
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
                    "Estado",
                    models.CharField(blank=True, help_text="Estado", max_length=256, null=True, verbose_name="Estado"),
                ),
                (
                    "IdTercer",
                    models.CharField(
                        blank=True, help_text="IdTercer", max_length=256, null=True, verbose_name="IdTercer"
                    ),
                ),
                (
                    "IdCenCos",
                    models.CharField(
                        blank=True, help_text="IdCenCos", max_length=256, null=True, verbose_name="IdCenCos"
                    ),
                ),
                (
                    "IdTercer1",
                    models.CharField(
                        blank=True, help_text="IdTercer1", max_length=256, null=True, verbose_name="IdTercer1"
                    ),
                ),
                (
                    "MostrarAutori",
                    models.CharField(
                        blank=True, help_text="MostrarAutori", max_length=256, null=True, verbose_name="MostrarAutori"
                    ),
                ),
                (
                    "FechaCon",
                    models.CharField(
                        blank=True, help_text="FechaCon", max_length=256, null=True, verbose_name="FechaCon"
                    ),
                ),
                (
                    "FechaIni",
                    models.CharField(
                        blank=True, help_text="FechaIni", max_length=256, null=True, verbose_name="FechaIni"
                    ),
                ),
                (
                    "FechaFin",
                    models.CharField(
                        blank=True, help_text="FechaFin", max_length=256, null=True, verbose_name="FechaFin"
                    ),
                ),
                ("Objeto", models.TextField(blank=True, help_text="Objeto", null=True, verbose_name="Objeto")),
                (
                    "ValSinIVA",
                    models.CharField(
                        blank=True, help_text="ValSinIVA", max_length=256, null=True, verbose_name="ValSinIVA"
                    ),
                ),
                (
                    "ValIVA",
                    models.CharField(blank=True, help_text="ValIVA", max_length=256, null=True, verbose_name="ValIVA"),
                ),
                (
                    "ValTot",
                    models.CharField(blank=True, help_text="ValTot", max_length=256, null=True, verbose_name="ValTot"),
                ),
                ("Observ", models.TextField(blank=True, help_text="Observ", null=True, verbose_name="Observ")),
                (
                    "IdCompro",
                    models.CharField(
                        blank=True, help_text="IdCompro", max_length=256, null=True, verbose_name="IdCompro"
                    ),
                ),
                (
                    "NumCompro",
                    models.CharField(
                        blank=True, help_text="NumCompro", max_length=256, null=True, verbose_name="NumCompro"
                    ),
                ),
                (
                    "IdConGas",
                    models.CharField(
                        blank=True, help_text="IdConGas", max_length=256, null=True, verbose_name="IdConGas"
                    ),
                ),
                (
                    "IdUsuari",
                    models.CharField(
                        blank=True, help_text="IdUsuari", max_length=256, null=True, verbose_name="IdUsuari"
                    ),
                ),
                (
                    "Operac",
                    models.CharField(blank=True, help_text="Operac", max_length=256, null=True, verbose_name="Operac"),
                ),
                (
                    "FecMod",
                    models.CharField(blank=True, help_text="FecMod", max_length=256, null=True, verbose_name="FecMod"),
                ),
            ],
            options={
                "verbose_name": "Contract",
                "verbose_name_plural": "Contracts",
            },
        ),
    ]
