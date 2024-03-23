from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from sicop.area.models import AreaMember, AreaRole
from sicop.budget.models import Budget, BudgetDecreaseTransaction
from sicop.budget.models.provision import (
    ProvisionCart,
    ProvisionCartApproval,
    ProvisionCartBudget,
    ProvisionCartBudgetHistory,
    ProvisionCartHistory,
    ProvisionCartAnullationReason,
    ProvisionCartAnullation,
)
from sicop.certificate.models import Certificate
from sicop.project.models import Project


class BudgetProvisionList(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    template_name = "sicop/frontend/budget/processes/provision/list.html"
    model = ProvisionCart
    context_object_name = "provision_carts"
    permission_required = "budget.view_provisioncart"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        area_member = AreaMember.objects.filter(user=user).first()
        role: AreaRole = area_member.role
        context["area_member"] = area_member
        context["role"] = role
        return context

    def get_queryset(self):
        user = self.request.user
        area_member = AreaMember.objects.filter(user=user).first()
        role: AreaRole = area_member.role
        if role.code == "chief" or role.code == "jefe":
            return ProvisionCart.objects.filter(
                project__area=area_member.area,
            )
        elif role.code == "director":
            return ProvisionCart.objects.filter(
                project__area=area_member.area,
            )
        elif role.code == "director_administrativo" or role.code == "administrator" or role.code == "administrador":
            return ProvisionCart.objects.filter(
                # project__area=area_member.area,
            )
        else:
            return ProvisionCart.objects.filter(
                project__project_manager=self.request.user,
            )


class BudgetProvisionDetail(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    model = ProvisionCart
    template_name = "sicop/frontend/budget/processes/provision/detail.html"
    context_object_name = "provision_cart"
    permission_required = "budget.view_provisioncart"


class BudgetProvisionCreate(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = "sicop/frontend/budget/processes/provision/create.html"
    permission_required = "budget.add_provisioncart"

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
            provistion_cart_history = ProvisionCartHistory.objects.create(
                provision_cart=cart,
                user=request.user,
                total_required_amount=cart.total_required_amount,
                total_provisioned_amount=cart.total_provisioned_amount,
                total_missing_amount=cart.total_missing_amount,
                finished=cart.finished,
                observation=cart.observation,
                requires_approval=cart.requires_approval,
                approved=cart.approved,
                rejected=cart.rejected,
            )
            for provision_cart_budget in provision_cart_budgets:
                ProvisionCartBudgetHistory.objects.create(
                    provision_cart_history=provistion_cart_history,
                    budget=provision_cart_budget.budget,
                    already_taked_amount=provision_cart_budget.provosioned_amount,
                    provosioned_amount=0,
                    available_budget=provision_cart_budget.available_budget,
                )
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


class ProvisionCertificateView(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = "sicop/frontend/budget/processes/provision/provision_certificate.html"
    permission_required = "budget.view_provisioncart"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get("pk")
        cart = ProvisionCart.objects.get(id=pk)
        user = cart.user
        current_user = self.request.user
        if AreaMember.objects.filter(user=user).exists():
            area_member = AreaMember.objects.filter(user=user).last()
            area_rol = area_member.role
        else:
            area_member = None
            area_rol = None
        if AreaMember.objects.filter(user=current_user).exists():
            current_user_area_member = AreaMember.objects.filter(user=current_user).last()
            current_user_area_rol = current_user_area_member.role
        else:
            current_user_area_member = None
            current_user_area_rol = None
        if ProvisionCartApproval.objects.filter(provision_cart=cart).exists():
            provision_cart_approval = ProvisionCartApproval.objects.filter(provision_cart=cart).last()
            provision_cart_approval_url = reverse(
                "provision_cart_approval_update",
                kwargs={"pk": provision_cart_approval.id},
            )
        else:
            provision_cart_approval = None

        provision_cart_anullation_url = reverse(
            "provision_cart_anullation_update",
            kwargs={"pk": provision_cart_approval.id},
        )
        context["provision_cart_approval"] = provision_cart_approval
        context["provision_cart"] = cart
        context["area_rol"] = area_rol
        context["project"] = cart.project
        context["area_member"] = area_member
        context["certificate_version"] = Certificate.objects.filter(slug="cap").first()
        context["current_user_area_rol"] = current_user_area_rol
        context["current_user_area_member"] = current_user_area_member
        context["provision_cart_approval_url"] = provision_cart_approval_url
        context["provision_cart_anullation_url"] = provision_cart_anullation_url
        context["provision_cart_anullation_reasons"] = ProvisionCartAnullationReason.objects.filter(status=True)
        context["provision_cart_anullations"] = ProvisionCartAnullation.objects.filter(provision_cart=cart).last()
        context["current_user"] = current_user
        # ------------------------------------------
        provision_cart = cart
        provision_cart_budgets = ProvisionCartBudget.objects.filter(provision_cart=provision_cart)
        is_viable = True
        test = []
        for provision_cart_budget in provision_cart_budgets:
            current_budget = Budget.objects.get(id=provision_cart_budget.budget.id)
            available_budget = current_budget.available_budget

            if float(available_budget) < float(provision_cart_budget.provosioned_amount):
                is_viable = False
            test.append(
                {
                    "id": provision_cart_budget.budget.id,
                    "available_budget": provision_cart_budget.budget.available_budget,
                    "provosioned_amount": provision_cart_budget.provosioned_amount,
                }
            )
        context["is_viable"] = is_viable
        context["test"] = test
        # ------------------------------------------
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


class GetBudgetIncartHistory(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        try:
            cart_id = kwargs["cart_id"]
            budget_id = kwargs["budget_id"]
            cart = ProvisionCartHistory.objects.get(id=cart_id)
            budget = Budget.objects.get(id=budget_id)
            current_budget = budget.current_budget - budget.budget_decrease_control
            if current_budget < 0:
                current_budget = 0
            provision_cart_budget = ProvisionCartBudgetHistory.objects.filter(
                provision_cart_history=cart,
                budget=budget,
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
                    "cart.id": cart.id,
                    "budget_id": budget_id,
                    "budget.id": budget.id,
                    "provision_cart_budget": str(provision_cart_budget),
                    "result": f"error: {str(e)}",
                }
            )


class ProvisionCartApprovalList(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    template_name = "sicop/frontend/budget/processes/provision/approval/list.html"
    model = ProvisionCartApproval
    context_object_name = "provision_carts"
    permission_required = "budget.view_provisioncartapproval"

    def get_queryset(self):
        user = self.request.user
        area_member = AreaMember.objects.filter(user=user).first()
        role: AreaRole = area_member.role
        queryset = None
        if role.code == "director":
            queryset = ProvisionCartApproval.objects.filter(
                provision_cart__project__area=area_member.area,
                provision_cart__approved=False,
                rejected=False,
            ).distinct("provision_cart__id")
        elif role.code == "director_administrativo":
            queryset = ProvisionCartApproval.objects.filter(
                provision_cart__approved=False,
                rejected=False,
            ).distinct("provision_cart__id")
        elif role.code == "administrator" or role.code == "administrador":
            queryset = ProvisionCartApproval.objects.filter().distinct("provision_cart__id")
        elif role.code == "chief" or role.code == "jefe":
            queryset = ProvisionCartApproval.objects.filter(
                provision_cart__project__area=area_member.area,
            ).distinct("provision_cart__id")

        return queryset


class ProvisionCartApprovalUpdateView(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    """View for Area update."""

    template_name = "sicop/frontend/budget/processes/provision/approval/update.html"
    permission_required = "budget.change_provisioncartapproval"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        provision_cart_approval = ProvisionCartApproval.objects.get(id=self.kwargs["pk"])

        provision_cart = provision_cart_approval.provision_cart
        provision_cart_budgets = ProvisionCartBudget.objects.filter(provision_cart=provision_cart)
        is_viable = True
        test = []
        for provision_cart_budget in provision_cart_budgets:
            current_budget = Budget.objects.get(id=provision_cart_budget.budget.id)
            available_budget = current_budget.available_budget
            if available_budget >= provision_cart_budget.provosioned_amount:
                print("------------------------------------------------------------------")
                print(f"{available_budget} >= {provision_cart_budget.provosioned_amount}")
                print("------------------------------------------------------------------")
                is_viable = False
            test.append(
                {
                    "id": provision_cart_budget.budget.id,
                    "available_budget": available_budget,
                    "provosioned_amount": provision_cart_budget.provosioned_amount,
                }
            )
        context["provision_cart_approval"] = provision_cart_approval
        context["is_viable"] = is_viable
        context["test"] = test
        return context

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
                provision_cart_approval.approved_by = request.user
                provision_cart_approval.save()
                test = []
                is_viable = True
                for provision_cart_budget in provision_cart_budgets:
                    current_budget = Budget.objects.get(id=provision_cart_budget.budget.id)
                    available_budget = current_budget.available_budget
                    if available_budget >= provision_cart_budget.provosioned_amount:
                        is_viable = False
                    test.append(
                        {
                            "id": provision_cart_budget.budget.id,
                            "available_budget": provision_cart_budget.budget.available_budget,
                            "provosioned_amount": provision_cart_budget.provosioned_amount,
                        }
                    )

                for provision_cart_budget in provision_cart_budgets:
                    current_budget = Budget.objects.get(id=provision_cart_budget.budget.id)
                    available_budget = current_budget.available_budget

                    budget = provision_cart_budget.budget
                    old_value = budget.current_budget
                    new_value = old_value - provision_cart_budget.provosioned_amount
                    if available_budget >= provision_cart_budget.provosioned_amount:
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
                request.POST["approved"] = False
                cart = provision_cart_approval.provision_cart
                cart.rejected = True
                cart.approved = False
                cart.save()
                provision_cart_approval.rejected = True
                provision_cart_approval.approved = False
                provision_cart_approval.save()
            url = reverse(
                "provision_certificate",
                kwargs={"pk": cart.id},
            )
            return HttpResponseRedirect(url)
        except Exception as e:
            print(e)
            return JsonResponse(
                {
                    "result": f"error: {str(e)}",
                }
            )


@method_decorator(csrf_exempt, name="dispatch")
class GetProvisionCartsByCriteria(TemplateView):
    def get(self, request, *args, **kwargs):
        query = request.GET.get("q", "")
        results = ProvisionCart.objects.filter(
            id__icontains=query,
        )
        result_list = []
        for result in results:
            result_list.append(
                {
                    "id": result.id,
                    "text": str(result),
                }
            )
        return JsonResponse(
            result_list,
            safe=False,
        )


class ProvisionCartAnullationUpdateView(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    """View for Area update."""

    template_name = "sicop/frontend/budget/processes/provision/anullation/update.html"
    permission_required = "budget.change_provisioncartanullation"

    def post(self, request, *args: str, **kwargs):
        try:
            # get the post values
            request.POST._mutable = True
            provision_cart = ProvisionCart.objects.get(id=kwargs["pk"])
            reason_id = request.POST.get("reason")
            observation = request.POST.get("observation")
            # Create the anullation
            reason = ProvisionCartAnullationReason.objects.get(id=reason_id)
            ProvisionCartAnullation.objects.create(
                provision_cart=provision_cart,
                anulled_by=request.user,
                reason=reason,
                observation=observation,
            )
            # Anull the provision cart
            provision_cart.rejected = True
            provision_cart.approved = False
            provision_cart.annulled = True
            provision_cart.save()
            # return the values
            if provision_cart.approved:
                provision_cart_budgets = ProvisionCartBudget.objects.filter(provision_cart=provision_cart)
                for provision_cart_budget in provision_cart_budgets:
                    budget = provision_cart_budget.budget
                    provosioned_amount = provision_cart_budget.provosioned_amount
                    budget.anulled_amount = budget.anulled_amount + provosioned_amount
                    budget.save()

            url = reverse(
                "provision_certificate",
                kwargs={"pk": provision_cart.id},
            )
            return HttpResponseRedirect(url)
        except Exception as e:
            print(e)
            return JsonResponse(
                {
                    "result": f"error: {str(e)}",
                }
            )
