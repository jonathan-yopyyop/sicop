from django import template
from django.utils.html import escape

register = template.Library()


@register.filter(name="multiline_text")
def multiline_text(value, line_length=50):
    """
    Convierte un texto de una sola línea en un texto de varias líneas
    con un máximo de caracteres por línea especificado.
    """
    words = value.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) <= line_length:
            current_line += " " + word
        else:
            lines.append(escape(current_line.strip()))
            current_line = word

    if current_line:
        lines.append(escape(current_line.strip()))

    return "<br>".join(lines)


@register.filter(name="format_to_cop")
def format_to_cop(value):
    # check if value is string and format to float
    if isinstance(value, str):
        value = float(value)
    formatted_value = f"${value:,.0f} COP"
    return formatted_value
