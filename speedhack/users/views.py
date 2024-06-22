from random import randint

from django.contrib.auth import authenticate, login, get_user_model
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.views import View
from django_ratelimit.decorators import ratelimit

from .forms import CustomUserCreationForm, CustomUserLogin, CustomUserChangePassForm
from users.models import CustomUser

User = get_user_model()


class SignUpView(View):
    def get(self, request):
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


def login_user(request):
    if request.method == 'POST':
        form = CustomUserLogin(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user and user.is_active:
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
        form = CustomUserLogin()
    context = {
        'form': form,
    }
    return render(request, 'users/login.html', context)


class ChangePasswordView(View):
    def get(self, request):
        form = CustomUserChangePassForm()
        return render(request, 'users/password_change.html', {'form': form})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        new_password = request.POST['new_password']
        user = User.objects.filter(username=username).first()
        if user and user.is_active and password != new_password:
            user.password = new_password
            return redirect('users:password_change_done')
        else:
            return redirect('users:login')


# from django.urls import reverse_lazy
# from django.views.generic import CreateView
# from django.shortcuts import redirect
# from django.contrib.auth.decorators import login_required

# from .forms import CustomUserCreationForm


# class SignUp(CreateView):
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy('users:login')
#     template_name = 'users/signup.html'


# @login_required
# def logout(request):
#     return redirect('forum:index')
