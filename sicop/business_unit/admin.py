from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from sicop.business_unit.models import BusinessUnit


class BusinessUnitResource(resources.ModelResource):
    class Meta:
        model = BusinessUnit


@admin.register(BusinessUnit)
class BusinessUnitAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "status",
        "created_at",
        "updated_at",
        "code",
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
        "id",
        "code",
    )
