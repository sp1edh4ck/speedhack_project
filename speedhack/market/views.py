from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Market
from .forms import AccForm
from users.models import CustomUser


def market(request):
    accs = Market.objects.all()
    count_accs = accs.count()
    context = {
        'accs': accs,
        'count_accs': count_accs,
    }
    return render(request, 'market/index.html', context)


@login_required
def acc_sell(request):
    form = AccForm(
        request.POST or None,
    )
    if request.method == 'POST':
        if form.is_valid():
            new_acc = form.save(commit=False)
            new_acc.author = request.user
            new_acc.save()
            return redirect('market:index')
    context = {
        'form': form
    }
    return render(request, 'market/acc_sell.html', context)


def acc_detail(request, acc_id):
    acc = get_object_or_404(Market, id=acc_id)
    context = {
        'acc': acc,
    }
    return render(request, 'market/acc_detail.html', context)
