from django.contrib import admin

from sicop.project.models import Project, ProjectStatus, ProjectStatusHistory, ProjectType

# Register your models here.
admin.site.register(ProjectStatus)


class ProjectStatusAdmin(admin.ModelAdmin):
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


@admin.register(ProjectType)
class ProjectTypeAdmin(admin.ModelAdmin):
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


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
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


@admin.register(ProjectStatusHistory)
class ProjectStatusHistoryAdmin(admin.ModelAdmin):
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
