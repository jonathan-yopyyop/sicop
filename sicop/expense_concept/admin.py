from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from sicop.expense_concept.models import ExpenseConcept


class ExpenseConceptResource(resources.ModelResource):
    class Meta:
        model = ExpenseConcept


@admin.register(ExpenseConcept)
class ExpenseConceptAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [ExpenseConceptResource]
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
