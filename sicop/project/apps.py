from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProjectConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sicop.project"
    verbose_name = _("Project")
