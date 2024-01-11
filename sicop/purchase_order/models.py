from django.db import models
from django.utils.translation import gettext_lazy as _

from config.models import BaseModel


class PurchaseOrder(BaseModel):
    """Model definition for Purchase Order."""

    IdOperac = models.CharField(
        _("Operation ID"),
        help_text=_("Operation ID"),
        null=True,
        blank=True,
        max_length=255,
    )
    Numero = models.CharField(
        _("Number"),
        help_text=_("Number"),
        null=True,
        blank=True,
        max_length=255,
    )
    Fecha = models.DateTimeField(
        _("Date"),
        help_text=_("Date"),
        null=True,
        blank=True,
    )
    FecContab = models.DateTimeField(
        _("Accountant date"),
        help_text=_("Accountant date"),
        null=True,
        blank=True,
    )
    FecVen = models.DateTimeField(
        _("Expiry date"),
        help_text=_("Expiry date"),
        null=True,
        blank=True,
    )
    IdTercer = models.CharField(
        _("Third ID"),
        help_text=_("Third ID"),
        null=True,
        blank=True,
        max_length=255,
    )
    IdActICA = models.CharField(
        _("ICA ID"),
        help_text=_("ICA ID"),
        null=True,
        blank=True,
        max_length=255,
    )
    IdRetFte = models.CharField(
        _("Withholding at source ID"),
        help_text=_("Withholding at source ID"),
        null=True,
        blank=True,
        max_length=255,
    )
    VlrRetFte = models.FloatField(
        _("Withholding at source value"),
        help_text=_("Withholding at source value"),
        null=True,
        blank=True,
        default=0,
    )
    FechaCruce = models.DateTimeField(
        _("Crossing date"),
        help_text=_("Crossing date"),
        null=True,
        blank=True,
    )
    FactProvee = models.CharField(
        _("Provider bill"),
        help_text=_("Provider bill"),
        null=True,
        blank=True,
        max_length=255,
    )
    FecEntrega = models.DateTimeField(
        _("Delivery date"),
        help_text=_("Delivery date"),
        null=True,
        blank=True,
    )
    CostoTtal = models.FloatField(
        _("Total cost"),
        help_text=_("Total cost"),
        null=True,
        blank=True,
        default=0,
    )
    VrBruto = models.FloatField(
        _("Gross value"),
        help_text=_("Gross value"),
        null=True,
        blank=True,
        default=0,
    )
    VrDesc = models.FloatField(
        _("Discount value"),
        help_text=_("Discount value"),
        null=True,
        blank=True,
        default=0,
    )
    VrIva = models.FloatField(
        _("Tax value"),
        help_text=_("Tax value"),
        null=True,
        blank=True,
        default=0,
    )
    VrReteIva = models.FloatField(
        _("VAT withholding value"),
        help_text=_("VAT withholding value"),
        null=True,
        blank=True,
        default=0,
    )
    VrReteIca = models.FloatField(
        _("ICA retention value"),
        help_text=_("ICA retention value"),
        null=True,
        blank=True,
        default=0,
    )
    VrNeto = models.FloatField(
        _("Net worth"),
        help_text=_("Net worth"),
        null=True,
        blank=True,
        default=0,
    )
    VrBaseImp = models.FloatField(
        _("Tax base value"),
        help_text=_("Tax base value"),
        null=True,
        blank=True,
        default=0,
    )
    Direccion = models.CharField(
        _("Address"),
        help_text=_("Address"),
        null=True,
        blank=True,
        max_length=255,
    )
    FecMod = models.DateTimeField(
        _("Modification date"),
        help_text=_("Modification date"),
        null=True,
        blank=True,
    )

    class Meta:
        """Meta definition for Purchase Order."""

        verbose_name = _("Purchase Order")
        verbose_name_plural = _("Purchase Orders")

    def __str__(self):
        """Unicode representation of Purchase Order."""
        return str(self.id)
