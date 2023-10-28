from django.contrib import admin

from sicop.contractor.models import Contractor, ContractorFile

# Register your models here.


@admin.register(Contractor)
class ContractorAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "commertial_name",
        "dni",
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
        "commertial_name",
        "dni",
        "contractor_type",
    )
    ordering = (
        "id",
        "name",
        "commertial_name",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(ContractorFile)
class ContractorFileAdmin(admin.ModelAdmin):
    list_display = (
        "contractor",
        "file",
        "status",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "contractor__name",
        "contractor__commertial_name",
        "contractor__dni",
        "status",
        "created_at",
        "updated_at",
    )
    search_fields = ("contractor",)
    ordering = (
        "contractor",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
