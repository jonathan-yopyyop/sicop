from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from sicop.cost_center.models import CostCenter


class CostCenterResource(resources.ModelResource):
    class Meta:
        model = CostCenter


@admin.register(CostCenter)
class CostCenterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [CostCenterResource]
    list_display = (
        "name",
        "id",
        "description",
        "status",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "status",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "name",
        "description",
    )
    ordering = ("id",)
    readonly_fields = (
        "created_at",
        "updated_at",
        "cost_center_id",
        "id",
    )
