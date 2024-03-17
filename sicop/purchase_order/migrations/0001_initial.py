# Generated by Django 4.2.7 on 2024-01-11 21:29

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PurchaseOrder",
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
                    "IdOperac",
                    models.CharField(
                        blank=True, help_text="Operation ID", max_length=255, null=True, verbose_name="Operation ID"
                    ),
                ),
                (
                    "Numero",
                    models.CharField(blank=True, help_text="Number", max_length=255, null=True, verbose_name="Number"),
                ),
                ("Fecha", models.DateField(blank=True, help_text="Date", null=True, verbose_name="Date")),
                (
                    "FecContab",
                    models.DateField(
                        blank=True, help_text="Accountant date", null=True, verbose_name="Accountant date"
                    ),
                ),
                (
                    "FecVen",
                    models.DateField(blank=True, help_text="Expiry date", null=True, verbose_name="Expiry date"),
                ),
                (
                    "IdTercer",
                    models.CharField(
                        blank=True, help_text="Third ID", max_length=255, null=True, verbose_name="Third ID"
                    ),
                ),
                (
                    "IdActICA",
                    models.CharField(blank=True, help_text="ICA ID", max_length=255, null=True, verbose_name="ICA ID"),
                ),
                (
                    "IdRetFte",
                    models.CharField(
                        blank=True,
                        help_text="Withholding at source ID",
                        max_length=255,
                        null=True,
                        verbose_name="Withholding at source ID",
                    ),
                ),
                (
                    "VlrRetFte",
                    models.FloatField(
                        blank=True,
                        default=0,
                        help_text="Withholding at source value",
                        null=True,
                        verbose_name="Withholding at source value",
                    ),
                ),
                (
                    "FechaCruce",
                    models.DateField(blank=True, help_text="Crossing date", null=True, verbose_name="Crossing date"),
                ),
                (
                    "FactProvee",
                    models.CharField(
                        blank=True, help_text="Provider bill", max_length=255, null=True, verbose_name="Provider bill"
                    ),
                ),
                (
                    "FecEntrega",
                    models.DateField(blank=True, help_text="Delivery date", null=True, verbose_name="Delivery date"),
                ),
                (
                    "CostoTtal",
                    models.FloatField(
                        blank=True, default=0, help_text="Total cost", null=True, verbose_name="Total cost"
                    ),
                ),
                (
                    "VrBruto",
                    models.FloatField(
                        blank=True, default=0, help_text="Gross value", null=True, verbose_name="Gross value"
                    ),
                ),
                (
                    "VrDesc",
                    models.FloatField(
                        blank=True, default=0, help_text="Discount value", null=True, verbose_name="Discount value"
                    ),
                ),
                (
                    "VrIva",
                    models.FloatField(
                        blank=True, default=0, help_text="Tax value", null=True, verbose_name="Tax value"
                    ),
                ),
                (
                    "VrReteIva",
                    models.FloatField(
                        blank=True,
                        default=0,
                        help_text="VAT withholding value",
                        null=True,
                        verbose_name="VAT withholding value",
                    ),
                ),
                (
                    "VrReteIca",
                    models.FloatField(
                        blank=True,
                        default=0,
                        help_text="ICA retention value",
                        null=True,
                        verbose_name="ICA retention value",
                    ),
                ),
                (
                    "VrNeto",
                    models.FloatField(
                        blank=True, default=0, help_text="Net worth", null=True, verbose_name="Net worth"
                    ),
                ),
                (
                    "VrBaseImp",
                    models.FloatField(
                        blank=True, default=0, help_text="Tax base value", null=True, verbose_name="Tax base value"
                    ),
                ),
                (
                    "Direccion",
                    models.CharField(
                        blank=True, help_text="Address", max_length=255, null=True, verbose_name="Address"
                    ),
                ),
                (
                    "FecMod",
                    models.DateField(
                        blank=True, help_text="Modification date", null=True, verbose_name="Modification date"
                    ),
                ),
            ],
            options={
                "verbose_name": "Purchase Order",
                "verbose_name_plural": "Purchase Orders",
            },
        ),
    ]
