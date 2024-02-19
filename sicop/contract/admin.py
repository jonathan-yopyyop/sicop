from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from sicop.contract.models import Contract


class ContractResource(resources.ModelResource):
    class Meta:
        model = Contract


@admin.register(Contract)
class ContractAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [ContractResource]
    list_display = (
        "IdContrato",
        "TipContrato",
        "Cumplido",
        "Estado",
        "IdTercer",
        "IdCenCos",
        "FechaCon",
        "FechaIni",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "IdContrato",
        "TipContrato",
        "Cumplido",
        "Estado",
        "IdTercer",
        "IdCenCos",
        "FechaCon",
        "FechaIni",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "IdContrato",
        "TipContrato",
        "Cumplido",
        "Estado",
        "IdTercer",
        "IdCenCos",
        "FechaCon",
        "FechaIni",
    )
    ordering = (
        "IdContrato",
        "TipContrato",
        "Cumplido",
        "Estado",
        "IdTercer",
        "IdCenCos",
        "FechaCon",
        "FechaIni",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
