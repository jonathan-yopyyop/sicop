from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from sicop.budget.models import Budget
from sicop.budget.models.addition import BudgetAddition, BudgetAdditionItem
from sicop.project.models import Project


class BudgetAdditionListView(LoginRequiredMixin, ListView):
    """View for Budget addition list."""

    model = BudgetAddition
    template_name = "sicop/frontend/budget/processes/addition/list.html"
    context_object_name = "budget_additions"

    def get_context_data(self, **kwargs):
        """Add extra context."""
        context = super().get_context_data(**kwargs)
        return context


class BudgetAdditionCreateView(LoginRequiredMixin, TemplateView):
    template_name = "sicop/frontend/budget/processes/addition/create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["projects"] = Project.objects.filter(status=True)
        user = self.request.user
        if BudgetAddition.objects.filter(
            user=user,
            status=True,
        ).exists():
            budget_addition = BudgetAddition.objects.get(
                user=user,
                status=True,
            )
        else:
            budget_addition = BudgetAddition.objects.create(
                user=user,
            )

        context["budget_addition"] = budget_addition
        return context


class CreateAdditionItem(LoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        try:
            budget_id = request.POST["budget_id"]
            budget = Budget.objects.get(id=budget_id)
            addition_id = request.POST["addition_id"]
            budget_addition = BudgetAddition.objects.get(id=addition_id)
            addition_item = BudgetAdditionItem.objects.create(
                budget_addition=budget_addition,
                budget=budget,
                original_amount=budget.available_budget,
                added_amount=0,
                new_amount=budget.available_budget,
            )
            return JsonResponse(
                {
                    "status": "ok",
                    "message": _("Item created"),
                    "item": {
                        "budget_id": budget.id,
                        "budget_description": budget.budget_description.description,
                        "addition_id": addition_item.id,
                        "original_amount": addition_item.original_amount,
                        "added_amount": addition_item.added_amount,
                        "new_amount": addition_item.new_amount,
                    },
                }
            )
        except Exception as e:
            return JsonResponse(
                {
                    "status": "error",
                    "message": str(e),
                }
            )


class RemoveAdditionItem(LoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        try:
            row_id = request.POST["row_id"]
            BudgetAdditionItem.objects.filter(
                id=row_id,
            ).delete()
            return JsonResponse(
                {
                    "status": "ok",
                    "id": row_id,
                    "message": _("Item deleted"),
                }
            )
        except Exception as e:
            return JsonResponse(
                {
                    "status": "error",
                    "message": str(e),
                }
            )


class UpdateAdditionItem(LoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        try:
            row_id = request.POST["row_id"]
            added_amount = request.POST["added_amount"]
            budget_redistribution_item = BudgetAdditionItem.objects.filter(
                id=row_id,
            ).first()
            added_amount = float(added_amount)
            new_amount = budget_redistribution_item.original_amount + added_amount
            if new_amount < 0:
                new_amount = 0
            budget_redistribution_item.new_amount = new_amount
            budget_redistribution_item.added_amount = added_amount
            budget_redistribution_item.save()
            return JsonResponse(
                {
                    "status": "ok",
                    "id": row_id,
                    "message": _("Item updated"),
                    "added_amount": added_amount,
                    "new_amount": new_amount,
                }
            )
        except Exception as e:
            return JsonResponse(
                {
                    "status": "error",
                    "message": str(e),
                }
            )
