from django.contrib import admin
from sicop.maloka_da.models import ActiveDirectoryCredential, OrganizationalUnit, ActiveDirectoryUser
from sicop.maloka_da.forms import ActiveDirectoryCredentialForm
from import_export.admin import ImportExportModelAdmin


@admin.register(ActiveDirectoryCredential)
class ActiveDirectoryCredentialAdmin(admin.ModelAdmin):
    form = ActiveDirectoryCredentialForm
    list_display = [
        "domain",
        "domain_extension",
        "id",
        "username",
        "status",
    ]
    search_fields = [
        "domain",
        "domain_extension",
        "username",
    ]


@admin.register(OrganizationalUnit)
class OrganizationalUnitAdmin(admin.ModelAdmin):
    list_display = [
        "credential",
        "OU",
        "id",
        "status",
    ]
    search_fields = [
        "OU",
    ]


@admin.register(ActiveDirectoryUser)
class ActiveDirectoryUserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = [
        "organizational_unit",
        "name",
        "user",
        "area",
        "role",
        "security_group",
        "status",
    ]
    search_fields = [
        "name",
        "user",
        "area",
        "role",
        "security_group",
    ]
