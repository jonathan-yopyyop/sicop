from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from sicop.expense_type.models import ExpenseConcept, ExpenseType


class ExpenseTypeListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    """View for Expense Type list."""

    model = ExpenseType
    template_name = "sicop/frontend/expense/type/list.html"
    context_object_name = "expense_types"
    permission_required = "expense_type.view_expense_type"


class ExpenseTypeCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    """View for Expense Type create."""

    model = ExpenseType
    template_name = "sicop/frontend/expense/type/form.html"
    fields = [
        "name",
        "expense_concepts",
    ]
    success_url = reverse_lazy("expense_type_list")
    permission_required = "expense_type.add_expense_type"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        messages.success(self.request, _("Expense Type created successfully."))
        return super().form_valid(form)

    def form_invalid(self, form):
        """If the form is invalid, show the associated model."""
        messages.error(self.request, _("Expense Type has not been created."))
        return super().form_invalid(form)


class ExpenseTypeDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    """View for Expense Type detail."""

    model = ExpenseType
    template_name = "sicop/frontend/expense/type/detail.html"
    context_object_name = "expense_type"
    permission_required = "expense_type.view_expense_type"

    def get_context_data(self, **kwargs):
        """Insert the single object into the context dict."""
        context = super().get_context_data(**kwargs)
        context["expense_concepts"] = self.object.expense_concepts.all()
        return context


class ExpenseTypeUpdatingView(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = "sicop/frontend/expense/type/update.html"
    permission_required = "expense_type.change_expense_type"

    def get_context_data(self, **kwargs):
        """Insert the single object into the context dict."""
        context = super().get_context_data(**kwargs)
        expense_type = ExpenseType.objects.get(pk=self.kwargs["pk"])
        expense_concepts = list(expense_type.expense_concepts.all().values_list("id", flat=True))
        context["expense_type"] = expense_type
        context["expense_concepts"] = expense_concepts
        context["expense_concepts_all"] = ExpenseConcept.objects.all()
        return context

    def post(self, request: HttpRequest, *args: str, **kwargs):
        try:
            name = request.POST["name"]
            expense_type_status = request.POST["status"]
            status = False
            if expense_type_status == "True":
                status = True
            expense_concepts = request.POST.getlist("expense_concepts[]")
            expense_type = ExpenseType.objects.get(pk=self.kwargs["pk"])
            expense_type.name = name
            expense_type.status = status
            expense_type.expense_concepts.clear()
            expense_type.expense_concepts.set(expense_concepts)
            expense_type.save()
            messages.success(request, _("Expense Type updated successfully."))
            return HttpResponseRedirect(
                reverse(
                    "expense_type_detail",
                    kwargs={"pk": self.kwargs["pk"]},
                )
            )
        except Exception as e:
            print(e)
            messages.error(request, _("Expense Type not updated."))
            return HttpResponseRedirect(
                reverse(
                    "expense_type_detail",
                    kwargs={"pk": self.kwargs["pk"]},
                )
            )
