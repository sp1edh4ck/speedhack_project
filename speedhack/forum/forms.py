from django import forms

from .models import Comment, Forum


class PostForm(forms.ModelForm):
		class Meta:
				model = Forum
				fields = ('title', 'text', 'image',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', 'image',)
