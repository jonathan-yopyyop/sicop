from django.contrib import admin
from sicop.maloka_menu.models import Menu, MenuOption, MenuGroup
from django import forms


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = [
        "menu",
        "group",
        "icon",
        "slug",
        "status",
    ]
    search_fields = [
        "menu",
    ]


class MenuOptionAdminForm(forms.ModelForm):
    class Meta:
        model = MenuOption
        fields = "__all__"
        widgets = {
            "permissions": admin.widgets.FilteredSelectMultiple("Permissions", is_stacked=False),
            "groups": admin.widgets.FilteredSelectMultiple("Permissions", is_stacked=False),
            "roles": admin.widgets.FilteredSelectMultiple("Permissions", is_stacked=False),
            "special_roles": admin.widgets.FilteredSelectMultiple("Permissions", is_stacked=False),
        }


@admin.register(MenuOption)
class MenuOptionAdmin(admin.ModelAdmin):
    form = MenuOptionAdminForm
    list_display = [
        "menu",
        "name",
        "url_name",
        "status",
    ]
    search_fields = [
        "name",
        "url_name",
    ]


class MenuGroupAdminForm(forms.ModelForm):
    class Meta:
        model = MenuGroup
        fields = "__all__"
        widgets = {
            "menus": admin.widgets.FilteredSelectMultiple("Permissions", is_stacked=False),
        }


@admin.register(MenuGroup)
class MenuGroupAdmin(admin.ModelAdmin):
    form = MenuGroupAdminForm
    list_display = [
        "name",
        "order",
        "status",
    ]
    search_fields = [
        "name",
    ]
