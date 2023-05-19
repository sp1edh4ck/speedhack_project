from django.contrib import admin

from .models import ProfileComment, Comment, Forum, Group, Viewers


class ForumAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'group',
        'text',
        'pub_date',
        'author',
    )
    list_editable = ('group',)
    search_fields = ('group',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'slug',
        'title',
    )
    search_fields = ('slug',)
    list_filter = ('slug',)
    empty_value_display = '-пусто-'


admin.site.register(Forum, ForumAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Comment)
admin.site.register(ProfileComment)
admin.site.register(Viewers)
