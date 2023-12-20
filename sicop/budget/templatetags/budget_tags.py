from django import template

register = template.Library()


@register.simple_tag
def sum_2_values(value_1, value):
    return value_1 + value


@register.simple_tag
def rest_2_values(value_1, value):
    rest = float(value_1) - float(value)
    if rest < 0:
        return 0
    else:
        return float(value_1) - float(value)
