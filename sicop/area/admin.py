from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from sicop.area.models import Area, AreaMember, AreaRole


class AreaResource(resources.ModelResource):
    class Meta:
        model = Area


@admin.register(Area)
class AreaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [AreaResource]
    list_display = (
        "name",
        "id",
        "description",
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
        "description",
    )
    ordering = (
        "name",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "id",
    )


class AreaMemberResource(resources.ModelResource):
    class Meta:
        model = AreaMember


@admin.register(ImportExportModelAdmin, AreaMember)
class AreaMembersAdmin(admin.ModelAdmin):
    resource_classes = [AreaMemberResource]
    list_display = (
        "user_full_name",
        "id",
        "user",
        "area",
        "job_title",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "created_at",
        "updated_at",
    )
    search_fields = (
        "user",
        "area",
        "job_title",
    )
    ordering = (
        "user",
        "area",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "id",
    )


class AreaRoleResource(resources.ModelResource):
    class Meta:
        model = AreaRole


@admin.register(ImportExportModelAdmin, AreaRole)
class AreaRoleAdmin(admin.ModelAdmin):
    resource_classes = [AreaRoleResource]
    list_display = (
        "name",
        "id",
        "code",
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
        "code",
    )
    ordering = (
        "name",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "id",
    )
