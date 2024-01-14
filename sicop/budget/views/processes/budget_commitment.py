from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from sicop.budget.models import (
    Commitment,
    CommitmentContract,
    CommitmentPO,
    CommitmentRealeaseItems,
    CommitmentRelease,
    ProvisionCart,
)
from sicop.budget.models.commitment import get_commitment_types
from sicop.contract.models import Contract
from sicop.integration.models import Third
from sicop.purchase_order.models import PurchaseOrder


class CommitmentListView(LoginRequiredMixin, ListView):
    template_name = "sicop/frontend/budget/processes/commitment/list.html"
    model = Commitment
    context_object_name = "commitments"


class CommitmentCreateView(LoginRequiredMixin, TemplateView):
    template_name = "sicop/frontend/budget/processes/commitment/create.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if Commitment.objects.filter(
            user=user,
            finished=False,
        ).exists():
            commitment = Commitment.objects.get(
                user=user,
                status=True,
                finished=False,
            )
        else:
            commitment = Commitment.objects.create(
                user=user,
                status=True,
                finished=False,
            )
        context["commitment_types"] = get_commitment_types()
        context["commitment"] = commitment
        context["commitment_contract"] = CommitmentContract.objects.filter(
            commitment=commitment,
        ).last()
        context["commitment_po"] = CommitmentPO.objects.filter(
            commitment=commitment,
        ).last()
        context["commitment_release"] = CommitmentRelease.objects.filter(
            commitment=commitment,
        ).last()
        return context

    def post(self, request, *args, **kwargs):
        pass
        # import ipdb; ipdb.set_trace()
        # print(request.POST)
        # print(request.POST.get("contract_or_po"))
        # print(request.POST.get("third"))
        # print(request.POST.get("has_tax"))
        # print(request.POST.get("provision_budget_amount"))
        # print(request.POST.get("provision_cart"))
        # print(request.POST.get("user"))
        # print(requ)


