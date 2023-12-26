from django.contrib import admin

from sicop.certificate.models import Certificate


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
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
