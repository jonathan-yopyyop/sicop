from django.db import models
from django.utils.translation import gettext_lazy as _

from config.models import BaseModel
from sicop.cost_center.models import CostCenter
from sicop.integration.models import Third


class Contract(BaseModel):
    """Model definition for Contract."""

    IdContrato = models.CharField(
        _("Contract ID"),
        help_text=_("Contract ID"),
        max_length=250,
        blank=True,
        null=True,
    )
    TipContrato = models.CharField(
        _("Contract Type"),
        help_text=_("Contract Type"),
        max_length=250,
        blank=True,
        null=True,
    )
    Cumplido = models.CharField(
        _("Compliment"),
        help_text=_("Compliment"),
        max_length=250,
        blank=True,
        null=True,
    )
    Estado = models.CharField(
        _("Contract Status"),
        help_text=_("Contract Status"),
        max_length=250,
        blank=True,
        null=True,
    )
    IdTercer = models.CharField(
        _("Third ID"),
        help_text=_("Third ID"),
        max_length=250,
        blank=True,
        null=True,
    )
    third = models.ForeignKey(
        Third,
        verbose_name=_("Third"),
        help_text=_("Third"),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    IdCenCos = models.CharField(
        _("Cost Center ID"),
        help_text=_("Cost Center ID"),
        max_length=250,
        blank=True,
        null=True,
    )
    cost_center = models.ForeignKey(
        CostCenter,
        verbose_name=_("Cost Center"),
        help_text=_("Cost Center"),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    FechaCon = models.DateField(
        _("Contract Date"),
        help_text=_("Contract Date"),
        blank=True,
        null=True,
    )
    FechaIni = models.DateField(
        _("Start Date"),
        help_text=_("Start Date"),
        blank=True,
        null=True,
    )
    FechaFin = models.DateField(
        _("Finish Date"),
        help_text=_("Finish Date"),
        blank=True,
        null=True,
    )
    Objeto = models.TextField(
        _("Object"),
        help_text=_("Object"),
        blank=True,
        null=True,
    )
    ValSinIVA = models.FloatField(
        _("Value Without Tax"),
        help_text=_("Value Without Tax"),
        blank=True,
        null=True,
        default=0,
    )
    ValIVA = models.FloatField(
        _("Tax Value"),
        help_text=_("Tax Value"),
        blank=True,
        null=True,
        default=0,
    )
    ValTot = models.FloatField(
        _("Total Value"),
        help_text=_("Total Value"),
        blank=True,
        null=True,
        default=0,
    )
    NumCompro = models.CharField(
        _("Voucher Number"),
        help_text=_("Voucher Number"),
        max_length=250,
        blank=True,
        null=True,
    )
    Operac = models.CharField(
        _("Operation"),
        help_text=_("Operation"),
        max_length=250,
        blank=True,
        null=True,
    )
    FecMod = models.DateField(
        _("Modification Date"),
        help_text=_("FecMod"),
        blank=True,
        null=True,
    )

    class Meta:
        """Meta definition for Contract."""

        verbose_name = _("Contract")
        verbose_name_plural = _("Contracts")

    def __str__(self):
        """Unicode representation of Contract."""
        return str(self.IdContrato)
