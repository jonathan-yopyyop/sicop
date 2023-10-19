from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse
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
    permission_required = "expense_type.view_expensetype"


class ExpenseTypeCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    """View for Expense Type create."""

    model = ExpenseType
    template_name = "sicop/frontend/expense/type/create.html"
    fields = [
        "name",
        "expense_concepts",
    ]
    permission_required = "expense_type.add_expensetype"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        expense_types = ExpenseType.objects.all()
        expense_concepts = []
        for expense_type in expense_types:
            types = expense_type.expense_concepts.all()
            for type_C in types:
                expense_concepts.append(type_C.id)

        context["expense_concepts_all"] = ExpenseConcept.objects.all().exclude(id__in=expense_concepts)
        return context

    def post(self, request, *args, **kwargs):
        try:
            name = request.POST["name"]
            expense_concepts = request.POST.getlist("expense_concepts[]")
            expense_type = ExpenseType.objects.create(name=name)
            expense_type.expense_concepts.set(expense_concepts)
            expense_type.save()
            messages.success(request, _("Expense type created successfully"))

        except Exception as e:
            print(e)
            messages.success(request, _("Expense type not created"))

        return HttpResponseRedirect(
            reverse(
                "expense_type_detail",
                kwargs={"pk": expense_type.id},
            )
        )


class ExpenseTypeDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    """View for Expense Type detail."""

    model = ExpenseType
    template_name = "sicop/frontend/expense/type/detail.html"
    context_object_name = "expense_type"
    permission_required = "expense_type.view_expensetype"

    def get_context_data(self, **kwargs):
        """Insert the single object into the context dict."""
        context = super().get_context_data(**kwargs)
        context["expense_concepts"] = self.object.expense_concepts.all()
        return context


class ExpenseTypeUpdatingView(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = "sicop/frontend/expense/type/update.html"
    permission_required = "expense_type.change_expensetype"

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
