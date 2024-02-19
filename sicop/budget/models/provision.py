from django.db import models
from django.utils.translation import gettext_lazy as _

from config.models import BaseModel
from sicop.budget.models.budget import Budget
from sicop.project.models import Project


class ProvisionCart(BaseModel):
    """Model definition for Provision Cart."""

    project = models.ForeignKey(
        Project,
        verbose_name=_("Project"),
        help_text=_("Project"),
        related_name="project_provision_carts",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        "users.User",
        verbose_name=_("User"),
        help_text=_("User"),
        related_name="user_provision_carts",
        on_delete=models.CASCADE,
    )
    total_required_amount = models.FloatField(
        _("Total required amount"),
        help_text=_("Total required amount"),
        default=0,
        null=True,
        blank=True,
    )
    total_provisioned_amount = models.FloatField(
        _("Total provisioned amount"),
        help_text=_("Total provisioned amount"),
        default=0,
        null=True,
        blank=True,
    )
    total_missing_amount = models.FloatField(
        _("Total missing amount"),
        help_text=_("Total missing amount"),
        default=0,
        null=True,
        blank=True,
    )
    total_released_amount = models.FloatField(
        _("Total released amount"),
        help_text=_("Total released amount"),
        default=0,
        null=True,
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
        default=True,
    )
    rejected = models.BooleanField(
        _("Rejected"),
        help_text=_("Rejected"),
        default=False,
    )

    @property
    def real_total_provisioned_amount(self) -> float:
        return self.total_provisioned_amount
        # return self.total_provisioned_amount - self.total_released_amount

    class Meta:
        """Meta definition for Provision Cart."""

        verbose_name = _("Provision Cart")
        verbose_name_plural = _("Provision Carts")

    def __str__(self):
        """Unicode representation of Provision Cart."""
        return f" {self.id} {self.project}"


class ProvisionCartBudget(BaseModel):
    """Model definition for Provision Budget."""

    provision_cart = models.ForeignKey(
        ProvisionCart,
        verbose_name=_("Provision Cart"),
        help_text=_("Provision Cart"),
        related_name="provision_cart_provision_budgets",
        on_delete=models.CASCADE,
    )
    budget = models.ForeignKey(
        Budget,
        verbose_name=_("Budget"),
        help_text=_("Budget"),
        related_name="budget_provision_budgets",
        on_delete=models.CASCADE,
    )
    provosioned_amount = models.FloatField(
        _("Provosioned amount"),
        help_text=_("Provosioned amount"),
        default=0,
    )
    released_amount = models.FloatField(
        _("Released amount"),
        help_text=_("Released amount"),
        default=0,
    )
    available_budget = models.FloatField(
        _("Budget taked"),
        help_text=_("Budget taked"),
        default=0,
    )

    @property
    def real_provisioned_amount(self) -> float:
        return self.provosioned_amount
        # return self.provosioned_amount - self.released_amount

    class Meta:
        """Meta definition for Provision Budget."""

        verbose_name = _("Provision Budget")
        verbose_name_plural = _("Provision Budgets")
        unique_together = ("provision_cart", "budget")

    def __str__(self):
        """Unicode representation of Provision Budget."""
        return f"{self.provision_cart}"


class ProvisionCartApproval(BaseModel):
    """Model definition for Provision Cart Approval."""

    provision_cart = models.ForeignKey(
        ProvisionCart,
        verbose_name=_("Provision Cart"),
        help_text=_("Provision Cart"),
        related_name="provision_cart_provision_approval",
        on_delete=models.CASCADE,
    )
    must_be_approved_by = models.ForeignKey(
        "users.User",
        verbose_name=_("Must be approbed by"),
        help_text=_("Must be approbed by"),
        related_name="must_be_approved_by_fk",
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
    observation = models.TextField(
        _("Observation"),
        help_text=_("Observation"),
        default="",
    )

    class Meta:
        """Meta definition for Provision Cart Approval."""

        verbose_name = _("Provision Cart Approval")
        verbose_name_plural = _("Provision Cart Approvals")

    def __str__(self):
        """Unicode representation of Provision Cart Approval."""
        return f" {self.provision_cart.id} {self.provision_cart.project}"


# History models
class ProvisionCartHistory(BaseModel):
    """Model definition for Provision Cart History."""

    provision_cart = models.ForeignKey(
        ProvisionCart,
        verbose_name=_("Provision Cart"),
        help_text=_("Provision Cart"),
        related_name="provision_cart_history",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        "users.User",
        verbose_name=_("User"),
        help_text=_("User"),
        related_name="user_provision_history_carts",
        on_delete=models.CASCADE,
    )
    total_required_amount = models.FloatField(
        _("Total required amount"),
        help_text=_("Total required amount"),
        default=0,
        null=True,
        blank=True,
    )
    total_provisioned_amount = models.FloatField(
        _("Total provisioned amount"),
        help_text=_("Total provisioned amount"),
        default=0,
        null=True,
        blank=True,
    )
    total_missing_amount = models.FloatField(
        _("Total missing amount"),
        help_text=_("Total missing amount"),
        default=0,
        null=True,
        blank=True,
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
        default=True,
    )
    rejected = models.BooleanField(
        _("Rejected"),
        help_text=_("Rejected"),
        default=False,
    )

    class Meta:
        """Meta definition for Provision Cart History."""

        verbose_name = _("Provision Cart History")
        verbose_name_plural = _("Provision Cart Histories")

    def __str__(self):
        """Unicode representation of Provision Cart History."""
        return f" {self.id} {self.provision_cart.project}"


class ProvisionCartBudgetHistory(BaseModel):
    """Model definition for Provision Budget History."""

    provision_cart_history = models.ForeignKey(
        ProvisionCartHistory,
        verbose_name=_("Provision Cart"),
        help_text=_("Provision Cart"),
        related_name="provision_cart_provision_budgets",
        on_delete=models.CASCADE,
    )
    budget = models.ForeignKey(
        Budget,
        verbose_name=_("Budget"),
        help_text=_("Budget"),
        related_name="budget_provision_history_budgets",
        on_delete=models.CASCADE,
    )
    provosioned_amount = models.FloatField(
        _("Provosioned amount"),
        help_text=_("Provosioned amount"),
        default=0,
    )
    available_budget = models.FloatField(
        _("Budget taked"),
        help_text=_("Budget taked"),
        default=0,
    )

    class Meta:
        """Meta definition for Provision Budget history."""

        verbose_name = _("Provision Budget history")
        verbose_name_plural = _("Provision Budget histories")

    def __str__(self):
        """Unicode representation of Provision Budget history."""
        return f"{self.provision_cart_history}"
