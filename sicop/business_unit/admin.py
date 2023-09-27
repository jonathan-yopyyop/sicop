from django.contrib import admin

from sicop.business_unit.models import BusinessUnit


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
