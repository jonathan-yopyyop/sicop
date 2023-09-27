from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CostCenterConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sicop.cost_center"
    verbose_name = _("Cost Center")
