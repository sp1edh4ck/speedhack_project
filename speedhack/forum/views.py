from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django_ratelimit.decorators import ratelimit

from market.models import Market
from users.forms import UserProfileForm
from users.models import CustomUser, IpUser

from .forms import (AdsForm, AnswerForm, CommentForm, DepositForm, HelpForm,
                    PostForm, ProfileCommentForm)
from .models import (Ads, Comment, Favourites, Follow, Forum, Group, Helpers,
                     HelpForum, Like, ProfileComment, Symp, User, Viewers)


def pagination_post(request, post_list):
    paginator = Paginator(post_list, 12)
    return paginator.get_page(request.GET.get('page'))


def pagination_sub(request, sub_list):
    paginator = Paginator(sub_list, 5)
    return paginator.get_page(request.GET.get('page'))


def pagination_comments(request, comment_list):
    paginator = Paginator(comment_list, 5)
    return paginator.get_page(request.GET.get('page'))


def banned_redirect(request):
    if request.user.rank == "заблокирован":
        return redirect('forum:banned')
    return redirect('forum:index')


def banned(request):
    return render(request, 'users/banned.html')


def successfully(request):
    return render(request, 'forum/successfully.html')


# Кастом страница для вывода 403 ошибки
# def ratelimited(request, exception):
#     return render(request, 'forum/limit.html')


@ratelimit(key='ip', rate='50/m')
def index(request):
    if request.user.is_authenticated and request.user.rank == "заблокирован":
        return banned_redirect(request)
    search_query = request.GET.get('search', '')
    if search_query:
        posts = Forum.objects.filter(title__icontains=search_query)
    else:
        posts = Forum.objects.select_related('author').all()
    # users = User.objects.filter(is_online=True)
    count_posts = posts.count()
    ads = Ads.objects.all()
    context = {
        'count_posts': count_posts,
        'ads': ads,
        # 'users': users,
        'objects': pagination_post(request, posts),
    }
    return render(request, 'forum/index.html', context)


@ratelimit(key='ip', rate='50/m')
@login_required
def my_topics(request):
    if request.user.rank == "заблокирован":
        return banned_redirect(request)
    user = request.user
    search_query = request.GET.get('search', '')
    if search_query:
        posts = user.posts.filter(title__icontains=search_query)
    else:
        posts = user.posts.all()
    count_posts = posts.count()
    ads = Ads.objects.all()
    context = {
        'count_posts': count_posts,
        'ads': ads,
        'objects': pagination_post(request, posts)
    }
    return render(request, 'forum/index.html', context)


@ratelimit(key='ip', rate='50/m')
@login_required
def favourites(request):
    if request.user.rank == "заблокирован":
        return banned_redirect(request)
    user = request.user
    favourites_posts = Favourites.objects.filter(user=user)
    count_posts = favourites_posts.count()
    ads = Ads.objects.all()
    context = {
        'count_posts': count_posts,
        'ads': ads,
        'objects': pagination_post(request, favourites_posts)
    }
    return render(request, 'forum/index.html', context)


@ratelimit(key='ip', rate='50/m')
def group_free(request, slug):
    if request.user.is_authenticated and request.user.rank == "заблокирован":
        return banned_redirect(request)
    group = get_object_or_404(Group, slug=slug)
    search_query = request.GET.get('search', '')
    posts = group.posts.all()
    if search_query:
        posts = group.posts.filter(title__icontains=search_query)
    else:
        posts = group.posts.all()
    helpers = Helpers.objects.filter(group=group)
    helpers_count = helpers.count()
    count_posts = posts.count()
    context = {
        'count_posts': count_posts,
        'group': group,
        'objects': pagination_post(request, posts),
        'helpers': helpers,
        'helpers_count': helpers_count,
    }
    return render(request, 'forum/template_groups.html', context)


