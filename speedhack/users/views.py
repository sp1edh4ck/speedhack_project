from django.contrib.auth import get_user_model, login
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from django.views import View
from django_ratelimit.decorators import ratelimit

from .forms import CustomUserCreationForm

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
