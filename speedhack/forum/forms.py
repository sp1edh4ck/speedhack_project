from django import forms

from users.models import CustomUser

from .models import Ads, Comment, Forum, HelpAnswer, HelpForum, ProfileComment


class PostForm(forms.ModelForm):
    # closed = forms.BooleanField(required=False)
    # edit = forms.BooleanField(required=False)
    # open_activities = forms.BooleanField(required=False)

    class Meta:
        model = Forum
        fields = ('group', 'title', 'text', 'image', 'closed', 'edit', 'open_activities',)


# Система личных сообщений
# class MessageForm(forms.ModelForm):
#     class Meta:
#         model = Message
#         fields = ['message']
#         labels = {'message': ""}


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
        fields = ('title', 'post_id', 'weeks', 'author',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', 'image',)


class ProfileCommentForm(forms.ModelForm):
    class Meta:
        model = ProfileComment
        fields = ('text',)


class DepositForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('save_deposit',)
