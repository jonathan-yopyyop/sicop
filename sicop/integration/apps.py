from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class IntegrationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sicop.integration"
    verbose_name = _("Integration")
