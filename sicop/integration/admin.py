from django.contrib import admin

from sicop.integration.models import ActiveIntegration, BusinessUnit, CostCenter, ExpenseType, Third


@admin.register(Third)
class ThirdAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "Nombre",
        "status",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "id",
        "Nombre",
        "status",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "id",
        "Nombre",
    )
    ordering = (
        "id",
        "Nombre",
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
        "id",
        "Nombre",
        "status",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "id",
        "Nombre",
        "status",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "id",
        "Nombre",
    )
    ordering = (
        "id",
        "Nombre",
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
        "id",
        "Nombre",
        "status",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "id",
        "Nombre",
        "status",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "id",
        "Nombre",
    )
    ordering = (
        "id",
        "Nombre",
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
        "id",
        "Nombre",
        "status",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "id",
        "Nombre",
        "status",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "id",
        "Nombre",
    )
    ordering = (
        "id",
        "Nombre",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(ActiveIntegration)
class ActiveIntegrationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "code",
        "status",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "id",
        "name",
        "code",
        "status",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "id",
        "name",
        "code",
    )
    ordering = (
        "id",
        "name",
        "code",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
