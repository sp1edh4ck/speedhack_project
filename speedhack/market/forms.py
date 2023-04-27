from django import forms

from .models import Market


class AccForm(forms.ModelForm):
    class Meta:
        model = Market
        fields = ('group', 'title', 'data', 'price', 'description',)
