from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm


class SignUp(CreateView):
	form_class = CustomUserCreationForm
	success_url = reverse_lazy('users:login')
	template_name = 'users/signup.html'


@login_required
def logout(request):
	return redirect('forum:index')
