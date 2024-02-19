from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from sicop.project.models import Project, ProjectStatus, ProjectStatusHistory, ProjectType


class ProjectResource(resources.ModelResource):
    class Meta:
        model = Project


@admin.register(ProjectStatus)
class ProjectStatusAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [ProjectResource]
    list_display = (
        "name",
        "id",
        "status",
        "created_at",
        "updated_at",
    )
    list_filter = (
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
        "id",
        "code",
    )


class ProjectTypeResource(resources.ModelResource):
    class Meta:
        model = ProjectType


@admin.register(ProjectType)
class ProjectTypeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [ProjectTypeResource]
    list_display = (
        "name",
        "id",
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
        "id",
        "code",
    )


class ProjectResource(resources.ModelResource):
    class Meta:
        model = Project


@admin.register(Project)
class ProjectAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [ProjectResource]
    list_display = (
        "name",
        "id",
        "description",
        "budget",
        "project_status",
        "project_type",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "project_status",
        "project_type",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "name",
        "description",
        "budget",
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


class ProjectStatusHistoryResource(resources.ModelResource):
    class Meta:
        model = ProjectStatusHistory


@admin.register(ProjectStatusHistory)
class ProjectStatusHistoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [ProjectStatusHistoryResource]
    list_display = (
        "project",
        "id",
        "project_status",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "project__name",
        "project_status",
        "created_at",
        "updated_at",
    )
    search_fields = ("project",)
    ordering = (
        "project",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "id",
    )
