from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from sicop.integration.models import ActiveIntegration, BusinessUnit, CostCenter, ExpenseType, Third


class ThirdResource(resources.ModelResource):
    class Meta:
        model = Third


@admin.register(Third)
class ThirdAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [ThirdResource]
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


class CostCenterResource(resources.ModelResource):
    class Meta:
        model = CostCenter


@admin.register(CostCenter)
class CostCenterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [CostCenterResource]
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


class BusinessUnitResource(resources.ModelResource):
    class Meta:
        model = BusinessUnit


@admin.register(BusinessUnit)
class BusinessUnitAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [BusinessUnitResource]
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


class ExpenseTypeResource(resources.ModelResource):
    class Meta:
        model = ExpenseType


@admin.register(ExpenseType)
class ExpenseTypeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [ExpenseTypeResource]
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
