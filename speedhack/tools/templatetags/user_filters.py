from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css, 'rows': css})


@register.filter
def addplaceholder(field, placeholder):
    return field.as_widget(attrs={'placeholder': placeholder})
