from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView

from sicop.integration.models import Third


@method_decorator(csrf_exempt, name="dispatch")
class GetThirdByCriteria(TemplateView):
    def get(self, request, *args, **kwargs):
        query = request.GET.get("q", "")
        results = Third.objects.filter(
            IdTercer__icontains=query,
        )
        result_list = []
        dni = _("DNI")
        name = _("Third")
        for result in results:
            result_list.append(
                {
                    "id": result.IdTercer,
                    "text": f"{dni} {result.IdTercer} {name} {result.Nombre}",
                }
            )
        return JsonResponse(
            result_list,
            safe=False,
        )
