import traceback
from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from sicop.area.models import AreaMember
from sicop.budget.models import (
    Budget,
    Commitment,
    CommitmentContract,
    CommitmentNotRelated,
    CommitmentOrphanRealeaseItems,
    CommitmentPO,
    CommitmentRealeaseItems,
    CommitmentRelease,
    ProvisionCart,
)
from sicop.budget.models.commitment import get_commitment_types
from sicop.certificate.models import Certificate
from sicop.contract.models import Contract
from sicop.integration.models import Third
from sicop.purchase_order.models import PurchaseOrder


class CommitmentListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    template_name = "sicop/frontend/budget/processes/commitment/list.html"
    model = Commitment
    context_object_name = "commitments"
    permission_required = "budget.view_commitment"


class CommitmentCreateView(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = "sicop/frontend/budget/processes/commitment/create.html"
    permission_required = "budget.add_commitment"

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
        context["commitment_not_related"] = CommitmentNotRelated.objects.filter(
            commitment=commitment,
        ).last()
        context["commitment_release"] = CommitmentRelease.objects.filter(
            commitment=commitment,
        ).last()
        return context

    def post(self, request, *args, **kwargs):
        commitment_object_id = request.POST.get("commitment_object_id")
        commitment = Commitment.objects.get(id=commitment_object_id)
        commitment.status = False
        commitment.finished = True
        commitment.save()
        commitment_release = CommitmentRelease.objects.filter(
            commitment=commitment,
        ).last()
        if commitment_release is not None:
            commitment_release_items = commitment_release.commitment_release_items.all()
            for item in commitment_release_items:
                budget: Budget = item.budget
                budget.released_amount = budget.released_amount + item.total_to_release
                budget.save()
        return HttpResponseRedirect(
            reverse(
                "commitment_certificate",
                kwargs={"pk": commitment.id},
            )
        )


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
            if not commitment.has_tax:
                commitment.tax_amount = 0
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
                budgets_count = provision_cart.provision_cart_provision_budgets.count()
                for budget in budgets:
                    commitment_release_item = CommitmentRealeaseItems.objects.create(
                        commitment_release=commitment_release,
                        budget=budget.budget,
                        budget_amount=budget.available_budget,
                    )
                    if budgets_count == 1:
                        commitment_release_item.total_to_release = commitment_release.total_to_release
                        commitment_release_item.save()
                        commitment_release.total_released = commitment_release.total_to_release
                        commitment_release.save()

                    release_items.append(
                        {
                            "id": commitment_release_item.id,
                            "budget_description": budget.budget.budget_description.description,
                            "current_budget": budget.budget.current_budget,
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
            commitment.third = None
            commitment.tax_amount = 0
            commitment.required_amount = 0
            commitment.diference_between_required_and_provisioned = 0
            commitment.save()
            CommitmentRelease.objects.filter(
                commitment=commitment,
            ).delete()
            if contract_or_po == "CT":
                CommitmentPO.objects.filter(
                    commitment=commitment,
                ).delete()
                CommitmentNotRelated.objects.filter(
                    commitment=commitment,
                ).delete()
            elif contract_or_po == "PO":
                CommitmentContract.objects.filter(
                    commitment=commitment,
                ).delete()
                CommitmentNotRelated.objects.filter(
                    commitment=commitment,
                ).delete()
            else:
                CommitmentContract.objects.filter(
                    commitment=commitment,
                ).delete()
                CommitmentPO.objects.filter(
                    commitment=commitment,
                ).delete()
                if contract_or_po == "CO":
                    CommitmentNotRelated.objects.filter(
                        commitment=commitment,
                        type="LG",
                    ).delete()
                    if not CommitmentNotRelated.objects.filter(
                        commitment=commitment,
                        type="CO",
                    ).exists():
                        CommitmentNotRelated.objects.create(
                            commitment=commitment,
                            type="CO",
                        )
                elif contract_or_po == "LG":
                    CommitmentNotRelated.objects.filter(
                        commitment=commitment,
                        type="CO",
                    ).delete()
                    if not CommitmentNotRelated.objects.filter(
                        commitment=commitment,
                        type="LG",
                    ).exists():
                        CommitmentNotRelated.objects.create(
                            commitment=commitment,
                            type="LG",
                        )
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
            third = Third.objects.filter(IdTercer__icontains=third_id).last()
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


class UpdateCommitmentEntity(LoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        try:
            commitment_id = request.POST.get("commitment_id")
            commitment = Commitment.objects.get(id=commitment_id)
            contract_or_po = request.POST.get("contract_or_po")
            entity_id = request.POST.get("entity_id")
            tax_amount = 0
            if contract_or_po == "CT":
                contract = Contract.objects.get(IdContrato=entity_id)
                third_id = contract.IdTercer
                third = Third.objects.filter(IdTercer__icontains=third_id).last()
                commitment.third = third
                commitment.save()
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
                tax_amount = contract.ValIVA
                commitment.required_amount = contract.ValTot
                commitment.tax_amount = contract.ValIVA
                commitment.save()
                commitment.diference_between_required_and_provisioned = (
                    commitment.provision_budget_amount - commitment.required_amount
                )
                commitment.save()
                deleted = False
            elif contract_or_po == "PO":
                po = PurchaseOrder.objects.get(Numero=entity_id)
                third_id = po.IdTercer
                third = Third.objects.filter(IdTercer__icontains=third_id).last()
                commitment.third = third
                commitment.save()
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
                tax_amount = po.VrIva
                commitment.required_amount = po.VrNeto
                commitment.tax_amount = po.VrIva
                commitment.save()
                commitment.diference_between_required_and_provisioned = (
                    commitment.provision_budget_amount - commitment.required_amount
                )
                commitment.save()
                deleted = False
            elif contract_or_po == "CO" or contract_or_po == "LG":
                third = None
                CommitmentContract.objects.filter(
                    commitment=commitment,
                ).delete()
                CommitmentPO.objects.filter(
                    commitment=commitment,
                ).delete()
                deleted = True

            # Create commitment realease
            CommitmentRelease.objects.filter(commitment=commitment).delete()
            release_items = []
            if commitment.diference_between_required_and_provisioned > 0:
                commitment_release = CommitmentRelease.objects.create(
                    commitment=commitment,
                    total_to_release=commitment.diference_between_required_and_provisioned,
                )
                provision_cart = commitment.provision_cart
                budgets = provision_cart.provision_cart_provision_budgets.all()
                budgets_count = provision_cart.provision_cart_provision_budgets.count()
                release_items = []
                for budget in budgets:
                    commitment_release_item = CommitmentRealeaseItems.objects.create(
                        commitment_release=commitment_release,
                        budget=budget.budget,
                        budget_amount=budget.available_budget,
                    )
                    if budgets_count == 1:
                        commitment_release_item.total_to_release = commitment_release.total_to_release
                        commitment_release_item.save()
                        commitment_release.total_released = commitment_release.total_to_release
                        commitment_release.save()
                    release_items.append(
                        {
                            "id": commitment_release_item.id,
                            "budget_description": budget.budget.budget_description.description,
                            "current_budget": budget.budget.current_budget,
                            "total_to_release": commitment_release_item.total_to_release,
                            "budgets_count": budgets_count,
                        }
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
                    "tax_amount": tax_amount,
                    "deleted": deleted,
                    "third_id": third.id,
                    "third": str(third),
                    "release_items": release_items,
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
            count = commitment_release.commitment_release_items.count()
            for item in commitment_release.commitment_release_items.all():
                total_released = total_released + item.total_to_release
                if count == 1:
                    item.total_to_release = commitment_release.total_to_release
                    item.save()
                    commitment_release.total_released = commitment_release.total_to_release
                    commitment_release.save()

            commitment_release.total_released = total_released
            commitment_release.save()
            negative_surplus = 0
            exceeded = False
            if commitment_release.total_pending < 0:
                exceeded = True
                negative_surplus = commitment_release.total_pending
                commiment_release_item.total_to_release = (
                    float(commiment_release_item.total_to_release) + negative_surplus
                )
                commiment_release_item.save()
                commitment_release.total_released = float(commitment_release.total_released) + negative_surplus
                commitment_release.save()
            return JsonResponse(
                {
                    "status": "ok",
                    "total_to_release": commitment_release.total_to_release,
                    "total_released": commitment_release.total_released,
                    "total_pending": commitment_release.total_pending,
                    "negative_surplus": negative_surplus,
                    "exceeded": exceeded,
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


class CommitmentTaxUpdateView(LoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        try:
            commitment_id = request.POST.get("commitment_id")
            tax_amount = request.POST.get("tax_amount")
            commitment = Commitment.objects.get(id=commitment_id)
            commitment.tax_amount = tax_amount
            commitment.save()

            return JsonResponse(
                {
                    "status": "ok",
                    "commitment": commitment.id,
                    "tax_amount": commitment.tax_amount,
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


class UpdateIdentifier(LoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        try:
            commitment_id = request.POST.get("commitment_id")
            identifier = request.POST.get("identifier")
            commitment = Commitment.objects.get(id=commitment_id)
            commitment_not_related = CommitmentNotRelated.objects.filter(
                commitment=commitment,
            ).last()
            commitment_not_related.key = identifier
            commitment_not_related.save()
            return JsonResponse(
                {
                    "status": "ok",
                    "commitment": commitment.id,
                    "commitment_not_related": commitment_not_related.id,
                    "identifier": identifier,
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


class UpdateCommitmentAmount(LoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        try:
            commitment_id = request.POST.get("commitment_id")
            amount = request.POST.get("amount")
            commitment = Commitment.objects.get(id=commitment_id)
            commitment.required_amount = float(amount)
            commitment.save()
            commitment.diference_between_required_and_provisioned = float(commitment.provision_budget_amount) - float(
                commitment.required_amount
            )
            commitment.save()
            return JsonResponse(
                {
                    "status": "ok",
                    "commitment": commitment.id,
                    "amount": amount,
                    "provision_budget_amount": commitment.provision_budget_amount,
                    "required_amount": commitment.required_amount,
                    "diference_between_required_and_provisioned": commitment.diference_between_required_and_provisioned,  # noqa
                    "total_provisioned_amount": commitment.provision_cart.total_provisioned_amount,
                },
                safe=False,
            )
        except Exception as e:
            traceback.print_exc()
            exception_info = traceback.format_exception_only(type(e), e)

            return JsonResponse(
                {
                    "status": "error",
                    "message": str(e),
                    "details": "".join(exception_info),
                },
                safe=False,
            )


class CreateOrdestroyReleaseTable(LoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        try:
            commitment_id = request.POST.get("commitment_id")
            commitment = Commitment.objects.get(id=commitment_id)

            if commitment.diference_between_required_and_provisioned > 0:
                CommitmentRelease.objects.filter(commitment=commitment).delete()
                commitment_release = CommitmentRelease.objects.create(
                    commitment=commitment,
                    total_to_release=commitment.diference_between_required_and_provisioned,
                )
                provision_cart = commitment.provision_cart
                budgets = provision_cart.provision_cart_provision_budgets.all()
                budgets_count = provision_cart.provision_cart_provision_budgets.count()
                release_items = []
                for budget in budgets:
                    commitment_release_item = CommitmentRealeaseItems.objects.create(
                        commitment_release=commitment_release,
                        budget=budget.budget,
                        budget_amount=budget.available_budget,
                    )
                    if budgets_count == 1:
                        commitment_release.total_to_release = commitment_release.total_to_release
                        commitment_release.save()
                        commitment_release.total_released = commitment_release.total_to_release
                        commitment_release.save()
                    release_items.append(
                        {
                            "id": commitment_release_item.id,
                            "budget_description": budget.budget.budget_description.description,
                            "current_budget": budget.budget.current_budget,
                            "total_to_release": commitment_release_item.total_to_release,
                        }
                    )
                return JsonResponse(
                    {
                        "status": "ok",
                        "commitment": commitment.id,
                        "commitment_release": commitment_release.id,
                        "total_to_release": commitment_release.total_to_release,
                        "total_released": commitment_release.total_released,
                        "total_pending": commitment_release.total_pending,
                        "commitment_release_items": release_items,
                    },
                    safe=False,
                )
            else:
                CommitmentRelease.objects.filter(commitment=commitment).delete()
                return JsonResponse(
                    {
                        "status": "ok",
                        "commitment": commitment.id,
                        "commitment_release": None,
                    },
                    safe=False,
                )
        except Exception as e:
            traceback.print_exc()
            exception_info = traceback.format_exception_only(type(e), e)
            return JsonResponse(
                {
                    "status": "error",
                    "message": str(e),
                    "details": "".join(exception_info),
                },
                safe=False,
            )


class CommitmentCertificateView(LoginRequiredMixin, TemplateView):
    template_name = "sicop/frontend/budget/processes/commitment/commitment_certificate.html"
    permission_required = "budget.add_commitment"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get("pk")
        commitment = Commitment.objects.get(id=pk)
        user = commitment.user
        if AreaMember.objects.filter(user=user).exists():
            area_member = AreaMember.objects.filter(user=user).last()
            area_rol = area_member.role
        else:
            area_member = None
            area_rol = None
        context["commitment"] = commitment
        context["area_rol"] = area_rol
        context["area_member"] = area_member
        context["certificate_version"] = Certificate.objects.filter(slug="commitment").first()
        context["commitment_release"] = CommitmentRelease.objects.filter(
            commitment=commitment,
        ).last()

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


class CommitmentReleaseOrphanUpdateView(LoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        try:
            commiment_release_item_id = request.POST.get("id")
            commitment_release_amount = float(request.POST.get("released_value"))

            commiment_release_orphan_item = CommitmentOrphanRealeaseItems.objects.get(id=commiment_release_item_id)
            commiment_release_orphan_item.total_to_release = commitment_release_amount
            commiment_release_orphan_item.save()

            commitment_orphan_release = commiment_release_orphan_item.commitment_release
            commitment_orphan_release_items = CommitmentOrphanRealeaseItems.objects.filter(
                commitment_release=commitment_orphan_release,
            )
            total_released = 0
            for item in commitment_orphan_release_items:
                total_released = total_released + item.total_to_release
            commitment_orphan_release.total_released = total_released
            commitment_orphan_release.save()

            return JsonResponse(
                {
                    "status": "ok",
                    "total_to_release": commitment_orphan_release.total_to_release,
                    "total_released": commitment_orphan_release.total_released,
                    "total_pending": 0,
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
