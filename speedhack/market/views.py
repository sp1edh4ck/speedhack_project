import requests
from bs4 import BeautifulSoup as BS
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from users.models import CustomUser

from .forms import AccForm
from .models import AccGroup, Market


def banned_redirect(request):
    return redirect('forum:banned')


def banned(request):
    return render(request, 'users/banned.html')


def close_redirect(request):
    return redirect('market:close')


def close(request):
    return render(request, 'users/close.html')


def acc_parser():
    r = requests.get(f"https://steamcommunity.com/id/sp1edh4ck")
    html = BS(r.content, 'html.parser')
    acc_info = {
        "name": "",
        "steam_lvl": 0,
        "last_online": "",
        "two_week_hours": 0,
        "count_friend": 0,
    }
    acc_info["name"] = html.find("span", class_="actual_persona_name").text
    acc_info["steam_lvl"] = html.find("span", class_="friendPlayerLevelNum").text
    acc_info["last_online"] = html.find("div", class_="profile_in_game_header").text
    acc_info["count_friend"] = html.find_all("span", class_="profile_count_link_total")[6].text
    return acc_info


def market(request):
    if request.user.is_authenticated and request.user.rank == "заблокирован":
        return banned_redirect(request)
    accs = Market.objects.all()
    context = {
        'accs': accs,
    }
    return render(request, 'market/index.html', context)


def group_free(request, slug):
    if request.user.is_authenticated and request.user.rank == "заблокирован":
        return banned_redirect(request)
    group = get_object_or_404(AccGroup, slug=slug)
    accs = group.acc.all()
    context = {
        'accs': accs,
        'group': group,
    }
    return render(request, 'market/template_groups.html', context)


@login_required
def my_accs(request):
    if request.user.rank == "заблокирован":
        return banned_redirect(request)
    user = CustomUser.objects.get(username=request.user.username)
    accs = Market.objects.filter(author=user).all()
    context = {
        'accs': accs,
    }
    return render(request, 'market/index.html', context)


@login_required
def my_buy_accs(request):
    if request.user.rank == "заблокирован":
        return banned_redirect(request)
    user = CustomUser.objects.get(username=request.user)
    accs = Market.objects.filter(buyer=user)
    context = {
        'accs': accs,
    }
    return render(request, 'market/index.html', context)


@login_required
def acc_sell(request):
    if request.user.rank == "заблокирован":
        return banned_redirect(request)
    if request.user.rank == "пользователь":
        return close(request)
    form = AccForm(
        request.POST or None,
    )
    if request.method == 'POST':
        if form.is_valid() and request.user.is_authenticated:
            new_acc = form.save(commit=False)
            new_acc.author = request.user
            new_acc.save()
            return redirect('market:index')
    context = {
        'form': form
    }
    return render(request, 'market/acc_sell.html', context)


def acc_detail(request, acc_id):
    if request.user.is_authenticated and request.user.rank == "заблокирован":
        return banned_redirect(request)
    acc = get_object_or_404(Market, id=acc_id)
    acc.view += 1
    acc.save()
    # acc_info = acc_parser()
    context = {
        # 'acc_info': acc_info,
        'acc': acc,
    }
    return render(request, 'market/acc_detail.html', context)


@login_required
def acc_buy(request, acc_id):
    if request.user.rank == "заблокирован":
        return banned_redirect(request)
    acc = get_object_or_404(Market, id=acc_id)
    user = CustomUser.objects.get(username=request.user.username)
    if acc.buyer == None and acc.author != user and user.balance >= acc.price:
        acc.buyer = user
        user.balance -= acc.price
        user.save()
        acc.save()
    return redirect('market:acc_detail', acc_id=acc_id)


def rules(request):
    return render(request, 'market/rules.html')
