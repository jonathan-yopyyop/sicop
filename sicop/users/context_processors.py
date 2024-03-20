from django.conf import settings
from sicop.maloka_menu.utils.maloka_menu import get_menu_and_menu_options


def allauth_settings(request):
    """Expose some settings from django-allauth in templates."""
    return {
        "ACCOUNT_ALLOW_REGISTRATION": settings.ACCOUNT_ALLOW_REGISTRATION,
    }


def menu_processor(request):
    if request.user.is_authenticated:
        user_menus = get_menu_and_menu_options(request.user)
    else:
        user_menus = None

    return {"user_menus": user_menus}