@ratelimit(key='ip', rate='50/m')
def profile(request, username):
    if request.user.is_authenticated and request.user.rank == "заблокирован":
        return banned_redirect(request)
    author = get_object_or_404(User, username=username)
    form = ProfileCommentForm(request.POST or None)
    if form.is_valid():
        form = form.save(commit=False)
        form.profile = author
        form.author = request.user
        form.save()
        return redirect('forum:profile', username=author)
    posts = author.posts.all()
    post_1 = posts.filter(group=1)
    profile_comments = ProfileComment.objects.filter(profile=author)
    subscriptions = author.follower.all()
    subscribers = author.following.all()
    following = (
        author.following.filter(user_id=request.user.id).exists()
        if request.user.is_authenticated
        else False
    )
    count_subscriptions = subscriptions.count()
    count_subscribers = subscribers.count()
    context = {
        'form': form,
        'author': author,
        'posts': posts,
        'post_1': post_1,
        'following': following,
        'profile_comments': profile_comments,
        'count_subscriptions': count_subscriptions,
        'count_subscribers': count_subscribers,
        'objects': pagination_post(request, posts),
        'subscriptions': pagination_sub(request, subscriptions),
        'subscribers': pagination_sub(request, subscribers),
    }
    return render(request, 'forum/profile.html', context)


@login_required
def complaint(request):
    pass


@ratelimit(key='ip', rate='50/m')
@login_required
def delete_profile_comment(request, username, comment_id):
    if request.user.rank == "заблокирован":
        return banned_redirect(request)
    ProfileComment.objects.filter(pk=comment_id).delete()
    return redirect('forum:profile', username=username)


# @login_required
# def payment(request, username, number):
#     user = CustomUser.objects.get(username=username)
#     return render(request, 'forum/payments.html')


@ratelimit(key='ip', rate='50/m')
@login_required
def deposit(request, username, number):
    if request.user.rank == "заблокирован":
        return banned_redirect(request)
    user = CustomUser.objects.get(username=username)
    if number == 1:
        user.save_deposit += 10000
        user.save()
    if number == 2:
        user.balance -= 10000
        user.save_deposit += 10000
        user.save()
    # if request.method == 'POST':
    #     form = DepositForm(
    #         request.POST or None
    #     )
    #     if form.is_valid():
    #         user.save_deposit += 10000
    #         form.save()
    #         return redirect('forum:profile', username=username)
    # else:
    #     form = DepositForm()
    return redirect('forum:profile', username=username)


@login_required
def ban(request, username):
    user = get_object_or_404(User, username=username)
    if user.rank == "заблокирован":
        user.rank = user.save_rank
        user.save()
    elif user.rank != "заблокирован":
        user.save_rank = user.rank
        user.rank = "заблокирован"
        user.save()
    return redirect('forum:profile', username=username)


@login_required
def admin_ban(request, username):
    user = get_object_or_404(User, username=username)
    if user.rank == "заблокирован":
        user.rank = user.save_rank
        user.save()
    elif user.rank != "заблокирован":
        user.save_rank = user.rank
        user.rank = "заблокирован"
        user.save()
    return redirect('forum:admin_panel')


@ratelimit(key='ip', rate='50/m')
@login_required
def info_edit(request, username):
    if request.user.rank == "заблокирован":
        return banned_redirect(request)
    form = UserProfileForm(
        request.POST or None,
        files=request.FILES or None,
        instance=request.user
    )
    if form.is_valid():
        form.brt_day = request.POST.get('brt_day')
        form.brt_month = request.POST.get('brt_month')
        form.brt_year = request.POST.get('brt_year')
        form.save()
        return redirect('forum:profile', username=username)
    context = {
        'form': form,
    }
    return render(request, 'forum/info_edit.html', context)


@ratelimit(key='ip', rate='50/m')
@login_required
def upgrade_temp(request, username):
    if request.user.rank == "заблокирован":
        return banned_redirect(request)
    return render(request, 'forum/upgrade.html')


