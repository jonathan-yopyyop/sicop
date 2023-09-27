from django.db import models
from django.utils.translation import gettext_lazy as _

from config.models import BaseModel


class Third(BaseModel):
    """Model definition for Third."""

    code = models.CharField(
        _("Code"),
        help_text=_("Code"),
        max_length=150,
        unique=True,
    )
    first_name = models.CharField(
        _("First name"),
        help_text=_("First name"),
        max_length=150,
    )
    last_name = models.CharField(
        _("Last name"),
        help_text=_("Last name"),
        max_length=150,
    )

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        """Meta definition for Third."""

        verbose_name = "Third"
        verbose_name_plural = "Thirds"

    def __str__(self):
        """Unicode representation of Third."""
        return f"{self.first_name} {self.last_name}"


class CostCenter(BaseModel):
    """Model definition for Cost Center."""

    code = models.CharField(
        _("Code"),
        help_text=_("Code"),
        max_length=150,
        unique=True,
    )
    name = models.CharField(
        _("Name"),
        help_text=_("Name"),
        max_length=150,
    )

    class Meta:
        """Meta definition for Cost Center."""

        verbose_name = "Cost Center"
        verbose_name_plural = "Cost Centers"

    def __str__(self):
        """Unicode representation of Cost Center."""
        return self.name


class BusinessUnit(BaseModel):
    """Model definition for Business Unit."""

    code = models.CharField(
        _("Code"),
        help_text=_("Code"),
        max_length=150,
        unique=True,
    )
    name = models.CharField(
        _("Name"),
        help_text=_("Name"),
        max_length=150,
    )

    class Meta:
        """Meta definition for Business Unit."""

        verbose_name = "Business Unit"
        verbose_name_plural = "Business Units"

    def __str__(self):
        """Unicode representation of Business Unit."""
        return self.name


class ExpenseType(BaseModel):
    """Model definition for Expense Type."""

    code = models.CharField(
        _("Code"),
        help_text=_("Code"),
        max_length=150,
        unique=True,
    )
    name = models.CharField(
        _("Name"),
        help_text=_("Name"),
        max_length=150,
    )

    class Meta:
        """Meta definition for Expense Type."""

        verbose_name = "Expense Type"
        verbose_name_plural = "Expense Types"

    def __str__(self):
        """Unicode representation of Expense Type."""
        return self.name
