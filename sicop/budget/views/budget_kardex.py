from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.list import ListView

from sicop.budget.models import BudgetDecreaseTransaction


class BudgetDecreaseTransactionListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    """View for BudgetDecreaseTransaction list."""

    model = BudgetDecreaseTransaction
    template_name = "sicop/frontend/budget/kardex/list.html"
    context_object_name = "budget_decrease_transactions"
    permission_required = "budget.view_budget"