@ratelimit(key='ip', rate='50/m')
@login_required
def upgrade(request, username, number):
    if request.user.rank == "заблокирован":
        return banned_redirect(request)
    user = CustomUser.objects.get(username=username)
    if number == 1 and request.user.balance >= 100:
        user.market_privilege = "продавец"
        user.balance -= 100
        user.time_buy_market_privilege = timezone.now()
        user.save()
    if number == 2 and user.balance >= 100:
        user.profile_sub = True
        user.balance -= 100
        user.time_buy_profile_sub = timezone.now()
        user.save()
    if number == 3 and user.balance >= 2999:
        user.buy_privilege = "легенда"
        user.balance -= 2999
        user.time_buy_privilege = timezone.now()
        user.save()
    if number == 4 and user.balance >= 1499:
        user.buy_privilege = "суприм"
        user.balance -= 1499
        user.time_buy_privilege = timezone.now()
        user.save()
    if number == 5 and user.balance >= 7500:
        user.buy_privilege = "уник"
        user.balance -= 7500
        user.time_buy_privilege = timezone.now()
        user.save()
    return redirect('forum:profile', username=username)


@ratelimit(key='ip', rate='50/m')
def post_detail(request, post_id):
    if request.user.is_authenticated and request.user.rank == "заблокирован" and post.author != request.user:
        return banned_redirect(request)
    post = get_object_or_404(Forum, id=post_id)
    if request.user.is_authenticated:
        user = get_object_or_404(User, username=request.user.username)
        my_symp = Symp.objects.filter(post=post, user=user)
        favourite = Favourites.objects.filter(post=post, user=user)
    # Добавление просмотра (надо доработать)
    # if request.user.is_authenticated:
        # viewers = post.viewers.all()
        # post.view += 1
        # post.save()
    form = CommentForm(request.POST or None)
    comments = post.comments.all()
    count_comments = comments.count()
    symps = Symp.objects.filter(post=post)
    if request.user.is_authenticated:
        context = {
            'form': form,
            'favourite': favourite,
            'post': post,
            'user': user,
            'symps': symps,
            'my_symp': my_symp,
            'comments': comments,
            'count_comments': count_comments,
        }
        return render(request, 'forum/post_detail.html', context)
    context = {
        'form': form,
        'post': post,
        'symps': symps,
        'comments': comments,
        'count_comments': count_comments,
    }
    return render(request, 'forum/post_detail.html', context)


@login_required
def favourites_post_save(request, post_id, number):
    post = get_object_or_404(Forum, id=post_id)
    if number == 1:
        Favourites.objects.create(post=post, user=request.user)
    elif number == 2:
        Favourites.objects.filter(post=post, user=request.user).delete()
    return redirect('forum:post_detail', post_id=post_id)


@ratelimit(key='ip', rate='50/m')
@login_required
def post_oc(request, post_id, number):
    if request.user.rank == "заблокирован":
        return banned_redirect(request)
    post = get_object_or_404(Forum, id=post_id)
    if number == 1:
        post.closed = True
        post.save()
        return redirect('forum:post_detail', post_id=post_id)
    elif number == 2:
        post.closed = False
        post.save()
        return redirect('forum:post_detail', post_id=post_id)


