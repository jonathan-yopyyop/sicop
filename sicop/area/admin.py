from django.contrib import admin

from sicop.area.models import Area, AreaMember


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = (
        "name",
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
    )


@admin.register(AreaMember)
class AreaMembersAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "area",
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
    )
