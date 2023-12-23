from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm
from users.widgets import AvatarWidget
from random import randint
from .models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()


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

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False
        user.activation_code = randint(100000, 999999)
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        del self.fields['password2']
        self.fields['password1'].help_text = None
        self.fields['username'].help_text = None

# class CustomUserCreationForm(UserCreationForm):
#     username = forms.CharField(max_length=15, widget=forms.TextInput(attrs={
#         'class': 'field-input',
#     }))
#     email = forms.EmailField(widget=forms.TextInput(attrs={
#         'class': 'field-input',
#     }))
#     password1 = forms.CharField(widget=forms.PasswordInput(attrs={
#         'class': 'field-input',
#     }))

#     class Meta:
#         model = CustomUser
#         fields = ('username', 'email', 'password1',)

#     def __init__(self, *args, **kwargs):
#         super(CustomUserCreationForm, self).__init__(*args, **kwargs)
#         del self.fields['password2']
#         self.fields['password1'].help_text = None
#         self.fields['username'].help_text = None


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
    username_style = forms.CharField(required=False)
    banner = forms.CharField(required=False)
    description = forms.CharField(required=False)
    brt_day = forms.CharField(required=False)
    brt_month = forms.CharField(required=False)
    brt_year = forms.CharField(required=False, min_length=4, max_length=4)
    occupation = forms.CharField(required=False)
    interests = forms.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = ('description', 'tg_link', 'avatar', 'profile_background', 'username_style', 'banner', 'gender', 'brt_day', 'brt_month', 'brt_year', 'occupation', 'interests',)
        widgets = {
            "avatar": AvatarWidget,
        }
