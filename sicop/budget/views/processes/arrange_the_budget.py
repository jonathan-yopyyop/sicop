from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import TemplateView

from sicop.budget.models.provision import ProvisionCart
from sicop.cost_center.models import CostCenter
from sicop.project.models import Project


class BudgetProvisionCreate(LoginRequiredMixin, TemplateView):
    template_name = "sicop/frontend/budget/processes/provision/create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["projects"] = Project.objects.filter(status=True)
        context["cost_centers"] = CostCenter.objects.filter(status=True)
        user = self.request.user
        if ProvisionCart.objects.filter(user=user, status=True).exists():
            context["provision_cart"] = ProvisionCart.objects.get(user=user, status=True)
        else:
            provision_cart = ProvisionCart.objects.create(user=user)
            context["provision_cart"] = provision_cart
        return context


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
