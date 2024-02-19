from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from sicop.expense_type.models import ExpenseType


class ExpenseTypeResource(resources.ModelResource):
    class Meta:
        model = ExpenseType


@admin.register(ExpenseType)
class ExpenseTypeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [ExpenseTypeResource]
    list_display = (
        "name",
        "id",
        "status",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "name",
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
