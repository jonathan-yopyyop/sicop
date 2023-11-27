from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from sicop.budget.models.provision import ProvisionCart
from sicop.cost_center.models import CostCenter
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
        context["cost_centers"] = CostCenter.objects.filter(status=True)
        user = self.request.user
        if ProvisionCart.objects.filter(user=user, status=True).exists():
            context["provision_cart"] = ProvisionCart.objects.get(user=user, status=True)
        else:
            provision_cart = ProvisionCart.objects.create(user=user)
            context["provision_cart"] = provision_cart
        return context

    def post(self, request, *args, **kwargs):
        try:
            cart_id = request.POST.get("cart_id")
            cart = ProvisionCart.objects.get(id=cart_id)
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
        context["provision_cart"] = ProvisionCart.objects.get(id=pk)
        return context
