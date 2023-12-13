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

    @property
    def current_budget(self) -> float:
        return self.initial_value + self.budget_addition - self.budget_decrease

    @property
    def old_budget(self) -> float:
        return self.initial_value - (self.initial_value + self.budget_addition - self.budget_decrease)

    class Meta:
        """Meta definition for Budget."""

        verbose_name = _("Budget")
        verbose_name_plural = _("Budgets")

    def __str__(self):
        """Unicode representation of Budget."""
        return f"{self.project} ({self.budget_description})"

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

    class Meta:
        """Meta definition for Budet Transaction."""

        verbose_name = _("Budget Decrease Transaction")
        verbose_name_plural = _("Budget Decrease Transactions")

    def __str__(self):
        """Unicode representation of Budet Decrease Transaction."""
        return f"{self.budget} ({self.project})"


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

        verbose_name = "Budget Cap"
        verbose_name_plural = "Budget Caps"

    def __str__(self):
        """Unicode representation of Budget Cap."""
        return self.description
