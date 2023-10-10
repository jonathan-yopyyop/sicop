from django.db import models
from django.utils.translation import gettext_lazy as _

from config.models import BaseModel
from sicop.expense_concept.models import ExpenseConcept


class ExpenseType(BaseModel):
    """Model definition for Expense Type."""

    code = models.SlugField(
        _("Code"),
        help_text=_("Code"),
        max_length=250,
        null=True,
        blank=True,
    )
    name = models.CharField(
        _("Name"),
        help_text=_("Name"),
        max_length=150,
    )
    expense_concepts = models.ManyToManyField(
        ExpenseConcept,
        verbose_name=_("Expense Concepts"),
        help_text=_("Expense Concepts"),
        related_name="expense_concepts",
    )

    class Meta:
        """Meta definition for Expense Type."""

        verbose_name = "Expense Type"
        verbose_name_plural = "Expense Types"

    def __str__(self):
        """Unicode representation of Expense Type."""
        return self.name
