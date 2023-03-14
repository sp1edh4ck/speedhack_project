from django.contrib import admin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email',
                    'username',
                    'likes',
                    'subscriber',
                    'tg_link',
                    'avatar',
                    'rank',
                    'language',)

admin.site.register(CustomUser, CustomUserAdmin)
