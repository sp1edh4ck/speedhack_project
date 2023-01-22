from django import forms

from .models import Forum, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ('title', 'text', 'image',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', 'image',)
