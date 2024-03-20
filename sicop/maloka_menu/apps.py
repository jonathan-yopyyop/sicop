from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MalokaMenuConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sicop.maloka_menu"
    verbose_name = _("Menu")
