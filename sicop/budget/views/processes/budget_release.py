from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from sicop.area.models import AreaMember
from sicop.budget.models import (
    Budget,
    Commitment,
    CommitmentContract,
    CommitmentNotRelated,
    CommitmentOrphanRealeaseItems,
    CommitmentOrphanRelease,
    CommitmentPO,
    CommitmentRelease,
)
from sicop.budget.models.commitment import get_commitment_types
from sicop.certificate.models import Certificate
from sicop.contract.models import Contract
from sicop.purchase_order.models import PurchaseOrder


class BudgetReleaseSearch(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = "budget.view_commitment"
    template_name = "sicop/frontend/budget/processes/commitment/release/search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["commitment_types"] = get_commitment_types()
        return context


class BudgetRelease(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = "budget.view_commitment"
    template_name = "sicop/frontend/budget/processes/commitment/release/create.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get("pk")
        commitment = Commitment.objects.get(pk=pk)
        provision_cart = commitment.provision_cart
        user = self.request.user
        if CommitmentOrphanRelease.objects.filter(commitment=commitment, user=user, processed=False).count() > 0:
            commitment_orphan_release = CommitmentOrphanRelease.objects.filter(
                commitment=commitment,
                user=user,
            ).last()
        else:
            commitment_orphan_release = CommitmentOrphanRelease.objects.create(
                commitment=commitment,
                user=user,
            )
            provision_cart = commitment.provision_cart
            budgets = provision_cart.provision_cart_provision_budgets.all()
            for budget in budgets:
                CommitmentOrphanRealeaseItems.objects.create(
                    commitment_release=commitment_orphan_release,
                    budget=budget.budget,
                    budget_amount=budget.budget.available_budget,
                    total_to_release=0,
                )

        commitment_orphan_release_items = CommitmentOrphanRealeaseItems.objects.filter(
            commitment_release=commitment_orphan_release,
        )
        context["commitment_orphan_release"] = commitment_orphan_release
        context["commitment_orphan_release_items"] = commitment_orphan_release_items
        context["commitment_types"] = get_commitment_types()
        context["commitment"] = commitment
        context["commitment_contract"] = CommitmentContract.objects.filter(
            commitment=commitment,
        ).last()
        context["commitment_po"] = CommitmentPO.objects.filter(
            commitment=commitment,
        ).last()
        context["commitment_not_related"] = CommitmentNotRelated.objects.filter(
            commitment=commitment,
        ).last()
        context["commitment_release"] = CommitmentRelease.objects.filter(
            commitment=commitment,
        ).last()
        return context

    def post(self, request, *args, **kwargs):
        commitment_orphan_release_object_id = request.POST.get("commitment_orphan_release_object_id")
        commitment_orphan_release = CommitmentOrphanRelease.objects.get(pk=commitment_orphan_release_object_id)
        commitment_orphan_release.processed = True
        commitment_orphan_release.status = False
        commitment_orphan_release.save()
        commitment_orphan_release_items = CommitmentOrphanRealeaseItems.objects.filter(
            commitment_release=commitment_orphan_release,
        )
        commitment = commitment_orphan_release.commitment
        total_to_release = 0
        for item in commitment_orphan_release_items:
            total_to_release = total_to_release + item.total_to_release
            budget: Budget = item.budget
            budget.released_amount = budget.released_amount + item.total_to_release
            budget.save()
        for item in commitment_orphan_release_items:
            budget: Budget = item.budget
            item.new_db_budget_amount = budget.available_budget
            item.save()
        commitment_orphan_release_items = CommitmentOrphanRealeaseItems.objects.filter(
            commitment_release=commitment_orphan_release,
        )
        commitment.total_released = total_to_release
        commitment.save()
        return HttpResponseRedirect(
            reverse(
                "commitment_release_certificate",
                kwargs={"pk": commitment_orphan_release.id},
            )
        )


class BudgerReleaseSearchByCommitment(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = "budget.view_commitment"
    template_name = "sicop/frontend/budget/processes/commitment/release/search_by_commitment.html"

    def post(self, request, *args, **kwargs):
        try:
            pk = request.POST.get("commitment_id")
            commitment = Commitment.objects.get(pk=pk)
            return HttpResponseRedirect(
                reverse(
                    "commitment_release",
                    kwargs={"pk": commitment.id},
                )
            )
        except Exception as e:
            print(e)
            error = _(f"Error on search, the commitment with id {pk} does not exist.")
            messages.warning(request, error)
            return HttpResponseRedirect(reverse("commitment_release_search"))


class BudgerReleaseSearchByContract(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = "budget.view_commitment"
    template_name = "sicop/frontend/budget/processes/commitment/release/search_by_commitment.html"

    def post(self, request, *args, **kwargs):
        try:
            pk = request.POST.get("contract")
            contract = Contract.objects.get(IdContrato=pk)
            commitment_contract = CommitmentContract.objects.filter(
                contract=contract,
            ).last()
            commitment = commitment_contract.commitment
            return HttpResponseRedirect(
                reverse(
                    "commitment_release",
                    kwargs={"pk": commitment.id},
                )
            )
        except Exception as e:
            print(e)
            error = _(f"Error on search, the contract with id {pk} does not exist.")
            messages.warning(request, error)
            return HttpResponseRedirect(reverse("commitment_release_search"))


class BudgerReleaseSearchByPO(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = "budget.view_commitment"
    template_name = "sicop/frontend/budget/processes/commitment/release/search_by_commitment.html"

    def post(self, request, *args, **kwargs):
        try:
            pk = request.POST.get("po")
            po = PurchaseOrder.objects.get(Numero=pk)
            commitment_po = CommitmentPO.objects.filter(
                po=po,
            ).last()
            commitment = commitment_po.commitment
            return HttpResponseRedirect(
                reverse(
                    "commitment_release",
                    kwargs={"pk": commitment.id},
                )
            )
        except Exception as e:
            print(e)
            error = _(f"Error on search, the PO with id {pk} does not exist.")
            messages.warning(request, error)
            return HttpResponseRedirect(reverse("commitment_release_search"))


class BudgerReleaseSearchByLegalization(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = "budget.view_commitment"
    template_name = "sicop/frontend/budget/processes/commitment/release/search_by_commitment.html"

    def post(self, request, *args, **kwargs):
        try:
            pk = request.POST.get("legalization")
            commitment_legalization = CommitmentNotRelated.objects.filter(
                type="LG",
                key=pk,
            ).last()
            commitment = commitment_legalization.commitment
            return HttpResponseRedirect(
                reverse(
                    "commitment_release",
                    kwargs={"pk": commitment.id},
                )
            )
        except Exception as e:
            print(e)
            error = _(f"Error on search, the legalization with id {pk} does not exist.")
            messages.warning(request, error)
            return HttpResponseRedirect(reverse("commitment_release_search"))


class BudgerReleaseSearchByConsumption(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = "budget.view_commitment"
    template_name = "sicop/frontend/budget/processes/commitment/release/search_by_commitment.html"

    def post(self, request, *args, **kwargs):
        try:
            pk = request.POST.get("consumption")
            commitment_consumption = CommitmentNotRelated.objects.filter(
                type="CO",
                key=pk,
            ).last()
            commitment = commitment_consumption.commitment
            return HttpResponseRedirect(
                reverse(
                    "commitment_release",
                    kwargs={"pk": commitment.id},
                )
            )
        except Exception as e:
            print(e)
            error = _(f"Error on search, the consumption with id {pk} does not exist.")
            messages.warning(request, error)
            return HttpResponseRedirect(reverse("commitment_release_search"))


class CommitmentReleaseCertificateView(LoginRequiredMixin, TemplateView):
    template_name = "sicop/frontend/budget/processes/commitment/release/commitment_release_certificate.html"
    permission_required = "budget.add_commitment"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get("pk")
        commitment_orphan_release = CommitmentOrphanRelease.objects.get(id=pk)
        commitment_orphan_release_items = CommitmentOrphanRealeaseItems.objects.filter(
            commitment_release=commitment_orphan_release,
        )
        commitment = commitment_orphan_release.commitment
        user = commitment_orphan_release.user
        if AreaMember.objects.filter(user=user).exists():
            area_member = AreaMember.objects.filter(user=user).last()
            area_rol = area_member.role
        else:
            area_member = None
            area_rol = None
        context["commitment"] = commitment
        context["area_rol"] = area_rol
        context["area_member"] = area_member
        context["certificate_version"] = Certificate.objects.filter(slug="commitment_release").first()
        context["commitment_orphan_release"] = commitment_orphan_release
        context["commitment_orphan_release_items"] = commitment_orphan_release_items

        commitment_contract = CommitmentContract.objects.filter(
            commitment=commitment,
        ).last()
        commitment_po = CommitmentPO.objects.filter(
            commitment=commitment,
        ).last()
        commitment_not_related = CommitmentNotRelated.objects.filter(
            commitment=commitment,
        ).last()
        if commitment_contract is not None:
            key = commitment_contract.contract.IdContrato
        elif commitment_po is not None:
            key = commitment_po.po.Numero
        elif commitment_not_related is not None:
            key = commitment_not_related.key

        context["key"] = key

        return context


class CommitmentReleaseListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    template_name = "sicop/frontend/budget/processes/commitment/release/list.html"
    model = CommitmentOrphanRelease
    context_object_name = "commitment_releases"
    permission_required = "budget.view_commitment"
