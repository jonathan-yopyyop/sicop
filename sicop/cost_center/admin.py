from django.contrib import admin

from sicop.cost_center.models import CostCenter


@admin.register(CostCenter)
class CostCenterAdmin(admin.ModelAdmin):
    list_display = (
        # "cost_center_id",
        "name",
        # "description",
        # "cost_category",
        # "area",
        "status",
        "created_at",
        "updated_at",
    )
    list_filter = (
        # "cost_category",
        # "area",
        "status",
        "created_at",
        "updated_at",
    )
    search_fields = (
        # "cost_center_id",
        "name",
        "description",
        # "cost_category",
        # "area",
    )
    ordering = (
        # "cost_center_id",
        "name",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
