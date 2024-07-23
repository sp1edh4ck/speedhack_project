from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeDoneView,
                                       PasswordChangeView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.urls import path
from users.views import ActivationView, ChangePasswordView, SignUpView

from . import views
from .forms import CustomUserLogin

app_name = 'users'

urlpatterns = [
    path('activation', ActivationView.as_view(), name='activation'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(next_page='forum:index'), name='logout'),
    # * старый логин
    # ? ----------
    # path(
    #     'login/',
    #     LoginView.as_view(template_name='users/login.html',
    #                       authentication_form=CustomUserLogin),
    #     name='login'
    # ),
    # ? ----------
    path('login/', views.login_user, name='login'),
    path('password_change/', ChangePasswordView.as_view(), name='password_change'),
    path(
        'password_change/done/',
        PasswordChangeDoneView.as_view(
            template_name='users/password_change_done.html'
        ),
        name='password_change_done'
    ),
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
