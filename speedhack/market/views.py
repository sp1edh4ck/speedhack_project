from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Market, AccGroup
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


def group_free(request, slug):
    group = get_object_or_404(AccGroup, slug=slug)
    accs = group.acc.all()
    count_accs = accs.count()
    context = {
        'accs': accs,
        'group': group,
        'count_accs': count_accs,
    }
    return render(request, 'market/template_groups.html', context)


@login_required
def my_accs(request):
    user = request.user
    search_query = request.GET.get('search', '')
    if search_query:
        accs = user.acc.filter(title__icontains=search_query)
    else:
        accs = user.acc.all()
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


def rules(request):
    return render(request, 'market/rules.html')
