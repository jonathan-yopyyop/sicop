from django.db import models
from django.utils.translation import gettext_lazy as _

from config.models import BaseModel


class ExpenseConcept(BaseModel):
    """Model definition for Expense Concept."""

    code = models.SlugField(
        _("Code"),
        help_text=_("Code"),
        max_length=150,
        blank=True,
        null=True,
    )
    name = models.CharField(
        _("Name"),
        help_text=_("Name"),
        max_length=150,
    )

    class Meta:
        """Meta definition for Expense Concept."""

        verbose_name = _("Expense Concept")
        verbose_name_plural = _("Expense Concepts")

    def __str__(self):
        """Unicode representation of Expense Concept."""
        return self.name
