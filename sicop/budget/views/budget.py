from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from sicop.budget.models import Budget, BudgetDescription
from sicop.cost_center.models import CostCenter
from sicop.project.models import Project
from sicop.area.models import Area, AreaMember, AreaRole


class BudgetListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    """View for Budget list."""

    model = Budget
    template_name = "sicop/frontend/budget/budget/list.html"
    context_object_name = "budgets"
    permission_required = "budget.view_budget"

    def get_queryset(self):
        user = self.request.user
        area_member = AreaMember.objects.filter(user=user).first()
        role: AreaRole = area_member.role
        if role.code == "chief" or role.code == "jefe":
            return Budget.objects.filter(
                project__area=area_member.area,
            )
        elif role.code == "director":
            return Budget.objects.filter(
                project__area=area_member.area,
            )
        elif role.code == "administrator" or role.code == "administrador" or role.code == "director_administrativo":
            return Budget.objects.all()
        else:
            return Budget.objects.filter(
                project__project_manager=user,
            )


class BudgetDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    """View for Budget detail."""

    model = Budget
    template_name = "sicop/frontend/budget/budget/detail.html"
    context_object_name = "budget"
    permission_required = "budget.view_budget"


class BudgetCreateView(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    """View for Budget create."""

    template_name = "sicop/frontend/budget/budget/create.html"
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

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        project = request.POST["project"]
        budget_description = request.POST["budget_description"]
        unit_value = float(request.POST["unit_value"].replace(",", "."))
        quantity = request.POST["quantity"]
        cost_centers = request.POST.getlist("cost_centers")
        budget = Budget.objects.create(
            project=Project.objects.get(id=project),
            budget_description=BudgetDescription.objects.get(id=budget_description),
            unit_value=unit_value,
            quantity=quantity,
        )
        budget.cost_centers.set(cost_centers)
        budget.save()
        messages.success(request, _("Budget created successfully."))
        print(request.POST)
        return HttpResponseRedirect(
            reverse(
                "budget_detail",
                kwargs={"pk": budget.id},
            )
        )


class BudgetUpdateView(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = "sicop/frontend/budget/budget/update.html"
    permission_required = "budget.change_budget"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        budget = Budget.objects.get(pk=self.kwargs["pk"])
        cost_centers_in_budget = budget.cost_centers.all()
        selected_cost_centers = []
        for cost_center in cost_centers_in_budget:
            selected_cost_centers.append(cost_center.id)
        context["budget"] = budget
        context["projects"] = Project.objects.filter(status=True)
        context["cost_centers"] = CostCenter.objects.filter(status=True)
        context["budget_descriptions"] = BudgetDescription.objects.filter(status=True)
        context["selected_cost_centers"] = selected_cost_centers
        return context

    def post(self, request: HttpRequest, *args: str, **kwargs) -> HttpResponse:
        budget = Budget.objects.get(pk=self.kwargs["pk"])
        request.POST._mutable = True
        if request.POST.get("status") == "True":
            status = True
        else:
            status = False
        current_budget = request.POST["unit_value"].replace(",", ".")
        unit_value = float(current_budget)
        budget.project = Project.objects.get(id=request.POST["project"])
        budget.budget_description = BudgetDescription.objects.get(id=request.POST["budget_description"])
        budget.unit_value = unit_value
        budget.quantity = request.POST["quantity"]
        budget.status = status
        budget.cost_centers.clear()
        budget.cost_centers.set(request.POST.getlist("cost_centers"))
        budget.save()
        messages.success(request, _("Budget updated successfully."))
        return HttpResponseRedirect(
            reverse(
                "budget_detail",
                kwargs={"pk": budget.id},
            )
        )


class GetBudgetsByCostCenterAndProject(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        cost_center_id = kwargs["pk"]
        project_id = kwargs["project_id"]
        cost_center = CostCenter.objects.get(id=cost_center_id)
        project = Project.objects.get(id=project_id)
        budgets = Budget.objects.filter(
            project=project,
            cost_centers__in=[cost_center],
            status=True,
        )
        items = []

        for budget in budgets:
            budget_ready = budget.available_budget
            if budget_ready < 0:
                budget_ready = 0
            amount = f"{float(budget_ready):0,.2f}"
            items.append(
                [
                    budget.id,
                    f"{budget.budget_description} (${amount})",
                    budget.available_budget,
                ]
            )
        return JsonResponse(
            {
                "cost_center_id": cost_center_id,
                "items": items,
            }
        )


class GetBudgetDetailById(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        budget_id = kwargs["pk"]
        budget = Budget.objects.get(id=budget_id)
        amount = budget.available_budget
        cost_centers = budget.cost_centers.all()
        cost_center_list = []
        for cost_center in cost_centers:
            cost_center_list.append(cost_center.name)
        return JsonResponse(
            {
                "budget_id": budget_id,
                "amount": amount,
                "budget_description": budget.budget_description.description,
                "unit_value": budget.unit_value,
                "quantity": budget.quantity,
                "initial_value": budget.initial_value,
                "budget_addition": budget.budget_addition,
                "budget_decrease": budget.budget_decrease,
                "cost_centers": cost_center_list,
            }
        )


class GetBudgetDetailExceptId(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        budget_id = kwargs["pk"]
        budget = Budget.objects.get(id=budget_id)
        budgets_to_take = Budget.objects.exclude(id=budget.id)
        items = []
        for budget in budgets_to_take:
            items.append(
                [
                    budget.id,
                    f"{budget.budget_description.description} (${budget.available_budget})",
                ]
            )
        return JsonResponse(
            {
                "budget_id": budget_id,
                "items": items,
            }
        )


class GetBudgetsByProject(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        project_id = kwargs["project_id"]
        project = Project.objects.get(id=project_id)
        budgets = Budget.objects.filter(
            project=project,
            status=True,
        )
        items = []

        for budget in budgets:
            budget_ready = budget.available_budget
            if budget_ready < 0:
                budget_ready = 0
            items.append(
                [
                    budget.id,
                    f"{budget.budget_description}",
                    budget.available_budget,
                ]
            )
        return JsonResponse(
            {
                "project_id": project_id,
                "items": items,
            }
        )


class GetBudgetsByProjectExcludingBudget(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        project_id = kwargs["project_id"]
        project = Project.objects.get(id=project_id)
        budgets = Budget.objects.filter(
            project=project,
            status=True,
        )
        items = []
        for budget in budgets:
            budget_ready = budget.available_budget
            if budget_ready < 0:
                budget_ready = 0
            items.append(
                [
                    budget.id,
                    f"{budget.budget_description}",
                    budget.available_budget,
                ]
            )
        return JsonResponse(
            {
                "project_id": project_id,
                "items": items,
            }
        )
