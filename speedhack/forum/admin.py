from django.contrib import admin

from .models import (Ads, Comment, Forum, Group, Helpers, HelpForum, Like,
                     ProfileComment, Symp, Viewers)


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


class HelpersAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'group',
        'helper',
    )
    list_editable = ('group',)
    search_fields = ('group',)
    list_filter = ('group',)
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


class AdsAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'post_id',
        'weeks',
    )
    list_filter = ('weeks',)
    empty_value_display = '-пусто-'


class SympAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'post',
        'user',
        'owner',
        'created',
    )
    list_filter = ('post',)
    empty_value_display = '-пусто-'


class LikeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'post',
        'user',
        'owner',
        'created',
    )
    list_filter = ('post',)
    empty_value_display = '-пусто-'


# class FavouriteAdmin(admin.ModelAdmin):
#     list_display = (
#         'post',
#         'user',
#     )


class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'slug',
        'title',
    )
    search_fields = ('slug',)
    ordering = ('id',)
    empty_value_display = '-пусто-'


admin.site.register(Forum, ForumAdmin)
admin.site.register(Helpers, HelpersAdmin)
admin.site.register(HelpForum, HelpForumAdmin)
admin.site.register(Ads, AdsAdmin)
admin.site.register(Symp, SympAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Group, GroupAdmin)
# admin.site.register(Favourites, FavouriteAdmin)
admin.site.register(Comment)
admin.site.register(ProfileComment)
admin.site.register(Viewers)
