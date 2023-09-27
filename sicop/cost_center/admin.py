from django.contrib import admin

from sicop.cost_center.models import CostCategory, CostCenter


@admin.register(CostCategory)
class CostCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
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
    ordering = (
        "name",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(CostCenter)
class CostCenterAdmin(admin.ModelAdmin):
    list_display = (
        "cost_center_id",
        "name",
        "description",
        "cost_category",
        "area",
        "status",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "cost_category",
        "area",
        "status",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "cost_center_id",
        "name",
        "description",
        "cost_category",
        "area",
    )
    ordering = (
        "cost_center_id",
        "name",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