@ratelimit(key='ip', rate='50/m')
@login_required
def symps_add(request, post_id, username):
    if request.user.rank == "заблокирован":
        return banned_redirect(request)
    post = get_object_or_404(Forum, id=post_id)
    owner = get_object_or_404(User, username=username)
    if owner != request.user:
        if not Symp.objects.filter(post=post, owner=owner, user=request.user).exists():
            owner.symps += 1
            owner.save()
            Symp.objects.create(post=post, owner=owner, user=request.user)
        else:
            owner.symps -= 1
            owner.save()
            Symp.objects.filter(post=post, owner=owner, user=request.user).delete()
    comments = post.comments.all()
    if post.author.username == request.user.username:
        for comment in comments:
            user = CustomUser.objects.get(username=comment.author.username)
    else:
        user = CustomUser.objects.get(username=post.author.username)
    if user.privilege != "местный" and user.symps >= 20 and user.symps <= 199:
        user.privilege = "местный"
        user.save()
    elif user.privilege != "постоялец" and user.symps >= 200 and user.symps <= 999:
        user.privilege = "постоялец"
        user.save()
    elif user.privilege != "эксперт" and user.symps >= 1000 and user.symps <= 3999:
        user.privilege = "эксперт"
        user.save()
    elif user.privilege != "гуру" and user.symps >= 4000 and user.symps <= 9999:
        user.privilege = "гуру"
        user.save()
    elif user.privilege != "искусственный интелект" and user.symps >= 10000:
        user.privilege = "искусственный интелект"
        user.save()
    if user.symps < 20:
        user.privilege = "новорег"
        user.save()
    elif user.symps < 200:
        user.privilege = "местный"
        user.save()
    elif user.symps < 1000:
        user.privilege = "постоялец"
        user.save()
    elif user.symps < 4000:
        user.privilege = "эксперт"
        user.save()
    elif user.symps < 10000:
        user.privilege = "гуру"
        user.save()
    return redirect('forum:post_detail', post_id=post_id)


@ratelimit(key='ip', rate='50/m')
@login_required
def post_create(request):
    if request.user.rank == "заблокирован":
        return banned_redirect(request)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None
    )
    if request.method == 'POST':
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect('forum:index')
    context = {
        'form': form
    }
    return render(request, 'forum/post_create.html', context)


