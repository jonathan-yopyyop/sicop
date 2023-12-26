from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse  # , reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

# from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from sicop.area.models import AreaMember
from sicop.budget.models import Budget, BudgetDecreaseTransaction
from sicop.budget.models.provision import ProvisionCart, ProvisionCartApproval, ProvisionCartBudget
from sicop.certificate.models import Certificate
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
            observation = request.POST.get("observation")
            cart = ProvisionCart.objects.get(id=cart_id)
            cart.observation = observation
            project = cart.project
            provision_cart_budgets = ProvisionCartBudget.objects.filter(provision_cart=cart)
            project_type = project.project_type
            if cart.total_provisioned_amount >= project_type.cap:
                cart.requires_approval = True
                cart.approved = False
            else:
                cart.requires_approval = False
                cart.approved = True
            cart.save()
            for provision_cart_budget in provision_cart_budgets:
                if not cart.requires_approval:
                    budget = provision_cart_budget.budget
                    old_value = budget.current_budget
                    new_value = old_value - provision_cart_budget.provosioned_amount
                    provosioned_amount = provision_cart_budget.provosioned_amount
                    budget.budget_decrease_control = budget.budget_decrease_control + provosioned_amount
                    budget.save()
                    BudgetDecreaseTransaction.objects.create(
                        budget=budget,
                        old_amount=old_value,
                        requiered_amount=old_value - new_value,
                        new_amount=new_value,
                        project=project,
                        provision_cart=cart,
                    )
                    cart.approved = True
                    cart.save()
                else:
                    ProvisionCartApproval.objects.create(
                        provision_cart=cart,
                        must_be_approved_by=cart.user,
                    )
            cart.finished = True
            cart.status = False
            cart.save()

            messages.success(request, _("Budget provision created successfully."))
            return HttpResponseRedirect(
                reverse(
                    "provision_certificate",
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
        if ProvisionCartApproval.objects.filter(provision_cart=cart).exists():
            provision_cart_approval = ProvisionCartApproval.objects.filter(provision_cart=cart).last()
        else:
            provision_cart_approval = None
        context["provision_cart_approval"] = provision_cart_approval
        context["provision_cart"] = cart
        context["area_rol"] = area_rol
        context["project"] = cart.project
        context["area_member"] = area_member
        context["certificate_version"] = Certificate.objects.filter(slug="cap").first()
        return context


class GetBudgetIncart(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        try:
            cart_id = kwargs["cart_id"]
            budget_id = kwargs["budget_id"]
            cart = ProvisionCart.objects.get(id=cart_id)
            budget = Budget.objects.get(id=budget_id)
            current_budget = budget.current_budget - budget.budget_decrease_control
            if current_budget < 0:
                current_budget = 0
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
                    "provosioned_amount": budget.available_budget,
                    "available_budget": budget.available_budget,
                    "current_budget": budget.available_budget,
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


class ProvisionCartApprovalList(LoginRequiredMixin, ListView):
    template_name = "sicop/frontend/budget/processes/provision/approval/list.html"
    model = ProvisionCartApproval
    context_object_name = "provision_carts"

    def get_queryset(self):
        user = self.request.user
        queryset = ProvisionCartApproval.objects.filter(
            must_be_approved_by=user,
            provision_cart__approved=False,
            rejected=False,
        )
        return queryset


class ProvisionCartApprovalUpdateView(LoginRequiredMixin, TemplateView):
    """View for Area update."""

    template_name = "sicop/frontend/budget/processes/provision/approval/update.html"

    def post(self, request, *args: str, **kwargs):
        try:
            request.POST._mutable = True
            provision_cart_approval: ProvisionCartApproval = ProvisionCartApproval.objects.get(id=kwargs["pk"])
            if request.POST.get("approved") == "True":
                request.POST["approved"] = True
                # Go to approve

                provision_cart = provision_cart_approval.provision_cart
                provision_cart_budgets = ProvisionCartBudget.objects.filter(provision_cart=provision_cart)
                cart = provision_cart_approval.provision_cart
                project = cart.project
                cart.approved = True
                cart.save()
                provision_cart_approval.rejected = False
                provision_cart_approval.approved = True
                provision_cart_approval.save()
                for provision_cart_budget in provision_cart_budgets:
                    budget = provision_cart_budget.budget
                    old_value = budget.current_budget
                    new_value = old_value - provision_cart_budget.provosioned_amount
                    provosioned_amount = provision_cart_budget.provosioned_amount
                    budget.budget_decrease_control = budget.budget_decrease_control + provosioned_amount
                    budget.save()
                    BudgetDecreaseTransaction.objects.create(
                        budget=budget,
                        old_amount=old_value,
                        requiered_amount=old_value - new_value,
                        new_amount=new_value,
                        project=project,
                        provision_cart=cart,
                    )
            else:
                cart = provision_cart_approval.provision_cart
                request.POST["approved"] = False
                provision_cart_approval.rejected = True
                provision_cart_approval.approved = False
                provision_cart_approval.save()
            url = reverse(
                "provision_certificate",
                kwargs={"pk": cart.id},
            )
            # return JsonResponse(
            #     {
            #         "cart.id": cart.id,
            #         "url": url,
            #     }
            # )
            return HttpResponseRedirect(url)
        except Exception as e:
            print(e)
            return JsonResponse(
                {
                    "result": f"error: {str(e)}",
                }
            )
