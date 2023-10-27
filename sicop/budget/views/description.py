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

from sicop.budget.models import BudgetDescription
from sicop.expense_concept.models import ExpenseConcept


class BudgetDescriptionListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    """View for Budgetdescription list."""

    model = BudgetDescription
    template_name = "sicop/frontend/budget/description/list.html"
    context_object_name = "budgetdescriptions"
    permission_required = "budget.view_budgetdescription"


class BudgetDescriptionDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    """View for Budgetdescription detail."""

    model = BudgetDescription
    template_name = "sicop/frontend/budget/description/detail.html"
    context_object_name = "budgetdescription"
    permission_required = "budget.view_budgetdescription"


class BudgetDescriptionCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    """View for Budgetdescription create."""

    model = BudgetDescription
    template_name = "sicop/frontend/budget/description/create.html"
    fields = [
        "expense_concept",
        "description",
    ]
    context_object_name = "budgetdescription"
    permission_required = "budget.add_budgetdescription"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        budget_descriptions = BudgetDescription.objects.all()
        current_expense_concepts = []
        for budget_description in budget_descriptions:
            current_expense_concepts.append(budget_description.expense_concept.id)
        context["expense_concepts"] = ExpenseConcept.objects.all().exclude(id__in=current_expense_concepts)
        return context

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        messages.success(self.request, _("Budget description created successfully"))
        return super().form_valid(form)

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        messages.error(self.request, _("Budget description not created"))
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy(
            "budget_description_detail",
            kwargs={
                "pk": self.object.pk,
            },
        )


class BudgetDescriptionUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    """View for Budgetdescription update."""

    model = BudgetDescription
    template_name = "sicop/frontend/budget/description/update.html"
    fields = [
        "expense_concept",
        "description",
        "status",
    ]
    context_object_name = "budgetdescription"
    permission_required = "budget.change_budgetdescription"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        budget_descriptions = BudgetDescription.objects.all()
        current_expense_concepts = []
        for budget_description in budget_descriptions:
            current_expense_concepts.append(budget_description.expense_concept.id)
        context["expense_concepts"] = ExpenseConcept.objects.all().exclude(id__in=current_expense_concepts)
        return context

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        messages.success(self.request, _("Budget description updated successfully"))
        return super().form_valid(form)

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        messages.error(self.request, _("Budget description not updated"))
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy(
            "budget_description_detail",
            kwargs={
                "pk": self.object.pk,
            },
        )

    def post(self, request: HttpRequest, *args: str, **kwargs) -> HttpResponse:
        if request.POST.get("status") == "True":
            request.POST._mutable = True
            request.POST["status"] = True
        else:
            request.POST._mutable = True
            request.POST["status"] = False
        return super().post(request, *args, **kwargs)
