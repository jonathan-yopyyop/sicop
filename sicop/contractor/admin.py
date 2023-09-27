from django.contrib import admin

from sicop.contractor.models import Contractor, ContractorFile

# Register your models here.


@admin.register(Contractor)
class ContractorAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "email",
        "phone",
        "address",
        "dni",
        "contractor_type",
        "status",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "contractor_type",
        "status",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "first_name",
        "last_name",
        "email",
        "phone",
        "address",
        "dni",
        "contractor_type",
    )
    ordering = (
        "first_name",
        "last_name",
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
        "contractor__email",
        "contractor__first_name",
        "contractor__last_name",
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
