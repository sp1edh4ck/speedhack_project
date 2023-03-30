from django import forms

from .models import ProfileComment, Comment, Forum


class PostForm(forms.ModelForm):
	class Meta:
		model = Forum
		fields = ('group', 'title', 'text', 'image',)


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('text', 'image',)


class ProfileCommentForm(forms.ModelForm):
	class Meta:
		model = ProfileComment
		fields = ('text', 'profile', 'image',)
