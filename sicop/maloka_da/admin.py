from django.contrib import admin
from sicop.maloka_da.models import ActiveDirectoryCredential, OrganizationalUnit, ActiveDirectoryUser
from sicop.maloka_da.forms import ActiveDirectoryCredentialForm


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


@admin.register(OrganizationalUnit)
class OrganizationalUnitAdmin(admin.ModelAdmin):
    list_display = [
        "credential",
        "OU",
        "id",
        "status",
    ]


@admin.register(ActiveDirectoryUser)
class ActiveDirectoryUserAdmin(admin.ModelAdmin):
    list_display = [
        "organizational_unit",
        "name",
        "user",
        "id",
        "status",
    ]