class UpdateCommitmentCap(LoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        try:
            commitment_id = request.POST.get("commitment_id")
            cap_id = request.POST.get("cap_id")
            commitment = Commitment.objects.get(id=commitment_id)
            provision_cart = ProvisionCart.objects.get(id=cap_id)
            project = provision_cart.project
            has_tax = project.is_it_taxable
            commitment.provision_cart = provision_cart
            commitment.provision_budget_amount = provision_cart.total_provisioned_amount
            commitment.has_tax = has_tax
            commitment.save()
            commitment.diference_between_required_and_provisioned = (
                commitment.provision_budget_amount - commitment.required_amount
            )
            commitment.save()
            # Create commitment realease
            CommitmentRelease.objects.filter(commitment=commitment).delete()
            commitment_release_dict = None
            if commitment.diference_between_required_and_provisioned > 0:
                commitment_release = CommitmentRelease.objects.create(
                    commitment=commitment,
                    total_to_release=commitment.diference_between_required_and_provisioned,
                )
                commitment_release_dict = {
                    "id": commitment_release.id,
                    "total_to_release": commitment_release.total_to_release,
                    "total_released": commitment_release.total_released,
                    "total_pending": commitment_release.total_pending,
                }
                provision_cart = commitment.provision_cart
                budgets = provision_cart.provision_cart_provision_budgets.all()
                release_items = []
                for budget in budgets:
                    commitment_release_item = CommitmentRealeaseItems.objects.create(
                        commitment_release=commitment_release,
                        budget=budget.budget,
                    )
                    release_items.append(
                        {
                            "id": commitment_release_item.id,
                            "budget_description": budget.budget.budget_description.description,
                            "total_to_release": commitment_release_item.total_to_release,
                        }
                    )
                commitment_release_dict["commitment_release_items"] = release_items

            return JsonResponse(
                {
                    "status": "ok",
                    "commitment": commitment.id,
                    "provision_cart": provision_cart.id,
                    "total_provisioned_amount": provision_cart.total_provisioned_amount,
                    "project": project.id,
                    "has_tax": commitment.has_tax,
                    "provision_budget_amount": commitment.provision_budget_amount,
                    "required_amount": commitment.required_amount,
                    "diference_between_required_and_provisioned": commitment.diference_between_required_and_provisioned,  # noqa
                    "commitment_release_dict": commitment_release_dict,
                },
                safe=False,
            )
        except Exception as e:
            return JsonResponse(
                {
                    "status": "error",
                    "message": str(e),
                },
                safe=False,
            )


class UpdateContractOrPoCap(LoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        try:
            commitment_id = request.POST.get("commitment_id")
            contract_or_po = request.POST.get("type")
            commitment = Commitment.objects.get(id=commitment_id)
            commitment.contract_or_po = contract_or_po
            commitment.save()
            return JsonResponse(
                {
                    "status": "ok",
                    "commitment": commitment.id,
                    "type": contract_or_po,
                },
                safe=False,
            )
        except Exception as e:
            return JsonResponse(
                {
                    "status": "error",
                    "message": str(e),
                },
                safe=False,
            )


class UpdateThirdOrPoCap(LoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        try:
            commitment_id = request.POST.get("commitment_id")
            third_id = request.POST.get("third_id")
            commitment = Commitment.objects.get(id=commitment_id)
            third = Third.objects.filter(IdTercer=third_id).last()
            commitment.third = third
            commitment.save()
            return JsonResponse(
                {
                    "status": "ok",
                    "commitment": commitment.id,
                    "third_id": third_id,
                    "third": third.name,
                },
                safe=False,
            )
        except Exception as e:
            return JsonResponse(
                {
                    "status": "error",
                    "message": str(e),
                },
                safe=False,
            )


class UpdateContractOrPoCapEntity(LoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        try:
            commitment_id = request.POST.get("commitment_id")
            commitment = Commitment.objects.get(id=commitment_id)
            contract_or_po = request.POST.get("contract_or_po")
            entity_id = request.POST.get("entity_id")
            if contract_or_po == "CT":
                contract = Contract.objects.get(IdContrato=entity_id)
                if CommitmentContract.objects.filter(
                    commitment=commitment,
                ).exists():
                    CommitmentContract.objects.filter(
                        commitment=commitment,
                    ).update(
                        contract=contract,
                    )
                else:
                    CommitmentContract.objects.create(
                        commitment=commitment,
                        contract=contract,
                    )
                if CommitmentPO.objects.filter(
                    commitment=commitment,
                ).exists():
                    CommitmentPO.objects.filter(
                        commitment=commitment,
                    ).delete()
                commitment.required_amount = contract.ValTot
                commitment.save()
                commitment.diference_between_required_and_provisioned = (
                    commitment.provision_budget_amount - commitment.required_amount
                )
                commitment.save()
            elif contract_or_po == "PO":
                po = PurchaseOrder.objects.get(Numero=entity_id)
                if CommitmentPO.objects.filter(
                    commitment=commitment,
                ).exists():
                    CommitmentPO.objects.filter(
                        commitment=commitment,
                    ).update(
                        po=po,
                    )
                else:
                    CommitmentPO.objects.create(
                        commitment=commitment,
                        po=po,
                    )
                if CommitmentContract.objects.filter(
                    commitment=commitment,
                ).exists():
                    CommitmentContract.objects.filter(
                        commitment=commitment,
                    ).delete()
                commitment.required_amount = po.VrNeto
                commitment.save()
                commitment.diference_between_required_and_provisioned = (
                    commitment.provision_budget_amount - commitment.required_amount
                )
                commitment.save()
            # Create commitment realease
            CommitmentRelease.objects.filter(commitment=commitment).delete()
            if commitment.diference_between_required_and_provisioned > 0:
                commitment_release = CommitmentRelease.objects.create(
                    commitment=commitment,
                    total_to_release=commitment.diference_between_required_and_provisioned,
                )
                provision_cart = commitment.provision_cart
                budgets = provision_cart.provision_cart_provision_budgets.all()
                for budget in budgets:
                    CommitmentRealeaseItems.objects.create(
                        commitment_release=commitment_release,
                        budget=budget.budget,
                    )
            return JsonResponse(
                {
                    "status": "ok",
                    "commitment": commitment.id,
                    "type": contract_or_po,
                    "has_tax": commitment.has_tax,
                    "provision_budget_amount": commitment.provision_budget_amount,
                    "required_amount": commitment.required_amount,
                    "diference_between_required_and_provisioned": commitment.diference_between_required_and_provisioned,  # noqa
                },
                safe=False,
            )
        except Exception as e:
            return JsonResponse(
                {
                    "status": "error",
                    "message": str(e),
                    "commitment": commitment.id,
                    "type": contract_or_po,
                    "entity_id": entity_id,
                },
                safe=False,
            )


class CommitmentReleaseUpdateView(LoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        try:
            commiment_release_item_id = request.POST.get("commiment_release_item_id")
            commitment_release_amount = request.POST.get("commitment_release_amount")
            commiment_release_item = CommitmentRealeaseItems.objects.get(id=commiment_release_item_id)
            commiment_release_item.total_to_release = commitment_release_amount
            commiment_release_item.save()
            commitment_release = commiment_release_item.commitment_release
            total_released = 0
            for item in commitment_release.commitment_release_items.all():
                total_released = total_released + item.total_to_release

            commitment_release.total_released = total_released
            commitment_release.save()
            return JsonResponse(
                {
                    "status": "ok",
                    "total_to_release": commitment_release.total_to_release,
                    "total_released": commitment_release.total_released,
                    "total_pending": commitment_release.total_pending,
                },
                safe=False,
            )
        except Exception as e:
            return JsonResponse(
                {
                    "status": "error",
                    "message": str(e),
                },
                safe=False,
            )
