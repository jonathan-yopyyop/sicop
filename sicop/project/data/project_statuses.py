from django.utils.translation import gettext_lazy as _

STATUSES = [
    {
        "id": 1,
        "code": "started",
        "name": _("Iniciado"),
    },
    {
        "id": 2,
        "code": "in_process",
        "name": _("En Proceso"),
    },
    {
        "id": 3,
        "code": "finished",
        "name": _("Finalizado"),
    },
    {
        "id": 4,
        "code": "canceled",
        "name": _("Cancelado"),
    },
]
