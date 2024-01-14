from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView

from sicop.contract.models import Contract


@method_decorator(csrf_exempt, name="dispatch")
class GetContractsByCriteria(TemplateView):
    def get(self, request, *args, **kwargs):
        query = request.GET.get("q", "")
        results = Contract.objects.filter(
            IdContrato__icontains=query,
        )
        result_list = []
        third = _("Third")
        contract = _("Contract")
        for result in results:
            result_list.append(
                {
                    "id": result.IdContrato,
                    "text": f"{contract} {result.IdContrato} {third} {result.IdTercer}",
                }
            )
        return JsonResponse(
            result_list,
            safe=False,
        )
