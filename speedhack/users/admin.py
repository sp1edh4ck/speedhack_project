from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.forms import CustomUserChangeForm
from users.models import CustomUser, IpUser


class CustomUserAdmin(UserAdmin):
    readonly_fields = ["avatar_tag"]
    fieldsets = (
        (None, {'fields': ('username', 'password', 'email',)}),
        ('About user',
            {'fields': (
                'likes',
                'balance',
                'subscriber',
                'tg_link',
                'rank',
                'privilege',
                'market_privilege',
                'buy_privilege',
                'time_buy_privilege',
                'time_buy_profile_sub',
                'time_buy_market_privilege',
                'profile_sub',
                'username_style',
                'banner',
                'gender',
                'birthday',
                'occupation',
                'interests',
                'description',
                'scam',
            )}),
        (
            'Permissions',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                ),
            },
        ),
        ('Important dates', {'fields': ('last_login', 'date_joined',)}),
        ('Additional fields', {'fields': ('avatar', 'profile_background',)})
    )

    list_display = (
        'username',
        'email',
        'is_staff',
        'likes',
        'subscriber',
        'tg_link',
        'rank',
    )

    list_filter = (
        'rank',
        'is_staff',
        'is_superuser',
        'is_active',
    )

    form = CustomUserChangeForm

    def avatar_tag(self, obj):
        return obj.avatar_tag()


class IpUsersAdmin(UserAdmin):
    ordering = ('user',)
    fieldsets = (
        ('Ip address',
            {'fields': (
                'user',
                'ip_address',
                'banned',
            )}
        ),
    )

    list_display = (
        'user',
    )

    list_filter = (
        'user',
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(IpUser)
