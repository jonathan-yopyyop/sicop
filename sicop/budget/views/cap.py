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

from sicop.budget.models import BudgetCap
from sicop.business_unit.models import BusinessUnit


class BudgetCapListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    """BudgetCapListView."""

    model = BudgetCap
    template_name = "sicop/frontend/budget/cap/list.html"
    context_object_name = "budget_caps"
    permission_required = "budget.view_budgetcap"


class BudgetCapDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    """BudgetCapDetailView."""

    model = BudgetCap
    template_name = "sicop/frontend/budget/cap/detail.html"
    context_object_name = "budget_cap"
    permission_required = "budget.view_budgetcap"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["business_units"] = BusinessUnit.objects.filter(status=True)
        return context


class BudgetCapCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    """BudgetCapCreateView."""

    model = BudgetCap
    template_name = "sicop/frontend/budget/cap/create.html"
    fields = [
        "business_unit",
        "cap",
        "description",
    ]
    context_object_name = "budget_cap"
    permission_required = "budget.add_budgetcap"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["business_units"] = BusinessUnit.objects.filter(status=True)
        return context

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        messages.success(self.request, _("Budget cap created successfully"))
        return super().form_valid(form)

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        messages.warning(self.request, _("Budget cap not created"))
        return super().form_invalid(form)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "budget_cap_detail",
            kwargs={
                "pk": self.object.pk,
            },
        )

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        request.POST._mutable = True
        cap = request.POST.get("cap")
        # convert cap string to float
        cap = cap.replace(",", "")
        cap = cap.replace(".", "")
        cap = cap.replace(" ", "")
        cap = float(cap)
        request.POST["cap"] = cap

        print(request.POST)

        return super().post(request, *args, **kwargs)


class BudgetCapUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    """BudgetCapUpdateView."""

    model = BudgetCap
    template_name = "sicop/frontend/budget/cap/update.html"
    fields = [
        "business_unit",
        "cap",
        "description",
        "status",
    ]
    context_object_name = "budget_cap"
    permission_required = "budget.change_budgetcap"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["business_units"] = BusinessUnit.objects.filter(status=True)
        return context

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        messages.success(self.request, _("Budget cap updated successfully"))
        return super().form_valid(form)

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        messages.warning(self.request, _("Budget cap not updated"))
        return super().form_invalid(form)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "budget_cap_detail",
            kwargs={
                "pk": self.object.pk,
            },
        )

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        request.POST._mutable = True
        if request.POST.get("status") == "True":
            request.POST["status"] = True
        else:
            request.POST["status"] = False
        cap = request.POST.get("cap")
        # convert cap string to float
        cap = cap.replace(",", "")
        cap = cap.replace(".", "")
        cap = cap.replace(" ", "")
        cap = float(cap)
        request.POST["cap"] = cap
        return super().post(request, *args, **kwargs)
