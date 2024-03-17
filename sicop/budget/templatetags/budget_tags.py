import re

from django import template

register = template.Library()

RE_URL = {
    "commitment_certificate": r"/budget/commitment/\d+/certificate/",
    "commitment_release_certificate": r"/budget/commitment/release/certificate/\d+/",
}


@register.simple_tag
def sum_2_values(value_1, value):
    return float(value_1) + float(value)


@register.simple_tag
def rest_2_values(value_1, value):
    value_1 = float(value_1)
    value = float(value)
    if value_1 < 0:
        value_1 = value_1 * -1
    if value < 0:
        value = value * -1
    rest = value_1 - value
    if rest < 0:
        return 0
    else:
        return rest


@register.simple_tag
def check_url(request_path, pattern_key):
    url = request_path[3:]
    pattern = RE_URL.get(pattern_key)
    return bool(re.search(pattern, url))
