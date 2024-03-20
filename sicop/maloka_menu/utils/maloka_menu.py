from sicop.maloka_menu.models import Menu, MenuOption
from sicop.users.models import User
from sicop.area.models import AreaRole, Area, AreaMember
from django.contrib.auth.models import Permission


def get_menu_and_menu_options(user: User):
    """Get menu and menu options."""
    security_groups = user.groups.all()
    user_permissions = user.get_all_permissions()
    area_member = AreaMember.objects.filter(user=user).first()
    role: AreaRole = area_member.role
    permissions = []
    menu = {}
    for user_permission in user_permissions:
        codename = user_permission.split(".")[1]
        perm = Permission.objects.filter(codename=codename).last()
        permissions.append(perm)

    menu_options_queryset = MenuOption.objects.filter(
        permissions__in=permissions,
    )
    # print(menu_options_queryset)
    for menu_option in menu_options_queryset:
        menu_group_object = menu_option.menu.group
        menu_object = menu_option.menu
        if menu_group_object.name not in menu:
            menu[menu_group_object.name] = {
                "menus": {},
            }
        if menu_object.menu not in menu[menu_group_object.name]["menus"]:
            menu[menu_group_object.name]["menus"][menu_object.menu] = {
                "icon": menu_object.icon,
                "options": {},
            }

        if menu_option.name not in menu[menu_group_object.name]["menus"][menu_object.menu]["options"]:
            menu[menu_group_object.name]["menus"][menu_object.menu]["options"][menu_option.name] = {
                "url_name": menu_option.url_name,
                "url_complement": menu_option.url_complement,
            }

    return menu
