from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import TemplateView

from sicop.budget.models import Budget
from sicop.budget.models.provision import ProvisionCart, ProvisionCartBudget
from sicop.project.models import Project


class UpdateProjectInCart(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        try:
            cart_id = kwargs["cart_id"]
            project_id = kwargs["project_id"]
            budget = ProvisionCart.objects.get(id=cart_id)
            project = Project.objects.get(id=project_id)
            budget.project = project
            budget.total_required_amount = project.budget
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


class UpdateTotalsInCart(LoginRequiredMixin, TemplateView):
    template_name = "sicop/frontend/budget/processes/provision/create.html"

    def post(self, request, *args, **kwargs):
        try:
            cart_id = kwargs["cart_id"]
            total_required_amount = request.POST["total_required_amount"]
            total_provisioned_amount = request.POST["total_provisioned_amount"]
            total_missing_amount = request.POST["total_missing_amount"]
            cart = ProvisionCart.objects.get(id=cart_id)
            cart.total_required_amount = total_required_amount
            cart.total_provisioned_amount = total_provisioned_amount
            cart.total_missing_amount = total_missing_amount
            cart.save()

            return JsonResponse(
                {
                    "cart_id": cart_id,
                    "result": "ok",
                }
            )
        except Exception as e:
            print(f"An error: ===============> {str(e)}")
            return JsonResponse(
                {
                    "cart_id": cart_id,
                    "result": f"error: {str(e)}",
                }
            )


class AddItemToProvisionInCart(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        try:
            cart_id = kwargs["cart_id"]
            budget_id = kwargs["budget_id"]
            cart = ProvisionCart.objects.get(id=cart_id)
            budget = Budget.objects.get(id=budget_id)
            provision_cart_budget = ProvisionCartBudget.objects.create(
                provision_cart=cart,
                budget=budget,
            )

            return JsonResponse(
                {
                    "cart_id": cart_id,
                    "budget_id": budget_id,
                    "provision_cart_budget_id": provision_cart_budget.id,
                    "result": "ok",
                }
            )
        except Exception as e:
            print(e)
            return JsonResponse(
                {
                    "cart_id": cart_id,
                    "budget_id": budget_id,
                    "result": f"error: {str(e)}",
                }
            )


class RemoveItemToProvisionInCart(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        try:
            cart_id = kwargs["cart_id"]
            budget_id = kwargs["budget_id"]
            cart = ProvisionCart.objects.get(id=cart_id)
            budget = Budget.objects.get(id=budget_id)
            provision_cart_budget = ProvisionCartBudget.objects.filter(
                provision_cart=cart,
                budget=budget,
            ).delete()

            return JsonResponse(
                {
                    "cart_id": cart_id,
                    "budget_id": budget_id,
                    "provision_cart_budget_id": provision_cart_budget.id,
                    "result": "ok",
                }
            )
        except Exception as e:
            print(e)
            return JsonResponse(
                {
                    "cart_id": cart_id,
                    "budget_id": budget_id,
                    "result": f"error: {str(e)}",
                }
            )


class EditItemProvisionAmountInCart(LoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        try:
            cart_id = kwargs["cart_id"]
            budget_id = request.POST.get("budget_id")
            provision_amount = request.POST.get("provision_amount")
            available_budget = request.POST.get("available_budget")
            cart = ProvisionCart.objects.get(id=cart_id)
            budget = Budget.objects.get(id=budget_id)
            provision_cart_budget = ProvisionCartBudget.objects.filter(
                provision_cart=cart,
                budget=budget,
            ).first()
            provision_cart_budget.provosioned_amount = provision_amount
            provision_cart_budget.available_budget = available_budget
            provision_cart_budget.save()

            return JsonResponse(
                {
                    "cart_id": cart_id,
                    "budget_id": budget_id,
                    "provision_cart_budget_id": provision_cart_budget.id,
                    "result": "ok",
                }
            )
        except Exception as e:
            print(e)
            return JsonResponse(
                {
                    "cart_id": cart_id,
                    "budget_id": budget_id,
                    "result": f"error on amount change: {str(e)}",
                }
            )


class GetCostCentersByProject(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        try:
            project_id = kwargs["pk"]
            project = Project.objects.get(id=project_id)
            budgets = Budget.objects.filter(project=project)
            cost_centers_list = []
            cost_centers_ids = []
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
            return JsonResponse(
                {
                    "project_id": project_id,
                    "cost_centers": cost_centers_list,
                }
            )
        except Exception as e:
            return JsonResponse(
                {
                    "project_id": project_id,
                    "result": f"error: {str(e)}",
                }
            )
