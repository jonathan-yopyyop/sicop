from django.db import models
from django.utils.translation import gettext_lazy as _

from config.models import BaseModel
from sicop.cost_center.models import CostCenter


class BusinessUnit(BaseModel):
    """Model definition for Business Unit."""

    code = models.SlugField(
        _("Code"),
        help_text=_("Code"),
        max_length=150,
        blank=True,
        null=True,
    )
    cost_centers = models.ManyToManyField(
        CostCenter,
        verbose_name=_("Cost centers"),
        help_text=_("Cost centers"),
        related_name="cost_centers_business_units",
    )
    name = models.CharField(
        _("Name"),
        help_text=_("Name"),
        max_length=150,
    )

    class Meta:
        """Meta definition for Business Unit."""

        verbose_name = _("Business Unit")
        verbose_name_plural = _("Business Units")

    def __str__(self):
        """Unicode representation of Business Unit."""
        return self.name
