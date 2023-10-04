from django.db import models
from django.utils.translation import gettext_lazy as _

from config.models import BaseModel
from sicop.area.models import Area


class CostCenter(BaseModel):
    """Model definition for CostCenter."""

    cost_center_id = models.CharField(
        _("Cost Center ID"),
        help_text=_("Cost Center ID"),
        max_length=150,
        unique=True,
    )
    name = models.CharField(
        _("Cost Center name"),
        help_text=_("Cost Center name"),
        max_length=150,
    )
    description = models.TextField(
        _("Cost Center description"),
        help_text=_("Cost Center description"),
        blank=True,
        null=True,
    )
    area = models.ForeignKey(
        Area,
        verbose_name=_("Area"),
        help_text=_("Area"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        """Meta definition for CostCenter."""

        verbose_name = _("Cost Center")
        verbose_name_plural = _("Cost Centers")

    def __str__(self):
        """Unicode representation of CostCenter."""
        return self.name
