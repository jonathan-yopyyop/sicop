from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BusinessUnitConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sicop.business_unit"
    verbose_name = _("Business Unit")
