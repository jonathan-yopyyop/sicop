from django.contrib import admin

from sicop.budget.models import Budget, BudgetDescription


@admin.register(BudgetDescription)
class BudgetDescriptionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "expense_type",
        "description",
    )
    search_fields = (
        "expense_type",
        "description",
    )


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "cost_center",
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
        "budget_description__code",
        "start_date",
        "budget_description__code",
    )
    list_filter = (
        "project",
        "cost_center",
        "budget_description",
        "budget_description",
        "status",
    )
    readonly_fields = (
        "initial_value",
        "budget_addition",
        "budget_decrease",
        "created_at",
        "updated_at",
    )
