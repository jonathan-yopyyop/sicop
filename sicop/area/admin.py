from django.contrib import admin

from sicop.area.models import Area, AreaMember, AreaRole


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
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


@admin.register(AreaMember)
class AreaMembersAdmin(admin.ModelAdmin):
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


@admin.register(AreaRole)
class AreaRoleAdmin(admin.ModelAdmin):
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
