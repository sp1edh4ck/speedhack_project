from random import randint

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, update_session_auth_hash
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django_ratelimit.decorators import ratelimit
import re
from users.models import CustomUser

from .forms import (CustomUserChangePassForm, CustomUserCreationForm,
                    CustomUserLogin)

User = get_user_model()


class SignUpView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('forum:index')
        else:
            form = CustomUserCreationForm()
            return render(request, 'users/signup.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_mail(
                'Подтверждение почты',
                f'Ваш код активации: {user.activation_code}',
                'speedhack_sup@mail.ru',
                [user.email],
            )
            return redirect('users:activation')
        return render(request, 'users/signup.html', {'form': form})


class ActivationView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('forum:index')
        else:
            return render(request, 'users/activation.html')

    def post(self, request):
        activation_code = request.POST['activation_code']
        user = User.objects.filter(activation_code=activation_code).first()
        if user:
            user.is_active = True
            user.activation_code = ''
            user.save()
            return redirect('users:login')
        else:
            return redirect('users:activation')


class CustomLoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('forum:index')
        else:
            form = CustomUserLogin()
            return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        form = CustomUserLogin(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect('forum:index')
                else:
                    u = CustomUser.objects.get(username=form.cleaned_data['username'])
                    u.activation_code = randint(100000, 999999)
                    u.save()
                    send_mail(
                        'Подтверждение почты',
                        f'Ваш код активации: {u.activation_code}',
                        'speedhack_sup@mail.ru',
                        [u.email],
                    )
                    return redirect('users:activation')
            else:
                messages.error(request, "Неверное имя пользователя или пароль")
        return render(request, 'users/login.html', {'form': form})


class ChangePasswordView(View):
    def get(self, request):
        form = CustomUserChangePassForm()
        return render(request, 'users/password_change.html', {'form': form})

    def post(self, request):
        form = CustomUserChangePassForm()
        username = request.POST['username']
        password = request.POST['password']
        new_password = request.POST['new_password']
        user = User.objects.filter(username=username).first()
        if user:
            if user.is_active:
                if user.check_password(password):
                    if password == new_password:
                        messages.error(request, "Новый пароль должен отличаться от старого")
                    elif not self.is_valid_password(new_password):
                        messages.error(request, "Пароль должен содержать минимум 8 символов, включая 1 заглавную букву, 1 строчную букву и 1 цифру")
                    else:
                        user.set_password(new_password)
                        user.save()
                        user = authenticate(request, username=username, password=new_password)
                        login(request, user)
                        return redirect('forum:index')
                else:
                    messages.error(request, "Старый пароль неверный")
            else:
                messages.error(request, "Аккаунт отключён или не был подтверждён письмом на почту")
        else:
            messages.error(request, "Пользователь не найден")
        return render(request, 'users/password_change.html', {'form': form})

    def is_valid_password(self, password):
        regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d!@#$%^&*()_+={}:;,.?-]{8,}$'
        return re.match(regex, password) is not None