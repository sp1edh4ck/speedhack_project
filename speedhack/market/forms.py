from django import forms

from .models import Market


class AccForm(forms.ModelForm):
    class Meta:
        model = Market
        fields = ('group', 'title', 'login', 'password', 'email', 'email_password', 'price', 'description',)
