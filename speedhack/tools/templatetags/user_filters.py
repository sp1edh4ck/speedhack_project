from django import template
import locale

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css, 'rows': css})


@register.filter
def addplaceholder(field, placeholder):
    return field.as_widget(attrs={'placeholder': placeholder})


@register.filter
def ru_plural(value, variants):
    variants = variants.split(",")
    value = abs(int(value))

    if value % 10 == 1 and value % 100 != 11:
        variant = 0
    elif value % 10 >= 2 and value % 10 <= 4 and (value % 100 < 10 or value % 100 >= 20):
        variant = 1
    else:
        variant = 2

    return variants[variant]


@register.filter
def bf_number(value):
    result = f'{value:,.0f}'.replace(',', ' ')
    return result
