from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from sicop.budget.models import Budget, BudgetDescription
from sicop.cost_center.models import CostCenter
from sicop.project.models import Project


class BudgetListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    """View for Budget list."""

    model = Budget
    template_name = "sicop/frontend/budget/budget/list.html"
    context_object_name = "budgets"
    permission_required = "budget.view_budget"


class BudgetDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    """View for Budget detail."""

    model = Budget
    template_name = "sicop/frontend/budget/budget/detail.html"
    context_object_name = "budget"
    permission_required = "budget.view_budget"


class BudgetCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    """View for Budget create."""

    model = Budget
    template_name = "sicop/frontend/budget/budget/create.html"
    context_object_name = "budget"
    fields = [
        "project",
        "cost_center",
        "budget_description",
        "unit_value",
        "quantity",
    ]
    permission_required = "budget.add_budget"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["projects"] = Project.objects.all()
        context["cost_centers"] = CostCenter.objects.all()
        context["budget_descriptions"] = BudgetDescription.objects.all()
        return context

    def get_success_url(self) -> str:
        """Return success url."""
        return reverse_lazy("budget_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """Save form."""
        messages.success(self.request, _("Budget created successfully."))
        return super().form_valid(form)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        request.POST._mutable = True
        current_budget = request.POST["unit_value"].replace(",", ".")
        request.POST["unit_value"] = float(current_budget)
        return super().post(request, *args, **kwargs)


class BudgetUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Budget
    template_name = "sicop/frontend/budget/budget/update.html"
    context_object_name = "budget"
    fields = ["project", "cost_center", "budget_description", "unit_value", "quantity", "status"]

    permission_required = "budget.change_budget"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["projects"] = Project.objects.all()
        context["cost_centers"] = CostCenter.objects.all()
        context["budget_descriptions"] = BudgetDescription.objects.all()
        return context

    def get_success_url(self) -> str:
        """Return success url."""
        return reverse_lazy("budget_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """Save form."""
        messages.success(self.request, _("Budget updated successfully."))
        return super().form_valid(form)

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        messages.error(self.request, _("Budget not updated"))
        return super().form_invalid(form)

    def post(self, request: HttpRequest, *args: str, **kwargs) -> HttpResponse:
        request.POST._mutable = True
        if request.POST.get("status") == "True":
            request.POST["status"] = True
        else:
            request.POST["status"] = False
        current_budget = request.POST["unit_value"].replace(",", ".")
        request.POST["unit_value"] = float(current_budget)
        return super().post(request, *args, **kwargs)
