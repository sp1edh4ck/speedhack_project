from django.contrib import admin

from .models import ProfileComment, Comment, Forum, Group, Viewers, HelpForum


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


class HelpForumAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'category',
        'priority',
        'priority_lvl',
        'request',
        'created',
        'author',
    )
    list_filter = ('priority_lvl',)
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
admin.site.register(HelpForum, HelpForumAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Comment)
admin.site.register(ProfileComment)
admin.site.register(Viewers)
