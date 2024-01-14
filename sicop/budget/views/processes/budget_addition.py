from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from sicop.area.models import AreaMember
from sicop.budget.models import Budget, BudgetAddtionTransaction
from sicop.budget.models.addition import BudgetAddition, BudgetAdditionApproval, BudgetAdditionItem
from sicop.certificate.models import Certificate
from sicop.project.models import Project


class BudgetAdditionListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    """View for Budget addition list."""

    model = BudgetAddition
    template_name = "sicop/frontend/budget/processes/addition/list.html"
    context_object_name = "budget_additions"
    permission_required = "budget.view_budgetaddition"

    def get_context_data(self, **kwargs):
        """Add extra context."""
        context = super().get_context_data(**kwargs)
        return context


class BudgetAdditionCreateView(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = "sicop/frontend/budget/processes/addition/create.html"
    permission_required = "budget.add_budgetaddition"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["projects"] = Project.objects.filter(status=True)
        user = self.request.user
        if BudgetAddition.objects.filter(
            user=user,
            finished=False,
        ).exists():
            budget_addition = BudgetAddition.objects.get(
                user=user,
                status=True,
                finished=False,
            )
        else:
            budget_addition = BudgetAddition.objects.create(
                user=user,
                status=True,
                finished=False,
            )

        context["budget_addition"] = budget_addition
        return context

    def post(self, request, *args, **kwargs):
        try:
            # todo
            user_for_approval = request.user
            # end todo

            # To create the budget redistribution
            addition_id = request.POST["addition_id"]
            observation = request.POST["observation"]
            budget_addition = BudgetAddition.objects.get(
                id=addition_id,
            )
            budget_addition.observation = observation
            budget_addition.finished = True
            budget_addition.must_be_approved_by = user_for_approval
            budget_addition.save()
            # create a new budget addition approval
            BudgetAdditionApproval.objects.create(
                budget_addition=budget_addition,
                must_be_approved_by=user_for_approval,
            )
            messages.success(request, _("Budget redistribution created successfully."))
            return HttpResponseRedirect(
                reverse(
                    "addition_certificate",
                    kwargs={"pk": addition_id},
                )
            )
        except Exception as e:
            return JsonResponse(
                {
                    "status": "error",
                    "message": str(e),
                }
            )


class CreateAdditionItem(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
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


class RemoveAdditionItem(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
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


class UpdateAdditionItem(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
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


class AdditionCertificateView(LoginRequiredMixin, TemplateView):
    template_name = "sicop/frontend/budget/processes/addition/addition_certificate.html"
    permission_required = "budget.view_budgetaddition"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get("pk")
        budget_addition = BudgetAddition.objects.get(id=pk)
        user = budget_addition.user
        if AreaMember.objects.filter(user=user).exists():
            area_member = AreaMember.objects.filter(user=user).last()
            area_rol = area_member.role
        else:
            area_member = None
            area_rol = None
        context["budget_addition"] = budget_addition
        context["area_rol"] = area_rol
        context["area_member"] = area_member
        context["certificate_version"] = Certificate.objects.filter(slug="addition").first()

        return context


class AdditionApprovalUpdateView(LoginRequiredMixin, TemplateView):
    permission_required = "budget.change_budgetaddition"

    def post(self, request, *args, **kwargs):
        try:
            addition_id = kwargs["pk"]
            addition = BudgetAddition.objects.get(id=addition_id)
            addition_approval = BudgetAdditionApproval.objects.filter(
                budget_addition=addition,
            ).first()
            approved = request.POST["approved"]
            observation = request.POST["observation"]
            addition.approval_observation = observation
            if approved == "True":
                approved = True
                rejected = False
                # To update the budget items
                budget_addition_items = addition.budgetadditionitem_set.all()
                for item in budget_addition_items:
                    budget: Budget = item.budget
                    added_amount = item.added_amount
                    budget.budget_addition = budget.budget_addition + added_amount
                    budget.save()
                    # update the status
                    item.approved = True
                    item.rejected = False
                    item.processed = True
                    item.save()
                    # create budget addtion transaction
                    BudgetAddtionTransaction.objects.create(
                        budget=budget,
                        original_amount=budget.available_budget,
                        added_amount=added_amount,
                        new_amount=budget.available_budget + added_amount,
                        addition_item=item,
                    )

                messages.success(request, _("Budget addition approved successfully."))
            else:
                approved = False
                rejected = True
                budget_addition_items = addition.budgetadditionitem_set.all()
                for item in budget_addition_items:
                    # update the status
                    item.approved = False
                    item.rejected = True
                    item.processed = True
                    item.save()
                messages.success(request, _("Budget addition rejected."))

            addition.approved = approved
            addition.rejected = rejected
            addition.save()
            addition_approval.approved = approved
            addition_approval.rejected = rejected
            addition_approval.save()
            return HttpResponseRedirect(
                reverse(
                    "budget_addition_list",
                )
            )
        except Exception as e:
            return JsonResponse(
                {
                    "status": "error",
                    "message": str(e),
                }
            )


class AdditionBudgetApprovalList(LoginRequiredMixin, TemplateView):
    """View for AdditiontionBudgetApproval list."""

    template_name = "sicop/frontend/budget/processes/addition/approval/list.html"
    permission_required = "budget.view_budgetadditionapproval"

    def get_context_data(self, **kwargs):
        """Add extra context."""
        context = super().get_context_data(**kwargs)
        context["approval_list"] = BudgetAddition.objects.filter(
            requires_approval=True,
            approved=False,
            finished=True,
        ).exclude(rejected=True)
        return context
