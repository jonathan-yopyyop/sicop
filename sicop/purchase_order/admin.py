from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from sicop.purchase_order.models import PurchaseOrder


class PurchaseOrderResource(resources.ModelResource):
    class Meta:
        model = PurchaseOrder


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [PurchaseOrderResource]
    list_display = (
        "id",
        "Numero",
        "status",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "status",
        "created_at",
        "updated_at",
    )
    search_fields = ("id",)
    ordering = (
        "id",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
