from django.contrib import admin

from sicop.contract.models import Contract


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
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
