from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm
from users.widgets import AvatarWidget, BirthdayWidget

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(max_length=15, widget=forms.TextInput(attrs={
        'class': 'field-input',
    }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': 'field-input',
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'field-input',
    }))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1',)

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        del self.fields['password2']
        self.fields['password1'].help_text = None
        self.fields['username'].help_text = None


class CustomUserLogin(AuthenticationForm):
    username = forms.CharField(max_length=15, widget=forms.TextInput(attrs={
        'class': 'field-input',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'field-input',
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
    brt_day = forms.CharField(required=False)
    brt_month = forms.CharField(required=False)
    brt_year = forms.CharField(required=False)
    occupation = forms.CharField(required=False)
    interests = forms.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = ('description', 'tg_link', 'avatar', 'profile_background', 'username_style', 'banner', 'gender', 'brt_day', 'brt_month', 'brt_year', 'occupation', 'interests',)
        widgets = {
            "avatar": AvatarWidget,
        }
