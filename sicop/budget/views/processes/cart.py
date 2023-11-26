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
            cart = ProvisionCart.objects.get(id=cart_id)
            budget = Budget.objects.get(id=budget_id)
            provision_cart_budget = ProvisionCartBudget.objects.filter(
                provision_cart=cart,
                budget=budget,
            ).first()
            provision_cart_budget.provosioned_amount = provision_amount
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
