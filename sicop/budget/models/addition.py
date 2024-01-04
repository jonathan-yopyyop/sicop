from django.db import models
from django.utils.translation import gettext_lazy as _

from config.models import BaseModel
from sicop.budget.models.budget import Budget


class BudgetAddition(BaseModel):
    """Model definition for Budget Addition."""

    user = models.ForeignKey(
        "users.User",
        verbose_name=_("User"),
        help_text=_("User"),
        related_name="+",
        on_delete=models.DO_NOTHING,
    )
    finished = models.BooleanField(
        _("Finished"),
        help_text=_("Finished"),
        default=False,
    )
    observation = models.TextField(
        _("Observation"),
        help_text=_("Observation"),
        null=True,
        blank=True,
    )
    requires_approval = models.BooleanField(
        _("Requires approval"),
        help_text=_("Requires approval"),
        default=False,
    )
    approved = models.BooleanField(
        _("Approved"),
        help_text=_("Approved"),
        default=False,
    )
    rejected = models.BooleanField(
        _("Rejected"),
        help_text=_("Rejected"),
        default=False,
    )
    must_be_approved_by = models.ForeignKey(
        "users.User",
        verbose_name=_("Must be approved by"),
        help_text=_("Must be approved by"),
        related_name="+",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )

    class Meta:
        """Meta definition for Budget Addition."""

        verbose_name = _("Budget Addition")
        verbose_name_plural = _("Budget Additions")

    def __str__(self):
        """Unicode representation of Budget Addition."""
        return str(self.id)


class BudgetAdditionItem(BaseModel):
    """Model definition for Budget Addition Item."""

    budget_addition = models.ForeignKey(
        BudgetAddition,
        verbose_name=_("Budget addition item"),
        help_text=_("Budget addition item"),
        on_delete=models.DO_NOTHING,
    )
    budget = models.ForeignKey(
        Budget,
        verbose_name=_("Budget"),
        help_text=_("Budget"),
        on_delete=models.DO_NOTHING,
    )
    original_amount = models.FloatField(
        _("Original amount"),
        help_text=_("Original amount"),
        default=0,
        null=True,
        blank=True,
    )
    added_amount = models.FloatField(
        _("Added amount"),
        help_text=_("Added amount"),
        default=0,
        null=True,
        blank=True,
    )
    new_amount = models.FloatField(
        _("New amount"),
        help_text=_("New amount"),
        default=0,
        null=True,
        blank=True,
    )
    requires_approval = models.BooleanField(
        _("Requires approval"),
        help_text=_("Requires approval"),
        default=False,
    )
    approved = models.BooleanField(
        _("Approved"),
        help_text=_("Approved"),
        default=False,
    )
    rejected = models.BooleanField(
        _("Rejected"),
        help_text=_("Rejected"),
        default=False,
    )
    must_be_approved_by = models.ForeignKey(
        "users.User",
        verbose_name=_("Must be approved by"),
        help_text=_("Must be approved by"),
        related_name="+",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )
    processed = models.BooleanField(
        _("Processed"),
        help_text=_("Processed"),
        default=False,
    )

    class Meta:
        """Meta definition for Budget Addition Item."""

        verbose_name = _("Budget Addition Item")
        verbose_name_plural = _("Budget Addition Items")

    def __str__(self):
        """Unicode representation of Budget Addition Item."""
        return str(self.id)
