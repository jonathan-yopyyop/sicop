from django import template

register = template.Library()


@register.simple_tag
def rest_values(first_value, second_value):
    # convert first and second value to Float
    first_value = float(first_value)
    second_value = float(second_value)
    return first_value - second_value
