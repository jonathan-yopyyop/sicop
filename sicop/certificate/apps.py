from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CertificateConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sicop.certificate"
    verbose_name = _("Certificate")
