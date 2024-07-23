from random import randint

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.shortcuts import redirect
from users.widgets import AvatarWidget

from .models import CustomUser

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        min_length=4,
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'field-input',})
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'field-input',})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'field-input',})
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1',)

    def save(self):
        user = super().save(commit=False)
        user.is_active = False
        # token = default_token_generator.make_token(user)
        # uid = urlsafe_base64_encode(force_bytes(user.pk))
        # activation_url = reverse_lazy('confirm_email', kwargs={'uidb64': uid, 'token': token})
        # current_site = Forum.objects.get_current().domain
        # user.activation_code = f'http://{current_site}{activation_url}'
        user.activation_code = randint(100000, 999999)
        user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        del self.fields['password2']
        self.fields['password1'].help_text = None
        self.fields['username'].help_text = None


class CustomUserLogin(forms.Form):
    username = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'field-input',})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'field-input',})
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'password',)

    def confirm_login_allowed(self, user):
        if not user.is_active:
            return redirect('users:activation')


class CustomUserChangePassForm(forms.Form):
    username = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'field-input',})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'field-input',})
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'field-input',})
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'new_password',)


class CustomUserChangeForm(UserChangeForm):
    description = forms.CharField(required=False)
    occupation = forms.CharField(required=False)
    interests = forms.CharField(required=False)

    class Meta:
        widgets = {
            "avatar": AvatarWidget,
        }


class UserPersonalForm(forms.ModelForm):
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
        fields = (
            'description',
            'avatar',
            'profile_background',
            'username_style',
            'banner',
            'gender',
            'brt_day',
            'brt_month',
            'brt_year',
            'occupation',
            'interests',
        )
        widgets = {
            "avatar": AvatarWidget,
        }


class UserContactForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            'tg_link',
            'vk_link',
            'discord_link',
            'steam_link',
            'github_link',
        )


class UserProfileAdminForm(forms.ModelForm):
    username = forms.CharField(required=False)
    rank = forms.CharField(required=False)
    rank_lvl = forms.CharField(required=False)
    privilege = forms.CharField(required=False)
    market_privilege = forms.CharField(required=False)
    time_buy_market_privilege = forms.CharField(required=False)
    buy_privilege = forms.CharField(required=False)
    time_buy_privilege = forms.CharField(required=False)
    profile_sub = forms.CharField(required=False)
    time_buy_profile_sub = forms.CharField(required=False)
    tg_link = forms.CharField(required=False)
    vk_link = forms.CharField(required=False)
    discord_link = forms.CharField(required=False)
    steam_link = forms.CharField(required=False)
    github_link = forms.CharField(required=False)
    scam = forms.CharField(required=False)
    username_style = forms.CharField(required=False)
    gender = forms.CharField(required=False)
    brt_day = forms.CharField(required=False)
    brt_month = forms.CharField(required=False)
    brt_year = forms.CharField(required=False, min_length=4, max_length=4)
    description = forms.CharField(required=False)
    occupation = forms.CharField(required=False)
    interests = forms.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'rank',
            'rank_lvl',
            'privilege',
            'buy_privilege',
            'time_buy_privilege',
            'market_privilege',
            'time_buy_market_privilege',
            'tg_link',
            'vk_link',
            'discord_link',
            'steam_link',
            'github_link',
            'description',
            'occupation',
            'interests',
            'gender',
            'brt_day',
            'brt_month',
            'brt_year',
            'username_style',
            'scam',
        )
