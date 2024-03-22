from typing import Any
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from sicop.area.models import AreaMember
from sicop.budget.models import Budget, BudgetRedistributionTransaction
from sicop.budget.models.redistribution import (
    BudgetRedistribution,
    BudgetRedistributionItem,
    BudgetRedistributionItemApproval,
)
from sicop.certificate.models import Certificate
from sicop.project.models import Project
from sicop.area.models import AreaRole


class BudgetRedistributionListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    """View for BudgetRedistribution list."""

    model = BudgetRedistribution
    template_name = "sicop/frontend/budget/processes/redistribution/list.html"
    context_object_name = "budget_redistributions"
    permission_required = "budget.view_budgetredistribution"

    def get_context_data(self, **kwargs):
        """Add extra context."""
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        user = self.request.user
        user = self.request.user
        area_member = AreaMember.objects.filter(user=user).first()
        role: AreaRole = area_member.role
        if role.code == "chief" or role.code == "jefe":
            return BudgetRedistribution.objects.all()
        elif role.code == "director":
            return BudgetRedistribution.objects.all()
        elif role.code == "administrator" or role.code == "director_administrativo":
            return BudgetRedistribution.objects.all()
        else:
            return None


class BudgetRedistributionCreate(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = "sicop/frontend/budget/processes/redistribution/create.html"
    permission_required = "budget.add_budgetredistribution"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if BudgetRedistribution.objects.filter(user=user, status=True).exists():
            budget_redistribution = BudgetRedistribution.objects.get(user=user, status=True)
        else:
            budget_redistribution = BudgetRedistribution.objects.create(user=user)
        budgets_to_take = None
        if budget_redistribution.budget:
            budgets_to_take = Budget.objects.exclude(id=budget_redistribution.budget.id)
        context["budget_redistribution"] = budget_redistribution
        context["projects"] = Project.objects.all()
        context["budgets"] = Budget.objects.all()
        context["budgets_to_take"] = budgets_to_take
        return context

    def post(self, request, *args, **kwargs):
        try:
            # To process the budget redistribution
            budget_redistribution_id = request.POST["budget_redistribution_id"]
            observation = request.POST["observation"]
            budget_redistribution = BudgetRedistribution.objects.get(
                id=budget_redistribution_id,
            )
            budget_redistribution.observation = observation
            budget_redistribution.save()
            budget_redistribution_items = budget_redistribution.budget_redistribution_budget_redistribution_items.all()
            budget_redistribution_requires_approval = False
            total_redistributed_amount = 0

            budget_for_redistribution = budget_redistribution.budget
            for budget_redistribution_item in budget_redistribution_items:
                item: BudgetRedistributionItem = budget_redistribution_item
                budget: Budget = item.budget
                proyect = budget.project
                proyect_type = proyect.project_type
                redistribution_cap = proyect_type.redistribution_cap

                if item.redistributed_amount > redistribution_cap:
                    budget_redistribution_requires_approval = True
                    item.requires_approval = True
                    # Add an approval request
                    BudgetRedistributionItemApproval.objects.create(
                        budget_redistribution_item=item,
                        approved=False,
                    )
                    # To do or review
                    item.must_be_approved_by = request.user
                    item.save()
                else:
                    # Process the values
                    total_redistributed_amount = total_redistributed_amount + item.redistributed_amount
                    new_budget_budget_decrease = budget.budget_decrease + item.redistributed_amount
                    budget.budget_decrease = new_budget_budget_decrease
                    budget.budget_decrease_control = budget.budget_decrease_control + item.redistributed_amount
                    budget.save()

                    # Update statuses
                    item.approved = True
                    item.requires_approval = False
                    item.must_be_approved_by = None
                    item.processed = True
                    item.save()
                    # Create a budget redistribution transaction
                    BudgetRedistributionTransaction.objects.create(
                        budget=budget,
                        original_amount=budget.available_budget,
                        redistributed_amount=item.redistributed_amount,
                        new_amount=item.new_amount,
                        redistribution_item=item,
                    )
                    # Modify the budget increasing
                    budget.save()
            # Update the budget redistribution
            budget_for_redistribution.budget_addition = (
                budget_for_redistribution.budget_addition + total_redistributed_amount
            )
            budget_for_redistribution.save()
            budget_redistribution.requires_approval = budget_redistribution_requires_approval
            budget_redistribution.status = False
            budget_redistribution.finished = True
            # todo
            user = self.request.user
            budget_redistribution.must_be_approved_by = user
            # todo finished
            budget_redistribution.save()
            messages.success(request, _("Budget redistribution created successfully."))
            return HttpResponseRedirect(
                reverse(
                    "redistribution_certificate",
                    kwargs={"pk": budget_redistribution_id},
                )
            )

        except Exception as e:
            return JsonResponse(
                {
                    "status": "error",
                    "message": str(e),
                }
            )


class BudgetRedistributionDetail(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = "sicop/frontend/budget/processes/redistribution/detail.html"
    permission_required = "budget.view_budgetredistribution"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        budget_redistribution_id = self.kwargs["pk"]
        budget_redistribution = BudgetRedistribution.objects.get(id=budget_redistribution_id)
        budgets_to_take = None
        if budget_redistribution.budget:
            budgets_to_take = Budget.objects.exclude(id=budget_redistribution.budget.id)

        context["budget_redistribution"] = budget_redistribution
        context["budgets"] = Budget.objects.all()
        context["budgets_to_take"] = budgets_to_take
        return context


class UpdateBudgetForRedistribution(LoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        try:
            budget_id = request.POST["budget_id"]
            budget = Budget.objects.get(id=budget_id)
            redistribution_id = request.POST["redistribution_id"]
            BudgetRedistribution.objects.filter(
                id=redistribution_id,
            ).update(
                budget=budget,
                original_amount=budget.available_budget,
                new_amount=budget.available_budget,
            )
            return JsonResponse(
                {
                    "status": "ok",
                    "message": _("Budget updated"),
                }
            )
        except Exception as e:
            return JsonResponse(
                {
                    "status": "error",
                    "message": str(e),
                }
            )


class CreateRedistributionItem(LoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        try:
            budget_id = request.POST["budget_id"]
            budget = Budget.objects.get(id=budget_id)
            redistribution_id = request.POST["redistribution_id"]
            redistribution = BudgetRedistribution.objects.get(id=redistribution_id)
            redistribution_item = BudgetRedistributionItem.objects.create(
                budget_redistribution=redistribution,
                budget=budget,
                original_amount=budget.available_budget,
                redistributed_amount=0,
                new_amount=budget.available_budget,
            )
            return JsonResponse(
                {
                    "status": "ok",
                    "message": _("Item created"),
                    "item": {
                        "budget_id": budget.id,
                        "budget_description": budget.budget_description.description,
                        "redistribution_id": redistribution_item.id,
                        "original_amount": redistribution_item.original_amount,
                        "redistributed_amount": redistribution_item.redistributed_amount,
                        "new_amount": redistribution_item.new_amount,
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


class RemoveRedistributionItem(LoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        try:
            row_id = request.POST["row_id"]
            BudgetRedistributionItem.objects.filter(
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


class UpdateRedistributionItem(LoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        try:
            row_id = request.POST["row_id"]
            taked_amount = request.POST["taked_amount"]
            budget_redistribution_item = BudgetRedistributionItem.objects.filter(
                id=row_id,
            ).first()
            redistributed_amount = float(taked_amount)
            new_amount = budget_redistribution_item.original_amount - redistributed_amount
            if new_amount < 0:
                new_amount = 0
            budget_redistribution_item.new_amount = new_amount
            budget_redistribution_item.redistributed_amount = redistributed_amount
            budget_redistribution_item.save()
            return JsonResponse(
                {
                    "status": "ok",
                    "id": row_id,
                    "message": _("Item updated"),
                    "redistributed_amount": redistributed_amount,
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


class UpdateRedistributionTotals(LoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        try:
            redistribution_id = request.POST["redistribution_id"]
            redistribution = BudgetRedistribution.objects.get(id=redistribution_id)
            redistribution_items = redistribution.budget_redistribution_budget_redistribution_items.all()
            original_amount = redistribution.original_amount
            redistributed_amount = 0

            for redistribution_item in redistribution_items:
                redistributed_amount = redistributed_amount + redistribution_item.redistributed_amount

            new_amount = original_amount + redistributed_amount
            if new_amount < 0:
                new_amount = 0

            redistribution.redistributed_amount = redistributed_amount
            redistribution.new_amount = new_amount
            redistribution.save()
            return JsonResponse(
                {
                    "status": "ok",
                    "message": _("Totals updated"),
                    "original_amount": original_amount,
                    "redistributed_amount": redistributed_amount,
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


class RedistributionBudgetApprovalList(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    """View for RedistributionBudgetApproval list."""

    template_name = "sicop/frontend/budget/processes/redistribution/approval/list.html"
    permission_required = "budget.view_budgetredistribution"

    def get_context_data(self, **kwargs):
        """Add extra context."""
        context = super().get_context_data(**kwargs)
        context["approval_list"] = BudgetRedistribution.objects.filter(
            requires_approval=True,
            approved=False,
            finished=True,
        ).exclude(rejected=True)
        return context


class RedistributionCertificateView(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = "sicop/frontend/budget/processes/redistribution/redistribution_certificate.html"
    permission_required = "budget.view_budgetredistribution"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get("pk")
        budget_redistribution = BudgetRedistribution.objects.get(id=pk)
        user = budget_redistribution.user
        if AreaMember.objects.filter(user=user).exists():
            area_member = AreaMember.objects.filter(user=user).last()
            area_rol = area_member.role
        else:
            area_member = None
            area_rol = None
        for_approval = BudgetRedistributionItemApproval.objects.filter(
            budget_redistribution_item__budget_redistribution=budget_redistribution,
            approved=False,
        )
        context["budget_redistribution"] = budget_redistribution
        context["area_rol"] = area_rol
        context["area_member"] = area_member
        context["certificate_version"] = Certificate.objects.filter(slug="redistribution").first()
        context["for_approval"] = for_approval
        return context


class RedistributionBudgetApprovalUpdate(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    """View for RedistributionBudgetApproval update."""

    template_name = "sicop/frontend/budget/processes/redistribution/redistribution_certificate.html"
    permission_required = "budget.view_budgetredistributionitemapproval"

    def post(self, request, *args, **kwargs):
        try:
            observation = request.POST["observation"]
            items = request.POST.getlist("items[]")
            budget_redistribution = None
            for item_id in items:
                item: BudgetRedistributionItem = BudgetRedistributionItem.objects.get(id=item_id)
                if budget_redistribution is None:
                    budget_redistribution = item.budget_redistribution
                    break
            budget_redistribution.approval_observation = observation
            budget_redistribution.save()

            if request.POST.get("approved") == "True":
                total_approved = 0
                budget_redistribution.approval_observation = observation
                budget_redistribution.approved = True
                budget_redistribution.save()
                for item_id in items:
                    item: BudgetRedistributionItem = BudgetRedistributionItem.objects.get(id=item_id)
                    total_approved = total_approved + item.redistributed_amount
                    BudgetRedistributionItemApproval.objects.filter(
                        budget_redistribution_item=item,
                    ).update(
                        approved=True,
                    )
                    if not item.processed:
                        budget = item.budget
                        # Process the values
                        new_budget_budget_decrease = budget.budget_decrease + item.redistributed_amount
                        budget.budget_decrease = new_budget_budget_decrease
                        budget.budget_decrease_control = budget.budget_decrease_control + item.redistributed_amount
                        budget.save()
                        # Update statuses
                        item.approved = True
                        item.processed = True
                        item.save()
                        # Create a budget redistribution transaction
                        BudgetRedistributionTransaction.objects.create(
                            budget=budget,
                            original_amount=budget.available_budget,
                            redistributed_amount=item.redistributed_amount,
                            new_amount=item.new_amount,
                            redistribution_item=item,
                        )
                        # Modify the budget increasing
                        budget.save()

                for_approval = BudgetRedistributionItemApproval.objects.filter(
                    budget_redistribution_item__budget_redistribution=budget_redistribution,
                )
                approved = True
                items_list = []
                for item in for_approval:
                    items_list.append([item.id, item.approved])
                    if not item.approved:
                        approved = False

                if approved:
                    budget_redistribution.approved = True
                    budget_redistribution.save()
                # Update the budget redistribution
                budget_for_redistribution = budget_redistribution.budget
                budget_for_redistribution.budget_addition = budget_for_redistribution.budget_addition + total_approved
                budget_for_redistribution.save()
                messages.success(request, _("Budget redistribution approved successfully."))
            else:
                messages.success(request, _("Budget redistribution rejected."))
                budget_redistribution.approved = False
                budget_redistribution.approval_observation = observation
                budget_redistribution.rejected = True
                budget_redistribution.save()

            return HttpResponseRedirect(
                reverse(
                    "redistribution_budget_approval_list",
                )
            )
        except Exception as e:
            messages.warning(request, _("Budget redistribution error" + str(e)))
            return HttpResponseRedirect(
                reverse(
                    "redistribution_budget_approval_list",
                )
            )
