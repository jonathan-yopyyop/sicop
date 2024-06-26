from django.db import models
from django.utils.translation import gettext_lazy as _

from config.models import BaseModel
from sicop.business_unit.models import BusinessUnit
from sicop.cost_center.models import CostCenter
from sicop.expense_type.models import ExpenseConcept
from sicop.project.models import Project


class BudgetDescription(BaseModel):
    """Model definition for Budget Description."""

    expense_concept = models.ForeignKey(
        ExpenseConcept,
        verbose_name=_("Expense concept"),
        help_text=_("Expense concept"),
        related_name="expense_concepts_budgets",
        on_delete=models.CASCADE,
    )
    description = models.TextField(
        _("Description"),
        help_text=_("Description"),
    )

    class Meta:
        """Meta definition for Budget Description."""

        verbose_name = _("Budget Description")
        verbose_name_plural = _("Budget Descriptions")

    def __str__(self):
        """Unicode representation of Budget Description."""
        return self.description


class Budget(BaseModel):
    """Model definition for Budget."""

    project = models.ForeignKey(
        Project,
        verbose_name=_("Project"),
        help_text=_("Project"),
        related_name="project_budgets",
        on_delete=models.CASCADE,
    )
    cost_centers = models.ManyToManyField(
        CostCenter,
        verbose_name=_("Cost centers"),
        help_text=_("Cost centers"),
        related_name="cost_centers_budgets",
        blank=True,
    )
    budget_description = models.ForeignKey(
        BudgetDescription,
        verbose_name=_("Budget description"),
        help_text=_("Budget description"),
        related_name="budget_description_budgets",
        on_delete=models.CASCADE,
    )
    unit_value = models.FloatField(
        _("Unit value"),
        help_text=_("Unit value"),
        default=0,
    )
    quantity = models.PositiveIntegerField(
        _("Quantity"),
        help_text=_("Quantity"),
        default=0,
    )
    initial_value = models.FloatField(
        _("Initial value"),
        help_text=_("Initial value"),
        default=0,
    )
    budget_addition = models.FloatField(
        _("Budget addition"),
        help_text=_("Budget addition"),
        default=0,
    )
    budget_decrease = models.FloatField(
        _("Budget decrease"),
        help_text=_("Budget decrease"),
        default=0,
    )
    budget_decrease_control = models.FloatField(
        _("Budget decrease control"),
        help_text=_("Budget decrease control"),
        default=0,
    )
    released_amount = models.FloatField(
        _("Released amount"),
        help_text=_("Released amount"),
        default=0,
    )
    anulled_amount = models.FloatField(
        _("Anulled amount"),
        help_text=_("Anulled amount"),
        default=0,
    )

    @property
    def current_budget(self) -> float:
        return (self.initial_value) + self.budget_addition - self.budget_decrease

    @property
    def old_budget(self) -> float:
        return self.initial_value - (self.initial_value + self.budget_addition - self.budget_decrease_control)

    @property
    def available_budget(self) -> float:
        budget_provision_budgets = self.budget_provision_budgets.filter(provision_cart__approved=True)
        provosioned_amount = 0
        for budget_provision_budget in budget_provision_budgets:
            provosioned_amount = provosioned_amount + budget_provision_budget.provosioned_amount
        return self.current_budget - provosioned_amount + self.released_amount + self.anulled_amount

    @property
    def available_budget_whit_decrease_control(self) -> float:
        budget_provision_budgets = self.budget_provision_budgets.filter(provision_cart__approved=True)
        provosioned_amount = 0
        for budget_provision_budget in budget_provision_budgets:
            provosioned_amount = provosioned_amount + budget_provision_budget.provosioned_amount
        return (
            self.current_budget
            - provosioned_amount
            - self.budget_decrease_control
            + self.released_amount
            + self.anulled_amount
        )

    @property
    def report_current_budget(self) -> float:
        return (
            self.initial_value
            - self.budget_decrease_control
            + self.budget_addition
            + self.released_amount
            + self.anulled_amount
        )

    @property
    def report_requested_budget(self) -> float:
        budget_provision_budgets = self.budget_provision_budgets.filter(
            provision_cart__approved=True,
            provision_cart__rejected=False,
            provision_cart__annulled=False,
            provision_cart__finished=True,
        )
        total_requested = 0
        for budget_provision_budget in budget_provision_budgets:
            total_requested = total_requested + (
                budget_provision_budget.provosioned_amount - budget_provision_budget.released_amount
            )
        return total_requested

    @property
    def report_available_budget(self) -> float:
        return self.report_current_budget - self.report_requested_budget

    @property
    def report_available_budget_percentage(self) -> float:
        if self.report_current_budget == 0:
            return 0
        else:
            return self.report_available_budget / self.report_current_budget * 100

    @property
    def report_committed_budget(self) -> float:
        budget_provision_budgets = self.budget_provision_budgets.filter(
            provision_cart__approved=True,
            provision_cart__rejected=False,
            provision_cart__annulled=False,
            provision_cart__finished=True,
        )
        carts = []
        total_committed = 0
        for budget_provision_budget in budget_provision_budgets:
            cart = budget_provision_budget.budget_provision_budget
            commitments = cart.provision_cart_commitments.filter(
                finished=True,
            )
            # for commitment in commitments:
            #     total_committed = total_committed + commitment.amount
        return total_committed

    class Meta:
        """Meta definition for Budget."""

        verbose_name = _("Budget")
        verbose_name_plural = _("Budgets")

    def __str__(self):
        """Unicode representation of Budget."""
        return f"{self.project} ({self.budget_description})"

    @property
    def project_name(self):
        return self.project.name

    @property
    def get_budget_description(self):
        return self.budget_description

    def save(self, *args, **kwargs):
        self.initial_value = float(self.unit_value) * float(self.quantity)
        super().save(*args, **kwargs)


