from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView

from sicop.budget.models import Commitment, CommitmentContract, CommitmentNotRelated, CommitmentPO, CommitmentRelease
from sicop.budget.models.commitment import get_commitment_types
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
