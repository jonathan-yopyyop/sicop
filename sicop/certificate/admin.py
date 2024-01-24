from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from sicop.certificate.models import Certificate


class CertificateResource(resources.ModelResource):
    class Meta:
        model = Certificate


@admin.register(Certificate)
class CertificateAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [CertificateResource]
    list_display = (
        "slug",
        "name",
        "version",
        "id",
        "status",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "slug",
        "name",
        "version",
        "status",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "slug",
        "name",
        "version",
    )
    ordering = (
        "slug",
        "name",
        "version",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "id",
    )
