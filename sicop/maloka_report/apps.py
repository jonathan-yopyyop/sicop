from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MalokaReportConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sicop.maloka_report"
    verbose_name = _("Maloka Report")
