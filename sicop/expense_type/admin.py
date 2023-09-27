from django.contrib import admin

from sicop.expense_type.models import ExpenseType


@admin.register(ExpenseType)
class ExpenseTypeAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "name",
        "status",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "code",
        "name",
        "status",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "code",
        "name",
    )
    ordering = (
        "code",
        "name",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
