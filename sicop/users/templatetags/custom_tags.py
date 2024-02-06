import datetime
import re

from django import template
from django.utils.translation import gettext as _

register = template.Library()


@register.simple_tag
def get_app_name():
    return _("SICOP")


@register.simple_tag
def get_large_app_name():
    return _("SICOP")


@register.simple_tag
def get_app_version():
    return _("V1.13.0")


@register.simple_tag
def get_current_year():
    today = datetime.date.today()
    year = today.year
    return f"{year}"


@register.simple_tag
def check_url(request_path, pattern):
    return bool(re.search(pattern, request_path))
