from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from market.models import Market
from users.forms import UserProfileForm
from users.models import CustomUser, IpUser

from .forms import ProfileCommentForm, CommentForm, PostForm, DepositForm, HelpForm, AnswerForm
from .models import Follow, Forum, User, Group, Comment, Viewers, HelpForum


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


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
    return redirect('forum:banned')


def banned(request):
    return render(request, 'users/banned.html')


def successfully(request):
    return render(request, 'forum/successfully.html')


def index(request):
    if request.user.is_authenticated and request.user.rank == "заблокирован":
        return banned_redirect(request)
    ip_address = get_client_ip(request)
    search_query = request.GET.get('search', '')
    if search_query:
        posts = Forum.objects.filter(title__icontains=search_query)
    else:
        posts = Forum.objects.select_related('author').all()
    count_posts = posts.count()
    context = {
        'count_posts': count_posts,
        'objects': pagination_post(request, posts)
    }
    return render(request, 'forum/index.html', context)


@login_required
def my_topics(request):
    if request.user.is_authenticated and request.user.rank == "заблокирован":
        return banned_redirect(request)
    user = request.user
    search_query = request.GET.get('search', '')
    if search_query:
        posts = user.posts.filter(title__icontains=search_query)
    else:
        posts = user.posts.all()
    count_posts = posts.count()
    context = {
        'count_posts': count_posts,
        'objects': pagination_post(request, posts)
    }
    return render(request, 'forum/index.html', context)


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
    count_posts = posts.count()
    context = {
        'count_posts': count_posts,
        'group': group,
        'objects': pagination_post(request, posts),
    }
    return render(request, 'forum/template_groups.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    subscriptions = author.follower.all()
    subscribers = author.following.all()
    following = (
        author.following.filter(user_id=request.user.id).exists()
        if request.user.is_authenticated
        else False
    )
    count_posts = posts.count()
    count_subscriptions = subscriptions.count()
    count_subscribers = subscribers.count()
    context = {
        'author': author,
        'following': following,
        'count_posts': count_posts,
        'count_subscriptions': count_subscriptions,
        'count_subscribers': count_subscribers,
        'objects': pagination_post(request, posts),
        'subscriptions': pagination_sub(request, subscriptions),
        'subscribers': pagination_sub(request, subscribers),
    }
    return render(request, 'forum/profile.html', context)


# @login_required
# def payment(request, username, number):
#     user = CustomUser.objects.get(username=username)
#     return render(request, 'forum/payments.html')


@login_required
def deposit(request, username, number):
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


@login_required
def upgrade_temp(request, username):
    if request.user.rank == "заблокирован":
        return banned_redirect(request)
    return render(request, 'forum/upgrade.html')


@login_required
def upgrade(request, username, number):
    if request.user.rank == "заблокирован":
        return banned_redirect(request)
    user = CustomUser.objects.get(username=username)
    if number == 1 and user.balance <= 100:
        user.market_privilege = "продавец"
        user.balance -= 100
        user.time_buy_market_privilege = timezone.now()
        user.save()
    if number == 2 and user.balance <= 100:
        user.profile_sub = True
        user.balance -= 100
        user.time_buy_profile_sub = timezone.now()
        user.save()
    if number == 3 and user.balance <= 2999:
        user.buy_privilege = "легенда"
        user.balance -= 2999
        user.time_buy_privilege = timezone.now()
        user.save()
    if number == 4 and user.balance <= 1500:
        user.buy_privilege = "суприм"
        user.balance -= 1500
        user.time_buy_privilege = timezone.now()
        user.save()
    if number == 5 and user.balance <= 7500:
        user.buy_privilege = "уник"
        user.balance -= 7500
        user.time_buy_privilege = timezone.now()
        user.save()
    return redirect('forum:profile', username=username)


@login_required
def add_comment_profile(request, username):
    if request.user.rank == "заблокирован":
        return banned_redirect(request)
    form = ProfileCommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.save()
    return redirect('forum:profile', username=username)


def post_detail(request, post_id):
    post = get_object_or_404(Forum, id=post_id)
    if request.user.is_authenticated and request.user.rank == "заблокирован" and post.author != request.user:
        return banned_redirect(request)
    # if request.user.is_authenticated:
        # viewers = post.viewers.all()
        # post.view += 1
        # post.save()
    form = CommentForm(request.POST or None)
    comments = post.comments.all()
    count_comments = comments.count()
    context = {
        'form': form,
        'post': post,
        'comments': comments,
        'count_comments': count_comments,
    }
    return render(request, 'forum/post_detail.html', context)


@login_required
def post_close(request, post_id):
    post = get_object_or_404(Forum, id=post_id)
    post.closed = True
    post.save()
    return redirect('forum:post_detail', post_id=post_id)


@login_required
def post_open(request, post_id):
    post = get_object_or_404(Forum, id=post_id)
    post.closed = False
    post.save()
    return redirect('forum:post_detail', post_id=post_id)


@login_required
def likes_add(request, post_id):
    post = get_object_or_404(Forum, id=post_id)
    comments = post.comments.all()
    if request.user.rank == "заблокирован":
        return banned_redirect(request)
    if post.author.username == request.user.username:
        for comment in comments:
            user = CustomUser.objects.get(username=comment.author.username)
    else:
        user = CustomUser.objects.get(username=post.author.username)
    user.likes += 1
    user.save()
    if user.privilege != "местный" and user.likes >= 20 and user.likes <= 199:
        user.privilege = "местный"
        user.save()
    elif user.privilege != "постоялец" and user.likes >= 200 and user.likes <= 999:
        user.privilege = "постоялец"
        user.save()
    elif user.privilege != "эксперт" and user.likes >= 1000 and user.likes <= 3999:
        user.privilege = "эксперт"
        user.save()
    elif user.privilege != "гуру" and user.likes >= 4000 and user.likes <= 9999:
        user.privilege = "гуру"
        user.save()
    elif user.privilege != "искусственный интелект" and user.likes >= 10000:
        user.privilege = "искусственный интелект"
        user.save()
    return redirect('forum:post_detail', post_id=post_id)


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
    if (request.user == post.author
        or request.user.rank == "владелец"
        or request.user.rank == "гл. администратор"
        or request.user.rank == "администратор"
        or request.user.rank == "арбитр"
        or request.user.rank == "куратор"):
        if request.method == 'POST':
            if form.is_valid():
                post.edit = True
                post.save()
                form.save()
                return redirect('forum:post_detail', post_id=post_id)
        template = 'forum/post_create.html'
        context = {
            'post': post,
            'form': form,
            'is_edit': True,
        }
        return render(request, template, context)
    return redirect('forum:post_detail', post_id=post_id)


@login_required
def post_delete(request, post_id):
    if request.user.rank == "заблокирован":
        return banned_redirect(request)
    post = get_object_or_404(Forum, pk=post_id)
    if (request.user == post.author
        or request.user.rank == "владелец"
        or request.user.rank == "гл. администратор"
        or request.user.rank == "администратор"
        or request.user.rank == "арбитр"
        or request.user.rank == "куратор"):
        Forum.objects.filter(pk=post_id).delete()
        return redirect('forum:successfully')


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Forum, pk=post_id)
    if post.closed == False:
        if request.user.rank == "заблокирован":
            return banned_redirect(request)
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


