from django.contrib import admin

from .models import AccGroup, Market


class MarketAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'group',
        'title',
        'price',
        'description',
        'pub_date',
        'author',
        'buyer',
    )
    list_editable = ('group',)
    search_fields = ('group',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class AccGroupAdmin(admin.ModelAdmin):
    list_display = (
        'slug',
        'title',
    )
    search_fields = ('slug',)
    list_filter = ('slug',)
    empty_value_display = '-пусто-'


admin.site.register(Market, MarketAdmin)
admin.site.register(AccGroup, AccGroupAdmin)