@ratelimit(key='ip', rate='50/m')
@login_required
def post_edit(request, post_id):
    if request.user.rank == "заблокирован":
        return banned_redirect(request)
    post = get_object_or_404(Forum, pk=post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if (request.user == post.author or request.user.rank_lvl >= "4"):
        if request.method == 'POST':
            if form.is_valid():
                if request.user.rank_lvl >= "4":
                    form.save()
                    return redirect('forum:post_detail', post_id=post_id)
                else:
                    post.edit = True
                    post.save()
                    form.save()
                    return redirect('forum:post_detail', post_id=post_id)
        context = {
            'post': post,
            'form': form,
            'is_edit': True,
        }
        return render(request, 'forum/post_create.html', context)
    return redirect('forum:post_detail', post_id=post_id)


@ratelimit(key='ip', rate='50/m')
@login_required
def post_delete(request, post_id):
    if request.user.rank == "заблокирован":
        return banned_redirect(request)
    post = get_object_or_404(Forum, pk=post_id)
    if (request.user == post.author or request.user.rank_lvl >= "4"):
        Forum.objects.filter(pk=post_id).delete()
        return redirect('forum:successfully')


@ratelimit(key='ip', rate='50/m')
@login_required
def add_comment(request, post_id):
    if request.user.rank == "заблокирован":
        return banned_redirect(request)
    post = get_object_or_404(Forum, pk=post_id)
    if post.closed == False:
        form = CommentForm(request.POST or None)
        if form.is_valid():
            user = CustomUser.objects.get(username=request.user.username)
            user.messages += 1
            user.save()
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('forum:post_detail', post_id=post_id)
    return redirect('forum:post_detail', post_id=post_id)


@ratelimit(key='ip', rate='50/m')
@login_required
def edit_comment(request, post_id):
    if request.user.rank == "заблокирован":
        return banned_redirect(request)
    post = get_object_or_404(Forum, pk=post_id)
    form = CommentForm(request.POST or None)
    if request.user == post.author or request.user.rank_lvl >= "4":
        if request.method == 'POST':
            if form.is_valid():
                comment = form.save(commit=False)
                comment.edit = True
                comment.save()
                return redirect('forum:post_detail', post_id=post_id)
        context = {
            'post': post,
            'form': form,
            'is_edit': True,
        }
        return render(request, 'forum/post_detail.html', context)


@ratelimit(key='ip', rate='50/m')
@login_required
def delete_comment(request, post_id, id):
    if request.user.rank == "заблокирован":
        return banned_redirect(request)
    comment = get_object_or_404(Comment, id=id)
    comment.delete()
    return redirect('forum:post_detail', post_id=post_id)


@ratelimit(key='ip', rate='50/m')
@login_required
def profile_follow(request, username):
    if request.user.rank == "заблокирован":
        return banned_redirect(request)
    author = get_object_or_404(User, username=username)
    if author != request.user:
        if not Follow.objects.filter(author=author, user=request.user).exists():
            Follow.objects.create(author=author, user=request.user)
    return redirect('forum:profile', username=username)


@ratelimit(key='ip', rate='50/m')
@login_required
def profile_unfollow(request, username):
    if request.user.rank == "заблокирован":
        return banned_redirect(request)
    author = get_object_or_404(User, username=username)
    author.following.filter(user=request.user).delete()
    return redirect('forum:profile', username=username)


@login_required
def admin_panel(request):
    if request.user.is_authenticated and request.user.rank == "заблокирован":
        return banned_redirect(request)
    users_list = CustomUser.objects.all()
    users_ban_list = CustomUser.objects.filter(rank="заблокирован")
    count_users = users_list.count()
    count_users_ban = users_ban_list.count()
    search_query = request.GET.get('search', '')
    if search_query:
        users_list = CustomUser.objects.filter(username__icontains=search_query)
    count_search = users_list.count()
    author = Forum.objects.select_related('author').all()
    context = {
        'author': author,
        'users': users_list,
        'count_users': count_users,
        'count_search': count_search,
        'count_users_ban': count_users_ban,
    }
    return render(request, 'forum/admin.html', context)


@login_required
def user_edit(request, username):
    user = get_object_or_404(User, username=username)
    context = {
        'user': user,
    }
    return render(request, 'forum/admin_user_edit.html', context)


@login_required
def tickets(request):
    if request.user.is_authenticated and request.user.rank == "заблокирован":
        return banned_redirect(request)
    tickets_list = HelpForum.objects.all()
    tickets_open_count = HelpForum.objects.filter(open=True).count()
    tickets_close = HelpForum.objects.filter(open=False)
    tickets_close_count = tickets_close.count()
    tickets_count = tickets_list.count()
    context = {
        'tickets_list': tickets_list,
        'tickets_count': tickets_count,
        'tickets_open_count': tickets_open_count,
        'tickets_close': tickets_close,
        'tickets_close_count': tickets_close_count,
    }
    return render(request, 'forum/tickets.html', context)


@ratelimit(key='ip', rate='50/m')
@login_required
def my_tickets(request, username):
    if request.user.rank == "заблокирован":
        return banned_redirect(request)
    user = request.user
    my_tickets = user.tickets.all()
    my_tickets_count = my_tickets.count()
    context = {
        'my_tickets': my_tickets,
        'my_tickets_count': my_tickets_count,
    }
    return render(request, 'forum/my_tickets.html', context)


@ratelimit(key='ip', rate='50/m')
@login_required
def ticket(request, ticket_id):
    if request.user.rank == "заблокирован":
        return banned_redirect(request)
    form = AnswerForm(request.POST or None)
    ticket = get_object_or_404(HelpForum, pk=ticket_id)
    comments = ticket.answer.all()
    count_comments = comments.count()
    context = {
        'form': form,
        'ticket': ticket,
        'comments': comments,
        'count_comments': count_comments,
    }
    return render(request, 'forum/ticket.html', context)


@ratelimit(key='ip', rate='50/m')
@login_required
def add_answer(request, ticket_id):
    if request.user.rank == "заблокирован":
        return banned_redirect(request)
    ticket = get_object_or_404(HelpForum, pk=ticket_id)
    if ticket.open:
        form = AnswerForm(request.POST or None)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.ticket = ticket
            answer.save()
    return redirect('forum:ticket', ticket_id=ticket_id)


@login_required
def ticket_close(request, ticket_id):
    if request.user.rank == "заблокирован":
        return banned_redirect(request)
    ticket = get_object_or_404(HelpForum, id=ticket_id)
    ticket.open = False
    ticket.save()
    return redirect('forum:tickets')


@login_required
def ticket_open(request, ticket_id):
    if request.user.rank == "заблокирован":
        return banned_redirect(request)
    ticket = get_object_or_404(HelpForum, id=ticket_id)
    ticket.open = True
    ticket.save()
    return redirect('forum:tickets')


@login_required
def ticket_delete(request, ticket_id):
    if request.user.rank == "заблокирован":
        return banned_redirect(request)
    HelpForum.objects.filter(pk=ticket_id).delete()
    return redirect('forum:tickets')


@ratelimit(key='ip', rate='50/m')
@login_required
def ticket_form(request):
    if request.user.rank == "заблокирован":
        return banned_redirect(request)
    form = HelpForm(
        request.POST or None
    )
    if request.method == 'POST':
        if form.is_valid():
            ticket = form.save(commit=False)
            if ticket.priority == "Низкий":
                ticket.priority_lvl = 1
            elif ticket.priority == "Средний":
                ticket.priority_lvl = 2
            elif ticket.priority == "Высокий":
                ticket.priority_lvl = 3
            ticket.author = request.user
            ticket.save()
            return redirect('forum:index')
    context = {
        'form': form
    }
    return render(request, 'forum/ticket_form.html', context)


@login_required
def ads(request):
    if request.user.rank == "заблокирован":
        return banned_redirect(request)
    form = AdsForm(request.POST or None)
    users = CustomUser.objects.all()
    ads = Ads.objects.all()
    ads_count = ads.count()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
    context = {
        'ads': ads,
        'users': users,
        'ads_count': ads_count,
        'form': form,
    }
    return render(request, 'forum/ads.html', context)


@ratelimit(key='ip', rate='50/m')
def rules(request):
    return render(request, 'forum/rules.html')


@ratelimit(key='ip', rate='50/m')
def users(request):
    if request.user.is_authenticated and request.user.rank == "заблокирован":
        return banned_redirect(request)
    posts = Forum.objects.select_related('author').all()
    accs = Market.objects.select_related('author').all()
    messages_count = Comment.objects.all().count()
    count_posts = posts.count()
    count_accs = accs.count()
    users_list = CustomUser.objects.order_by("-symps")
    new_users = CustomUser.objects.order_by("-date_joined")[:7]
    count_sellers = 0
    for user in users_list:
        if user.rank != "заблокирован":
            if ((user.rank == "пользователь" and user.buy_privilege != "нет привилегий")
                or (user.rank != "пользователь" and user.privilege != "местный")):
                count_sellers += 1
    count_users = users_list.count()
    search_query = request.GET.get('search', '')
    if search_query:
        users_list = CustomUser.objects.filter(username__icontains=search_query)
    count_search = users_list.count()
    context = {
        'new_users': new_users,
        'users': users_list,
        'count_sellers': count_sellers,
        'count_posts': count_posts,
        'count_users': count_users,
        'count_accs': count_accs,
        'count_search': count_search,
        'messages_count': messages_count,
    }
    return render(request, 'forum/users.html', context)


@ratelimit(key='ip', rate='50/m')
def faq(request):
    return render(request, 'forum/faq.html')


@ratelimit(key='ip', rate='50/m')
def guarantor(request):
    if request.user.is_authenticated and request.user.rank == "заблокирован":
        return banned_redirect(request)
    return render(request, 'forum/guarantor.html')


@ratelimit(key='ip', rate='50/m')
def words(request):
    return render(request, 'forum/words.html')


# Система личных сообщений
# def dialogs(self, request):
#     chats = Message.objects.filter(author=request.user, user=request.user)
#     context = {
#         'user_profile': request.user,
#         'chats': chats,
#     }
#     return render(request, 'users/dialogs.html', context)
