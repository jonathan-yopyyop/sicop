from django.db import models
from django.utils.translation import gettext_lazy as _

from config.models import BaseModel
from sicop.area.models import Area


class CostCategory(BaseModel):
    """Model definition for Cost Category."""

    name = models.CharField(
        _("Cost Category name"),
        help_text=_("Cost Category name"),
        max_length=150,
        unique=True,
    )
    description = models.TextField(
        _("Cost Category description"),
        help_text=_("Cost Category description"),
        blank=True,
        null=True,
    )

    class Meta:
        """Meta definition for Cost Category."""

        verbose_name = "Cost Category"
        verbose_name_plural = "Cost Categories"

    def __str__(self):
        """Unicode representation of Cost Category."""
        pass


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
    cost_category = models.ForeignKey(
        CostCategory,
        verbose_name=_("Cost Category"),
        help_text=_("Cost Category"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    area = models.ForeignKey(
        Area,
        verbose_name=_("Area"),
        help_text=_("Area"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    allocated_budget = models.DecimalField(
        _("Allocated Budget"),
        help_text=_("Allocated Budget"),
        max_digits=10,
        decimal_places=2,
        default=0,
    )
    current_expenses = models.DecimalField(
        _("Current Expenses"),
        help_text=_("Current Expenses"),
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    class Meta:
        """Meta definition for CostCenter."""

        verbose_name = _("Cost Center")
        verbose_name_plural = _("Cost Centers")

    def __str__(self):
        """Unicode representation of CostCenter."""
        return self.name
