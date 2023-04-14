from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeDoneView,
                                       PasswordChangeView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.urls import path, reverse_lazy
from .forms import CustomUserLogin

from users.views import SignUp

app_name = 'users'

urlpatterns = [
    path(
        'signup/',
        SignUp.as_view(),
        name='signup'
    ),
    path(
        'logout/',
        LogoutView.as_view(next_page='forum:index'),
        name='logout'
    ),
    path(
        'login/',
        LoginView.as_view(template_name='users/login.html',
                          authentication_form=CustomUserLogin),
        name='login'
    ),
    # path(
    #     'password_change/',
    #     PasswordChangeView.as_view(
    #         template_name='users/password_change_form.html',
    #         success_url=reverse_lazy('users:password_change')),
    #     name='password_change'
    # ),
    # path(
    #     'password_change/done/',
    #     PasswordChangeDoneView.as_view(
    #         template_name='users/password_change_done.html'),
    #     name='password_change_done'
    # ),
    # path(
    #     'password_reset/',
    #     PasswordResetView.as_view(
    #         template_name='users/password_reset_form.html'),
    #     name='password_reset'
    # ),
    # path(
    #     'password_reset/done/',
    #     PasswordResetDoneView.as_view(
    #         template_name='users/password_reset_done.html'),
    #     name='password_reset_done'
    # ),
    # path(
    #     'reset/<uidb64>/<token>/',
    #     PasswordResetConfirmView.as_view(
    #         template_name='users/password_reset_confirm.html'),
    #     name='password_reset_confirm'
    # ),
    # path(
    #     'reset/done/',
    #     PasswordResetCompleteView.as_view(
    #         template_name='password_reset_complete.html'),
    #     name='password_reset_complete'
    # ),
]
