from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ExpenseTypeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sicop.expense_type"
    verbose_name = _("Expense Type")
