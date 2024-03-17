from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SicopErrorHandlerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sicop.sicop_error_handler"
    verbose_name = _("Sicop Error Handler")
