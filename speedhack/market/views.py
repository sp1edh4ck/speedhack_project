from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Market, AccGroup
from .forms import AccForm
from users.models import CustomUser


import requests
from bs4 import BeautifulSoup as BS


def banned_redirect(request):
    return redirect('forum:banned')


def banned(request):
    return render(request, 'users/banned.html')


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
    count_accs = accs.count()
    context = {
        'accs': accs,
        'count_accs': count_accs,
    }
    return render(request, 'market/index.html', context)


def group_free(request, slug):
    if request.user.is_authenticated and request.user.rank == "заблокирован":
        return banned_redirect(request)
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
    if request.user.rank == "заблокирован":
        return banned_redirect(request)
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
    if request.user.rank == "заблокирован":
        return banned_redirect(request)
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
    if request.user.is_authenticated and request.user.rank == "заблокирован":
        return banned_redirect(request)
    acc = get_object_or_404(Market, id=acc_id)
    acc_info = acc_parser()
    context = {
        'acc_info': acc_info,
        'acc': acc,
    }
    return render(request, 'market/acc_detail.html', context)


@login_required
def acc_buy(request, acc_id):
    if request.user.rank == "заблокирован":
        return banned_redirect(request)
    acc = get_object_or_404(Market, id=acc_id)
    acc.buyer = request.user.username
    acc.save()
    return redirect('market:acc_detail', id=acc_id)


def rules(request):
    return render(request, 'market/rules.html')
