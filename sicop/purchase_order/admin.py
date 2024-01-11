from django.contrib import admin

from sicop.purchase_order.models import PurchaseOrder


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
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
