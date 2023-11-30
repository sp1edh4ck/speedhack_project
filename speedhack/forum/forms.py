from django import forms

from .models import ProfileComment, Comment, Forum, HelpForum, HelpAnswer, Ads
from users.models import CustomUser


class PostForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ('group', 'title', 'text', 'image',)


class HelpForm(forms.ModelForm):
    category = forms.CharField(required=True)
    priority = forms.CharField(required=True)
    title = forms.CharField(required=True)
    request = forms.CharField(required=True)
    description = forms.CharField(required=True)

    class Meta:
        model = HelpForum
        fields = ('category', 'priority', 'title', 'request', 'description',)


class AnswerForm(forms.ModelForm):
    class Meta:
        model = HelpAnswer
        fields = ('text',)


class AdsForm(forms.ModelForm):
    class Meta:
        model = Ads
        fields = ('title', 'description', 'weeks', 'author',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', 'image',)


class ProfileCommentForm(forms.ModelForm):
    class Meta:
        model = ProfileComment
        fields = ('text', 'profile', 'image',)


class DepositForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('save_deposit',)
