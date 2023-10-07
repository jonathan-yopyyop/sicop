# Generated by Django 4.2.5 on 2023-09-29 15:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("integration", "0003_activeintegration"),
    ]

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
                    "IdConGas",
                    models.CharField(
                        blank=True, help_text="IdConGas", max_length=150, null=True, verbose_name="IdConGas"
                    ),
                ),
                (
                    "Nombre",
                    models.CharField(blank=True, help_text="Nombre", max_length=150, null=True, verbose_name="Nombre"),
                ),
                (
                    "Nemoni",
                    models.CharField(blank=True, help_text="Nemoni", max_length=150, null=True, verbose_name="Nemoni"),
                ),
                (
                    "TipoPresup",
                    models.CharField(
                        blank=True, help_text="TipoPresup", max_length=150, null=True, verbose_name="TipoPresup"
                    ),
                ),
                (
                    "IdRetFte",
                    models.CharField(
                        blank=True, help_text="IdRetFte", max_length=150, null=True, verbose_name="IdRetFte"
                    ),
                ),
                (
                    "IdTipGas",
                    models.CharField(
                        blank=True, help_text="IdTipGas", max_length=150, null=True, verbose_name="IdTipGas"
                    ),
                ),
                (
                    "IdConGasDistrib",
                    models.CharField(
                        blank=True,
                        help_text="IdConGasDistrib",
                        max_length=150,
                        null=True,
                        verbose_name="IdConGasDistrib",
                    ),
                ),
                (
                    "CtGtoCauPag",
                    models.CharField(
                        blank=True, help_text="CtGtoCauPag", max_length=150, null=True, verbose_name="CtGtoCauPag"
                    ),
                ),
                (
                    "ECtGtoCauPag",
                    models.CharField(
                        blank=True, help_text="ECtGtoCauPag", max_length=150, null=True, verbose_name="ECtGtoCauPag"
                    ),
                ),
                (
                    "IdTipIVA",
                    models.CharField(
                        blank=True, help_text="IdTipIVA", max_length=150, null=True, verbose_name="IdTipIVA"
                    ),
                ),
                (
                    "PorIva",
                    models.CharField(blank=True, help_text="PorIva", max_length=150, null=True, verbose_name="PorIva"),
                ),
                (
                    "CodEquival",
                    models.CharField(
                        blank=True, help_text="CodEquival", max_length=150, null=True, verbose_name="CodEquival"
                    ),
                ),
                (
                    "CtGastos",
                    models.CharField(
                        blank=True, help_text="CtGastos", max_length=150, null=True, verbose_name="CtGastos"
                    ),
                ),
                (
                    "ECtGastos",
                    models.CharField(
                        blank=True, help_text="ECtGastos", max_length=150, null=True, verbose_name="ECtGastos"
                    ),
                ),
                (
                    "EsBaseImpto",
                    models.CharField(
                        blank=True, help_text="EsBaseImpto", max_length=150, null=True, verbose_name="EsBaseImpto"
                    ),
                ),
                (
                    "ValorBase",
                    models.CharField(
                        blank=True, help_text="ValorBase", max_length=150, null=True, verbose_name="ValorBase"
                    ),
                ),
                (
                    "ValorMax",
                    models.CharField(
                        blank=True, help_text="ValorMax", max_length=150, null=True, verbose_name="ValorMax"
                    ),
                ),
                (
                    "IdConMedMag",
                    models.CharField(
                        blank=True, help_text="IdConMedMag", max_length=150, null=True, verbose_name="IdConMedMag"
                    ),
                ),
                (
                    "Campo1",
                    models.CharField(blank=True, help_text="Campo1", max_length=150, null=True, verbose_name="Campo1"),
                ),
                (
                    "IdUsuari",
                    models.CharField(
                        blank=True, help_text="IdUsuari", max_length=150, null=True, verbose_name="IdUsuari"
                    ),
                ),
                (
                    "Operac",
                    models.CharField(blank=True, help_text="Operac", max_length=150, null=True, verbose_name="Operac"),
                ),
                (
                    "FecMod",
                    models.CharField(blank=True, help_text="FecMod", max_length=150, null=True, verbose_name="FecMod"),
                ),
            ],
            options={
                "verbose_name": "Expense Concept",
                "verbose_name_plural": "Expense Concepts",
            },
        ),
        migrations.RemoveField(
            model_name="businessunit",
            name="Campo1",
        ),
        migrations.RemoveField(
            model_name="businessunit",
            name="CodEquival",
        ),
        migrations.RemoveField(
            model_name="businessunit",
            name="CtGastos",
        ),
        migrations.RemoveField(
            model_name="businessunit",
            name="CtGtoCauPag",
        ),
        migrations.RemoveField(
            model_name="businessunit",
            name="ECtGastos",
        ),
        migrations.RemoveField(
            model_name="businessunit",
            name="ECtGtoCauPag",
        ),
        migrations.RemoveField(
            model_name="businessunit",
            name="EsBaseImpto",
        ),
        migrations.RemoveField(
            model_name="businessunit",
            name="IdConGas",
        ),
        migrations.RemoveField(
            model_name="businessunit",
            name="IdConGasDistrib",
        ),
        migrations.RemoveField(
            model_name="businessunit",
            name="IdConMedMag",
        ),
        migrations.RemoveField(
            model_name="businessunit",
            name="IdRetFte",
        ),
        migrations.RemoveField(
            model_name="businessunit",
            name="IdTipGas",
        ),
        migrations.RemoveField(
            model_name="businessunit",
            name="IdTipIVA",
        ),
        migrations.RemoveField(
            model_name="businessunit",
            name="PorIva",
        ),
        migrations.RemoveField(
            model_name="businessunit",
            name="TipoPresup",
        ),
        migrations.RemoveField(
            model_name="businessunit",
            name="ValorBase",
        ),
        migrations.RemoveField(
            model_name="businessunit",
            name="ValorMax",
        ),
        migrations.AddField(
            model_name="businessunit",
            name="IdTipCen",
            field=models.CharField(
                blank=True, help_text="IdTipCen", max_length=150, null=True, verbose_name="IdTipCen"
            ),
        ),
    ]
