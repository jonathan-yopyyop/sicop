from django.contrib import admin

from sicop.cost_center.models import CostCenter


@admin.register(CostCenter)
class CostCenterAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "id",
        "description",
        "area",
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
