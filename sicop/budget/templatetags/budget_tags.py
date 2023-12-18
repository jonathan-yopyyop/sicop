from django import template

register = template.Library()


@register.simple_tag
def sum_2_values(value_1, value):
    return value_1 + value


@register.simple_tag
def rest_2_values(value_1, value):
    return float(value_1) - float(value)
