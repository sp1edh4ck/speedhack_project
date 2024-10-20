import locale

from django import template

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
    if value != '':
        value = abs(int(value))
        if value % 10 == 1 and value % 100 != 11:
            variant = 0
        elif value % 10 >= 2 and value % 10 <= 4 and (value % 100 < 10 or value % 100 >= 20):
            variant = 1
        else:
            variant = 2
        return variants[variant]
    return variants[2]


@register.filter
def bf_number(value):
    result = f'{value:,.0f}'.replace(',', ' ')
    return result


@register.filter
def mail_forced(value):
    name, end = value.split('@',)
    lens = len(name) - 1
    letter_start = name[:1]
    letter_end = name[lens:]
    result = str(letter_start) + str('*' * (lens - 1)) + str(letter_end) + '@' + str(end)
    return result


@register.filter
def permission_access(user, type):
    if type == 'default':
        return (user.rank_lvl == 'default' or
                user.rank_lvl == 'designer_view' or
                user.rank_lvl == 'moder_view' or
                user.rank_lvl == 'admin_view' or
                user.rank_lvl == 'owner_view')
    elif type == 'designer':
        return (user.rank_lvl == 'designer_view' or
                user.rank_lvl == 'moder_view' or
                user.rank_lvl == 'admin_view' or
                user.rank_lvl == 'owner_view')
    elif type == 'moder':
        return (user.rank_lvl == 'moder_view' or
                user.rank_lvl == 'admin_view' or
                user.rank_lvl == 'owner_view')
    elif type == 'admin':
        return (user.rank_lvl == 'admin_view' or
                user.rank_lvl == 'owner_view')


@register.filter
def privilege_access(user, type):
    if type == 'default':
        return (user.privilege == 'искусственный интелект' or
                user.buy_privilege == 'уник')
    