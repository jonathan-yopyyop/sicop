from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PurchaseOrderConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sicop.purchase_order"
    verbose_name = _("Purchase Order")
