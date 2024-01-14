from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from sicop.expense_concept.models import ExpenseConcept


class ExpenseConceptListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    """View for Expense Concept list."""

    model = ExpenseConcept
    template_name = "sicop/frontend/expense/concept/list.html"
    context_object_name = "expense_concepts"
    permission_required = "expense_concept.view_expenseconcept"


class ExpenseConceptDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    """View for Expense Concept detail."""

    model = ExpenseConcept
    template_name = "sicop/frontend/expense/concept/detail.html"
    context_object_name = "expense_concept"
    permission_required = "expense_concept.view_expenseconcept"


class ExpenseConceptUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    """View for Expense Concept update."""

    model = ExpenseConcept
    template_name = "sicop/frontend/expense/concept/update.html"
    fields = [
        "name",
        "status",
    ]
    context_object_name = "expense_concept"
    permission_required = "expense_concept.change_expenseconcept"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        messages.success(self.request, _("Expense Concept updated successfully"))
        return super().form_valid(form)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        messages.warning(self.request, _("Expense Concept not updated, please review the data"))
        return super().form_invalid(form)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "expense_concept_detail",
            kwargs={"pk": self.object.id},
        )

    def post(self, request: HttpRequest, *args: str, **kwargs) -> HttpResponse:
        if request.POST.get("status") == "True":
            request.POST._mutable = True
            request.POST["status"] = True
        else:
            request.POST._mutable = True
            request.POST["status"] = False
        print(request.POST)
        return super().post(request, *args, **kwargs)


class ExpenseConceptCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    """View for Expense Concept create."""

    model = ExpenseConcept
    template_name = "sicop/frontend/expense/concept/create.html"
    fields = [
        "name",
    ]
    context_object_name = "expense_concept"
    permission_required = "expense_concept.add_expenseconcept"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        messages.success(self.request, _("Expense Concept created successfully"))
        return super().form_valid(form)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        messages.warning(self.request, _("Expense Concept not created, please review the data"))
        return super().form_invalid(form)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "expense_concept_detail",
            kwargs={"pk": self.object.id},
        )

    def post(self, request: HttpRequest, *args: str, **kwargs) -> HttpResponse:
        return super().post(request, *args, **kwargs)
