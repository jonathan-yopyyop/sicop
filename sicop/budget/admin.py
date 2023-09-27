from django.contrib import admin

from sicop.budget.models import Budget, BudgetDescription


@admin.register(BudgetDescription)
class BudgetDescriptionAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "description",
    )
    search_fields = (
        "code",
        "description",
    )


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = (
        "project",
        "cost_center",
        "expense_type",
        "budget_description",
        "expense_type",
        "budget_description",
        "unit_value",
        "quantity",
        "initial_value",
        "budget_addition",
        "budget_decrease",
        "current_budget",
        "created_at",
        "updated_at",
        "status",
    )
    search_fields = (
        "project__name",
        "cost_center__code",
        "expense_type__code",
        "budget_description__code",
        "expense_type__code",
        "start_date",
        "budget_description__code",
    )
    list_filter = (
        "project",
        "cost_center",
        "expense_type",
        "budget_description",
        "expense_type",
        "budget_description",
        "status",
    )
