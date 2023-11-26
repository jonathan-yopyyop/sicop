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
        _("Total provisioned amount"),
        help_text=_("Total provisioned amount"),
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
        _("Total provisioned amount"),
        help_text=_("Total provisioned amount"),
        default=0,
        null=True,
        blank=True,
    )

    class Meta:
        """Meta definition for Provision Cart."""

        verbose_name = "Provision Cart"
        verbose_name_plural = "Provision Carts"

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

    class Meta:
        """Meta definition for Provision Budget."""

        verbose_name = "Provision Budget"
        verbose_name_plural = "Provision Budgets"
        unique_together = ("provision_cart", "budget")

    def __str__(self):
        """Unicode representation of Provision Budget."""
        return f"{self.provision_cart}"
