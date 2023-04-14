from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm
from users.widgets import AvatarWidget, BirthdayWidget

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(max_length=15, widget=forms.TextInput(attrs={
        'class': 'field-input',
        'placeholder': 'Логин',
    }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': 'field-input',
        'placeholder': 'Почта',
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'field-input',
        'placeholder': 'Пароль',
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'field-input',
        'placeholder': 'Повтор пароля',
    }))

    class Meta:
        model = CustomUser
        fields = ('username', 'email',)


class CustomUserLogin(AuthenticationForm):
    username = forms.CharField(max_length=15, widget=forms.TextInput(attrs={
        'class': 'field-input',
        'placeholder': 'Логин',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'field-input',
        'placeholder': 'Пароль',
    }))


class CustomUserChangeForm(UserChangeForm):
    description = forms.CharField(required=False)
    occupation = forms.CharField(required=False)
    interests = forms.CharField(required=False)

    class Meta:
        widgets = {
            "avatar": AvatarWidget,
        }


class UserProfileForm(forms.ModelForm):
    description = forms.CharField(required=False)
    birthday = forms.DateField(label='Дата рождения', required=False)
    occupation = forms.CharField(required=False)
    interests = forms.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = ('description', 'tg_link', 'avatar', 'profile_background', 'username_style', 'banner', 'gender', 'birthday', 'occupation', 'interests',)
        widgets = {
            "avatar": AvatarWidget,
            "birthday": BirthdayWidget,
        }


class UserPrivilegeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('privilege',)
        widgets = {
            "avatar": AvatarWidget,
            "birthday": BirthdayWidget,
        }