class BudgetDecreaseTransaction(BaseModel):
    """Model definition for Budet Transaction."""

    budget = models.ForeignKey(
        Budget,
        verbose_name=_("Budget"),
        help_text=_("Budget"),
        related_name="budget_transactions",
        on_delete=models.DO_NOTHING,
    )
    old_amount = models.FloatField(
        _("Old amount"),
        help_text=_("Old amount"),
        default=0,
    )
    requiered_amount = models.FloatField(
        _("Requiered amount"),
        help_text=_("Requiered amount"),
        default=0,
    )
    new_amount = models.FloatField(
        _("New amount"),
        help_text=_("New amount"),
        default=0,
    )
    project = models.ForeignKey(
        Project,
        verbose_name=_("Project"),
        help_text=_("Project"),
        related_name="project_transactions",
        on_delete=models.DO_NOTHING,
    )
    provision_cart = models.ForeignKey(
        "budget.ProvisionCart",
        verbose_name=_("Provision cart"),
        help_text=_("Provision cart"),
        related_name="provision_cart_transactions",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    class Meta:
        """Meta definition for Budet Transaction."""

        verbose_name = _("Budget Decrease Transaction")
        verbose_name_plural = _("Budget Decrease Transactions")

    def __str__(self):
        """Unicode representation of Budet Decrease Transaction."""
        return f"{self.budget} ({self.project})"


class BudgetRedistributionTransaction(BaseModel):
    """Model definition for Budget Redistribution Transaction."""

    budget = models.ForeignKey(
        Budget,
        verbose_name=_("Budget"),
        help_text=_("Budget"),
        related_name="+",
        on_delete=models.DO_NOTHING,
    )
    original_amount = models.FloatField(
        _("Original amount"),
        help_text=_("Original amount"),
        default=0,
    )
    redistributed_amount = models.FloatField(
        _("Redistributed amount"),
        help_text=_("Redistributed amount"),
        default=0,
    )
    new_amount = models.FloatField(
        _("New amount"),
        help_text=_("New amount"),
        default=0,
    )
    redistribution_item = models.ForeignKey(
        "budget.BudgetRedistributionItem",
        verbose_name=_("Redistribution item"),
        help_text=_("Redistribution item"),
        related_name="redistribution_item_budget_redistribution_transactions",
        on_delete=models.DO_NOTHING,
    )

    class Meta:
        """Meta definition for Budget Redistribution Transaction."""

        verbose_name = _("Budget Redistribution Transaction")
        verbose_name_plural = _("Budget Redistribution Transactions")

    def __str__(self):
        """Unicode representation of Budget Redistribution Transaction."""
        return str(self.id)


# ------------
class BudgetAddtionTransaction(BaseModel):
    """Model definition for Budget Addition Transaction."""

    budget = models.ForeignKey(
        Budget,
        verbose_name=_("Budget"),
        help_text=_("Budget"),
        related_name="+",
        on_delete=models.DO_NOTHING,
    )
    original_amount = models.FloatField(
        _("Original amount"),
        help_text=_("Original amount"),
        default=0,
    )
    added_amount = models.FloatField(
        _("Added amount"),
        help_text=_("Added amount"),
        default=0,
    )
    new_amount = models.FloatField(
        _("New amount"),
        help_text=_("New amount"),
        default=0,
    )
    addition_item = models.ForeignKey(
        "budget.BudgetAdditionItem",
        verbose_name=_("addition item"),
        help_text=_("addition item"),
        related_name="addition_item_budget_addition_transactions",
        on_delete=models.DO_NOTHING,
    )

    class Meta:
        """Meta definition for Budget Addition Transaction."""

        verbose_name = _("Budget Addition Transaction")
        verbose_name_plural = _("Budget Addition Transactions")

    def __str__(self):
        """Unicode representation of Budget Addition Transaction."""
        return str(self.id)


# ------------


class BudgetCap(BaseModel):
    """Model definition for Budget Cap."""

    business_unit = models.ForeignKey(
        BusinessUnit,
        verbose_name=_("Business unit"),
        help_text=_("Business unit"),
        related_name="business_unit_budget_caps",
        on_delete=models.CASCADE,
    )
    cap = models.FloatField(
        _("Cap"),
        help_text=_("Cap"),
        default=0,
    )
    description = models.TextField(
        _("Description"),
        help_text=_("Description"),
    )

    class Meta:
        """Meta definition for Budget Cap."""

        verbose_name = _("Budget Cap")
        verbose_name_plural = _("Budget Caps")

    def __str__(self):
        """Unicode representation of Budget Cap."""
        return self.description
