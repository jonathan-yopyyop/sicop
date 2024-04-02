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
        default="",
    )
    approval_observation = models.TextField(
        _("Approval Observation"),
        help_text=_("Approval Observation"),
        null=True,
        blank=True,
        default="",
    )
    requires_approval = models.BooleanField(
        _("Requires approval"),
        help_text=_("Requires approval"),
        default=True,
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
    approved_by = models.ForeignKey(
        "users.User",
        verbose_name=_("Approved by"),
        help_text=_("Approved by"),
        related_name="+",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )
    rejected_by = models.ForeignKey(
        "users.User",
        verbose_name=_("Rejected by"),
        help_text=_("Rejected by"),
        related_name="+",
        on_delete=models.DO_NOTHING,
        null=True,
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
        default=True,
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


class BudgetAdditionApproval(BaseModel):
    """Model definition for Provision Cart Approval."""

    budget_addition = models.ForeignKey(
        BudgetAddition,
        verbose_name=_("Budget Addition"),
        help_text=_("Budget Addition"),
        related_name="budget_addition_approval",
        on_delete=models.CASCADE,
    )
    must_be_approved_by = models.ForeignKey(
        "users.User",
        verbose_name=_("Must be approbed by"),
        help_text=_("Must be approbed by"),
        related_name="budget_addition_must_be_approved_by_fk",
        on_delete=models.CASCADE,
    )
    approved = models.BooleanField(
        _("Approved?"),
        help_text=_("Approved?"),
        default=False,
    )
    rejected = models.BooleanField(
        _("Rejected"),
        help_text=_("Rejected"),
        default=False,
    )

    class Meta:
        """Meta definition for Provision Cart Approval."""

        verbose_name = _("Provision Cart Approval")
        verbose_name_plural = _("Provision Cart Approvals")

    def __str__(self):
        """Unicode representation of Provision Cart Approval."""
        return f" {self.provision_cart.id} {self.provision_cart.project}"