@login_required
def delete_comment(request, post_id, id):
    if request.user.rank == "заблокирован":
        return banned_redirect(request)
    comment = get_object_or_404(Comment, id=id)
    comment.delete()
    return redirect('forum:post_detail', post_id=post_id)


@login_required
def profile_follow(request, username):
    if request.user.rank == "заблокирован":
        return banned_redirect(request)
    author = get_object_or_404(User, username=username)
    if author != request.user:
        if not Follow.objects.filter(author=author, user=request.user).exists():
            Follow.objects.create(author=author, user=request.user)
    return redirect('forum:profile', username=username)


@login_required
def profile_unfollow(request, username):
    if request.user.rank == "заблокирован":
        return banned_redirect(request)
    author = get_object_or_404(User, username=username)
    author.following.filter(user=request.user).delete()
    return redirect('forum:profile', username=username)


@login_required
def admin_panel(request):
    if request.user.rank == "заблокирован":
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
def tickets(request):
    if request.user.rank == "заблокирован":
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


@login_required
def my_tickets(request, username):
    if request.user.rank == "заблокирован":
        return banned_redirect(request)
    user = request.user
    my_tickets = user.tickets.all()
    context = {
        'my_tickets': my_tickets,
    }
    return render(request, 'forum/my_tickets.html', context)


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


@login_required
def add_answer(request, ticket_id):
    ticket = get_object_or_404(HelpForum, pk=ticket_id)
    if ticket.open:
        if request.user.rank == "заблокирован":
            return banned_redirect(request)
        form = AnswerForm(request.POST or None)
        if form.is_valid():
            user = CustomUser.objects.get(username=request.user.username)
            user.messages += 1
            user.save()
            answer = form.save(commit=False)
            answer.author = request.user
            answer.ticket = ticket
            answer.save()
            return redirect('forum:ticket', ticket_id=ticket_id)
    return redirect('forum:ticket', ticket_id=ticket_id)


@login_required
def ticket_close(request, ticket_id):
    ticket = get_object_or_404(HelpForum, id=ticket_id)
    ticket.open = False
    ticket.save()
    return redirect('forum:tickets')


@login_required
def ticket_open(request, ticket_id):
    ticket = get_object_or_404(HelpForum, id=ticket_id)
    ticket.open = True
    ticket.save()
    return redirect('forum:tickets')


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


def rules(request):
    return render(request, 'forum/rules.html')


def users(request):
    if request.user.is_authenticated and request.user.rank == "заблокирован":
        return banned_redirect(request)
    posts = Forum.objects.select_related('author').all()
    accs = Market.objects.select_related('author').all()
    count_posts = posts.count()
    count_accs = accs.count()
    users_list = CustomUser.objects.all()
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
    author = Forum.objects.select_related('author').all()
    context = {
        'author': author,
        'users': users_list,
        'count_sellers': count_sellers,
        'count_posts': count_posts,
        'count_users': count_users,
        'count_accs': count_accs,
        'count_search': count_search,
    }
    return render(request, 'forum/users.html', context)


def faq(request):
    return render(request, 'forum/faq.html')


def guarantor(request):
    return render(request, 'forum/guarantor.html')


def words(request):
    return render(request, 'forum/words.html')
