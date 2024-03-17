from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView

from sicop.purchase_order.models import PurchaseOrder


@method_decorator(csrf_exempt, name="dispatch")
class GetPosByCriteria(TemplateView):
    def get(self, request, *args, **kwargs):
        query = request.GET.get("q", "")
        results = PurchaseOrder.objects.filter(
            Numero__icontains=query,
        )
        result_list = []
        po = _("PO")
        third = _("Third")
        for result in results:
            result_list.append(
                {
                    "id": result.Numero,
                    "text": f"{po} {result.Numero} {third} {result.IdTercer}",
                }
            )
        return JsonResponse(
            result_list,
            safe=False,
        )
