from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from sicop.budget.models import Budget
from sicop.budget.models.provision import (
    ProvisionCart,
    ProvisionCartBudget,
    ProvisionCartBudgetHistory,
    ProvisionCartHistory,
)
from sicop.project.models import Project


class ProvisionCartAdditionListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    template_name = "sicop/frontend/budget/processes/provision/addition/list.html"
    model = ProvisionCartHistory
    context_object_name = "provision_carts"
    permission_required = "budget.view_provisioncart"

    def get_queryset(self):
        return ProvisionCartHistory.objects.filter()


class ProvisionCartSearchView(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = "sicop/frontend/budget/processes/provision/addition/search.html"
    permission_required = "budget.view_provisioncart"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        cap_id = request.POST.get("cap_id")
        if ProvisionCart.objects.filter(id=cap_id).count() > 0:
            provision_cart = ProvisionCart.objects.get(id=cap_id)
            if ProvisionCartHistory.objects.filter(provision_cart=provision_cart, finished=False).count() > 0:
                provision_cart_history = ProvisionCartHistory.objects.filter(provision_cart=provision_cart).last()
            else:
                provision_cart_history = ProvisionCartHistory.objects.create(
                    provision_cart=provision_cart,
                    user=request.user,
                    total_required_amount=provision_cart.total_required_amount,
                    total_provisioned_amount=provision_cart.total_provisioned_amount,
                    total_missing_amount=provision_cart.total_missing_amount,
                    finished=False,
                    approved=False,
                )
                provision_cart_budgets = ProvisionCartBudget.objects.filter(provision_cart=provision_cart)
                for provision_cart_budget in provision_cart_budgets:
                    print(f"provision_cart_budget: {provision_cart_budget.id}")
                    print(f"provision_cart_budget.budget: {provision_cart_budget.budget.id}")
                    print(
                        f"provision_cart_budget.budget.current_budget: {provision_cart_budget.budget.current_budget}"
                    )
                    print(f"provision_cart_budget.provosioned_amount: {provision_cart_budget.provosioned_amount}")
                    ProvisionCartBudgetHistory.objects.create(
                        provision_cart_history=provision_cart_history,
                        budget=provision_cart_budget.budget,
                        already_taked_amount=provision_cart_budget.provosioned_amount,
                        available_budget=provision_cart_budget.available_budget,
                    )
            return HttpResponseRedirect(
                reverse(
                    "budget_arrange_update",
                    kwargs={"pk": provision_cart_history.id},
                )
            )
        else:
            error = _(f"Error on search, the CAP with id {cap_id} does not exist.")
            messages.warning(request, error)
            return HttpResponseRedirect(reverse("budget_arrange_addition_search"))


class ProvisionCartUpdateView(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = "sicop/frontend/budget/processes/provision/addition/update.html"
    permission_required = "budget.view_provisioncart"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get("pk")
        provision_cart_history = ProvisionCartHistory.objects.get(id=id)
        provision_cart = provision_cart_history.provision_cart
        context["provision_cart"] = provision_cart
        context["projects"] = Project.objects.filter(status=True)
        context["provision_cart_history"] = provision_cart_history
        cost_centers_list = []
        cost_centers_ids = []
        if provision_cart.project is not None:
            budgets = Budget.objects.filter(project=provision_cart.project)

            for budget in budgets:
                cost_centers = budget.cost_centers.all()
                for cost_center in cost_centers:
                    if cost_center.id not in cost_centers_ids:
                        cost_centers_list.append(
                            {
                                "id": cost_center.id,
                                "name": cost_center.name,
                            }
                        )
                    cost_centers_ids.append(cost_center.id)
        context["cost_centers"] = cost_centers_list
        return context

    def post(self, request, *args, **kwargs):
        provision_cart_history_id = request.POST.get("cart_id")
        provision_cart_history = ProvisionCartHistory.objects.get(id=provision_cart_history_id)
        provision_cart_history_budgets = ProvisionCartBudgetHistory.objects.filter(
            provision_cart_history=provision_cart_history
        ).all()
        provision_cart = ProvisionCart.objects.get(id=provision_cart_history.provision_cart.id)
        # provision_cart_budgets = ProvisionCartBudget.objects.filter(provision_cart=provision_cart)

        # Require approval
        project = provision_cart.project
        project_type = project.project_type
        if provision_cart.total_provisioned_amount >= project_type.cap:
            provision_cart.requires_approval = True
            provision_cart.approved = False
        else:
            provision_cart.requires_approval = False
            provision_cart.approved = True
        provision_cart.save()
        # provision_certificate
        return HttpResponseRedirect(
            reverse(
                "provision_certificate",
                kwargs={"pk": provision_cart.id},
            )
        )
        # return JsonResponse(
        #     {
        #         "status": "success",
        #         "post": request.POST,
        #         "provision_cart": provision_cart.id,
        #         "provision_cart_history_budgets": list(provision_cart_history_budgets.values()),
        #     }
        # )
