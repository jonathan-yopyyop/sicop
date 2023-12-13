from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from sicop.area.models import AreaMember
from sicop.budget.models import BudetTransaction, Budget
from sicop.budget.models.provision import ProvisionCart, ProvisionCartBudget
from sicop.project.models import Project


class BudgetProvisionList(LoginRequiredMixin, ListView):
    template_name = "sicop/frontend/budget/processes/provision/list.html"
    model = ProvisionCart
    context_object_name = "provision_carts"

    def get_queryset(self):
        return ProvisionCart.objects.filter()
        # user = self.request.user
        # return ProvisionCart.objects.filter(user=user, status=True)


class BudgetProvisionDetail(LoginRequiredMixin, DetailView):
    model = ProvisionCart
    template_name = "sicop/frontend/budget/processes/provision/detail.html"
    context_object_name = "provision_cart"


class BudgetProvisionCreate(LoginRequiredMixin, TemplateView):
    template_name = "sicop/frontend/budget/processes/provision/create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["projects"] = Project.objects.filter(status=True)
        user = self.request.user
        if ProvisionCart.objects.filter(user=user, status=True).exists():
            provision_cart = ProvisionCart.objects.get(user=user, status=True)
        else:
            provision_cart = ProvisionCart.objects.create(user=user)
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
        context["provision_cart"] = provision_cart
        context["cost_centers"] = cost_centers_list
        return context

    def post(self, request, *args, **kwargs):
        try:
            cart_id = request.POST.get("cart_id")
            cart = ProvisionCart.objects.get(id=cart_id)
            project = cart.project
            provision_cart_budgets = ProvisionCartBudget.objects.filter(provision_cart=cart)
            for provision_cart_budget in provision_cart_budgets:
                budget = provision_cart_budget.budget
                old_value = budget.current_budget
                new_value = old_value - provision_cart_budget.provosioned_amount
                provosioned_amount = provision_cart_budget.provosioned_amount
                budget.budget_decrease = budget.budget_decrease + provosioned_amount
                budget.save()
                BudetTransaction.objects.create(
                    budget=budget,
                    old_amount=old_value,
                    new_amount=new_value,
                    project=project,
                )
            cart.finished = True
            cart.status = False
            cart.save()

            messages.success(request, _("Budget provision created successfully."))
            return HttpResponseRedirect(
                reverse(
                    "budget_provision_detail",
                    kwargs={"pk": cart_id},
                )
            )
        except Exception as e:
            print(e)
            return JsonResponse(
                {
                    "cart": cart_id,
                    "result": f"error: {str(e)}",
                }
            )


class UpdateProjectInCart(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        try:
            cart_id = kwargs["cart_id"]
            project_id = kwargs["project_id"]
            budget = ProvisionCart.objects.get(id=cart_id)
            project = Project.objects.get(id=project_id)
            budget.project = project
            budget.save()

            return JsonResponse(
                {
                    "cart_id": cart_id,
                    "result": "ok",
                }
            )
        except Exception as e:
            print(e)
            return JsonResponse(
                {
                    "cart_id": cart_id,
                    "result": f"error: {str(e)}",
                }
            )


class ProvisionCertificateView(TemplateView):
    template_name = "sicop/frontend/budget/processes/provision/provision_certificate.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get("pk")
        cart = ProvisionCart.objects.get(id=pk)
        user = cart.user
        area_member = AreaMember.objects.get(user=user)
        area_rol = area_member.role
        context["provision_cart"] = cart
        context["area_rol"] = area_rol
        return context


class GetBudgetIncart(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        try:
            cart_id = kwargs["cart_id"]
            budget_id = kwargs["budget_id"]
            cart = ProvisionCart.objects.get(id=cart_id)
            budget = Budget.objects.get(id=budget_id)
            provision_cart_budget = ProvisionCartBudget.objects.filter(
                provision_cart_id=cart.id,
                budget_id=budget_id,
            ).first()
            return JsonResponse(
                {
                    "cart_id": cart_id,
                    "budget_id": budget_id,
                    "budget_item": str(budget),
                    "provision_cart_budget_id": provision_cart_budget.id,
                    "provosioned_amount": provision_cart_budget.provosioned_amount,
                    "available_budget": provision_cart_budget.available_budget,
                    "current_budget": budget.current_budget,
                    "result": "ok",
                }
            )
        except Exception as e:
            print(e)
            return JsonResponse(
                {
                    "cart_id": cart_id,
                    "result": f"error: {str(e)}",
                }
            )
