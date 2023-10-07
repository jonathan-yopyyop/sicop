from django.db import models
from django.utils.translation import gettext_lazy as _

from config.models import BaseModel
from sicop.cost_center.models import CostCenter
from sicop.expense_type.models import ExpenseType
from sicop.project.models import Project


class BudgetDescription(BaseModel):
    """Model definition for Budget Description."""

    expense_type = models.ForeignKey(
        ExpenseType,
        verbose_name=_("Expense type"),
        help_text=_("Expense type"),
        related_name="expense_type_budgets",
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
    cost_center = models.ForeignKey(
        CostCenter,
        verbose_name=_("Cost center"),
        help_text=_("Cost center"),
        related_name="cost_center_budgets",
        on_delete=models.CASCADE,
    )
    budget_description = models.ForeignKey(
        BudgetDescription,
        verbose_name=_("Budget description"),
        help_text=_("Budget description"),
        related_name="budget_description_budgets",
        on_delete=models.CASCADE,
    )
    unit_value = models.DecimalField(
        _("Unit value"),
        help_text=_("Unit value"),
        max_digits=10,
        decimal_places=2,
        default=0,
    )
    quantity = models.PositiveIntegerField(
        _("Quantity"),
        help_text=_("Quantity"),
        default=0,
    )
    initial_value = models.DecimalField(
        _("Initial value"),
        help_text=_("Initial value"),
        max_digits=10,
        decimal_places=2,
        default=0,
    )
    budget_addition = models.DecimalField(
        _("Budget addition"),
        help_text=_("Budget addition"),
        max_digits=10,
        decimal_places=2,
        default=0,
    )
    budget_decrease = models.DecimalField(
        _("Budget decrease"),
        help_text=_("Budget decrease"),
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    @property
    def current_budget(self) -> float:
        return self.initial_value + self.budget_addition - self.budget_decrease

    class Meta:
        """Meta definition for Budget."""

        verbose_name = _("Budget")
        verbose_name_plural = _("Budgets")

    def __str__(self):
        """Unicode representation of Budget."""
        return f"{self.project} - {self.cost_center} - {self.expense_type} - {self.budget_description}"

    def save(self, *args, **kwargs):
        self.initial_value = self.unit_value * self.quantity
        super().save(*args, **kwargs)
