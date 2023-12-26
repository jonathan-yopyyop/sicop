from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.list import ListView

from sicop.budget.models import BudgetDecreaseTransaction, BudgetRedistributionTransaction


class BudgetDecreaseTransactionListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    """View for BudgetDecreaseTransaction list."""

    model = BudgetDecreaseTransaction
    template_name = "sicop/frontend/budget/kardex/decrease/list.html"
    context_object_name = "budget_decrease_control_transactions"
    permission_required = "budget.view_budget"


class BudgetRedistributionTransactionListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    """View for BudgetRedistributionTransaction list."""

    model = BudgetRedistributionTransaction
    template_name = "sicop/frontend/budget/kardex/redistribution/list.html"
    context_object_name = "budget_redistribution_transactions"
    permission_required = "budget.view_budget"
