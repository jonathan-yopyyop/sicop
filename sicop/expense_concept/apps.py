from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ExpenseConceptConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sicop.expense_concept"
    verbose_name = _("Expense Concept")
