from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeDoneView,
                                       PasswordChangeView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.urls import path

from users.views import (ActivationView, ChangeLoginPasswordView,
                         ChangePasswordView, CustomLoginView, SignUpView)

from . import views
from .forms import CustomUserLogin

app_name = 'users'

urlpatterns = [
    path('activation', ActivationView.as_view(), name='activation'),
    path('empty_user', ActivationView.as_view(), name='empty_user'),
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
    path('login/', CustomLoginView.as_view(), name='login'),
    path('password_change/', ChangePasswordView.as_view(), name='password_change'),
    path('safety/', ChangeLoginPasswordView.as_view(), name='profile_safety'),
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
