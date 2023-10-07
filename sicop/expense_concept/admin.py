from django.contrib import admin

from sicop.expense_concept.models import ExpenseConcept


@admin.register(ExpenseConcept)
class ExpenseConceptAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "id",
        "status",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "status",
        "created_at",
        "updated_at",
    )
    search_fields = ("name",)
    ordering = (
        "code",
        "name",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "id",
        "code",
    )
