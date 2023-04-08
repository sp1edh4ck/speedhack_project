from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.forms import CustomUserChangeForm
from users.models import CustomUser


class CustomUserAdmin(UserAdmin):
	readonly_fields = ["avatar_tag"]
	fieldsets = (
		(None, {'fields': ('username', 'password', 'email',)}),
		('About user', {'fields': ('likes', 'subscriber', 'tg_link', 'rank', 'privilege', 'profile_sub', 'username_style', 'gender', 'birthday', 'occupation', 'interests', 'description',)}),
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

admin.site.register(CustomUser, CustomUserAdmin)
