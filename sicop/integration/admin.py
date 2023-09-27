from django.contrib import admin

from sicop.integration.models import BusinessUnit, CostCenter, ExpenseType, Third


@admin.register(Third)
class ThirdAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "first_name",
        "last_name",
        "status",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "code",
        "first_name",
        "last_name",
        "status",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "code",
        "first_name",
        "last_name",
    )
    ordering = (
        "code",
        "first_name",
        "last_name",
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


@admin.register(BusinessUnit)
class BusinessUnitAdmin(admin.ModelAdmin):
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
