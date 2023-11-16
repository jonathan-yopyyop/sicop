from django.contrib import admin

from sicop.budget.models import Budget, BudgetCap, BudgetDescription


@admin.register(BudgetDescription)
class BudgetDescriptionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "expense_concept",
        "description",
    )
    search_fields = (
        "expense_concept",
        "description",
    )


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = (
        "id",
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
        "budget_description__code",
        "start_date",
        "budget_description__code",
    )
    list_filter = (
        "project",
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


@admin.register(BudgetCap)
class BudgetCapAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "business_unit",
        "cap",
        "description",
        "status",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "business_unit__code",
        "description",
    )
    list_filter = (
        "business_unit",
        "description",
        "status",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
