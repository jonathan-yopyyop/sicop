from django.db import models
from django.utils.translation import gettext_lazy as _

from config.models import BaseModel
from sicop.budget.models.budget import Budget


class BudgetRedistribution(BaseModel):
    """Model definition for Budget Redistribution."""

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
    budget = models.ForeignKey(
        Budget,
        verbose_name=_("Budget"),
        help_text=_("Budget"),
        related_name="budget_budget_redistributions",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    original_amount = models.FloatField(
        _("Original amount"),
        help_text=_("Original amount"),
        default=0,
        null=True,
        blank=True,
    )
    redistributed_amount = models.FloatField(
        _("Redistributed amount"),
        help_text=_("Redistributed amount"),
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
    observation = models.TextField(
        _("Observation"),
        help_text=_("Observation"),
        null=True,
        blank=True,
    )
    approval_observation = models.TextField(
        _("Approval observation"),
        help_text=_("Approval observation"),
        null=True,
        blank=True,
        default="",
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
        related_name="user_budget_redistributions",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )

    class Meta:
        """Meta definition for Budget Redistribution."""

        verbose_name = _("Budget Redistribution")
        verbose_name_plural = _("Budget Redistributions")

    def __str__(self):
        """Unicode representation of Budget Redistribution."""
        return f"{self.budget}"


class BudgetRedistributionItem(BaseModel):
    """Model definition for Budget Redistribution Item."""

    budget_redistribution = models.ForeignKey(
        BudgetRedistribution,
        verbose_name=_("Budget Redistribution"),
        help_text=_("Budget Redistribution"),
        related_name="budget_redistribution_budget_redistribution_items",
        on_delete=models.CASCADE,
    )
    budget = models.ForeignKey(
        Budget,
        verbose_name=_("Budget"),
        help_text=_("Budget"),
        related_name="budget_budget_redistribution_items",
        on_delete=models.DO_NOTHING,
    )
    original_amount = models.FloatField(
        _("Original amount"),
        help_text=_("Original amount"),
        default=0,
        null=True,
        blank=True,
    )
    redistributed_amount = models.FloatField(
        _("Redistributed amount"),
        help_text=_("Redistributed amount"),
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
    must_be_approved_by = models.ForeignKey(
        "users.User",
        verbose_name=_("Must be approved by"),
        help_text=_("Must be approved by"),
        related_name="user_budget_redistribution_items",
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
        """Meta definition for Budget Redistribution Item."""

        verbose_name = _("Budget Redistribution Item")
        verbose_name_plural = _("Budget Redistribution Items")

    def __str__(self):
        """Unicode representation of Budget Redistribution Item."""
        return str(self.id)


class BudgetRedistributionItemApproval(BaseModel):
    """Model definition for Budget Redistribution Item Approval."""

    budget_redistribution_item = models.ForeignKey(
        BudgetRedistributionItem,
        verbose_name=_("Budget Redistribution Item"),
        help_text=_("Budget Redistribution Item"),
        related_name="budget_redistribution_item_budget_redistribution_item_approvals",
        on_delete=models.CASCADE,
    )
    observation = models.TextField(
        _("Observation"),
        help_text=_("Observation"),
        null=True,
        blank=True,
        default="",
    )
    approved = models.BooleanField(
        _("Approved"),
        help_text=_("Approved"),
        default=False,
    )

    class Meta:
        """Meta definition for Budget Redistribution Item Approval."""

        verbose_name = _("Budget Redistribution Item Approval")
        verbose_name_plural = _("Budget Redistribution Item Approvals")

    def __str__(self):
        """Unicode representation of Budget Redistribution Item Approval."""
        return str(self.id)
