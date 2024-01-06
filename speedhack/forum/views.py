from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django_ratelimit.decorators import ratelimit
from market.models import Market
from users.forms import UserProfileAdminForm, UserProfileForm
from users.models import CustomUser, IpUser

from .forms import (AdsForm, AnswerForm, CommentForm, DepositForm, HelpForm,
                    PostForm, ProfileCommentForm)
from .models import (Ads, Comment, CommentSymp, Favourites, Follow, Forum,
                     Group, Helper, HelpForum, Like, ProfileComment, Symp,
                     User, Viewer)


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


def empty_page(request):
    return render(request, 'forum/empty_page.html')


def error404_page(request):
    return render(request, 'forum/error404_page.html')


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
    ads = Ads.objects.all()
    context = {
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
    ads = Ads.objects.all()
    context = {
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
    ads = Ads.objects.all()
    context = {
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
    helpers = Helper.objects.filter(group=group)
    context = {
        'group': group,
        'helpers': helpers,
        'objects': pagination_post(request, posts),
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
    author_symps_count = Symp.objects.filter(user=author).count()
    profile_comments = ProfileComment.objects.filter(profile=author)
    subscriptions = author.follower.all()
    subscribers = author.following.all()
    following = (
        author.following.filter(user_id=request.user.id).exists()
        if request.user.is_authenticated
        else False
    )
    context = {
        'form': form,
        'author': author,
        'posts': posts,
        'post_1': post_1,
        'author_symps_count': author_symps_count,
        'following': following,
        'profile_comments': profile_comments,
        'subscriptions': subscriptions,
        'subscribers': subscribers,
        'objects': pagination_post(request, posts),
    }
    return render(request, 'forum/profile.html', context)


@login_required
def symps_view(request, username):
    if request.user.rank == "заблокирован":
        return banned_redirect(request)
    author = get_object_or_404(User, username=username)
    user_symps = Symp.objects.filter(user=author)
    owner_symps = Symp.objects.filter(owner=author)
    context = {
        'author': author,
        'user_symps': user_symps,
        'owner_symps': owner_symps,
    }
    return render(request, 'forum/user_symps.html', context)


@login_required
def messages_view(request, username):
    if request.user.rank == "заблокирован":
        return banned_redirect(request)
    author = get_object_or_404(User, username=username)
    user_messages = Comment.objects.filter(author=author).order_by('-created')
    context = {
        'author': author,
        'user_messages': user_messages,
    }
    return render(request, 'forum/user_messages.html', context)


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
        user.save_rank = ''
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
        user.save_rank = ''
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
        my_symp = Symp.objects.filter(post=post, owner=user)
        # my_symp_comment = Symp.objects.filter(comment=comment, user=user)
        favourite = Favourites.objects.filter(post=post, user=user)
        if not Viewer.objects.filter(post=post, user=user).exists():
            Viewer.objects.create(post=post, user=user)
    views = Viewer.objects.filter(post=post).all()
    form = CommentForm(request.POST or None)
    comments = post.comment.all()
    symps = Symp.objects.filter(post=post)
    author_symps_count = Symp.objects.filter(user=post.author).count()
    if request.user.is_authenticated:
        context = {
            'form': form,
            'favourite': favourite,
            'post': post,
            'user': user,
            'views': views,
            'author_symps_count': author_symps_count,
            'symps': symps,
            'my_symp': my_symp,
            'comments': comments,
        }
        return render(request, 'forum/post_detail.html', context)
    context = {
        'form': form,
        'post': post,
        'views': views,
        'author_symps_count': author_symps_count,
        'symps': symps,
        'comments': comments,
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
    user = get_object_or_404(User, username=username)
    request_user = get_object_or_404(User, username=request.user.username)
    symps = Symp.objects.filter(user=post.author).all().count()
    if user != request.user:
        if request_user.symps_count_per_day > 0:
            if not Symp.objects.filter(post=post, user=user, owner=request.user).exists():
                request_user.symps_count_per_day -= 1
                request_user.save()
                Symp.objects.create(post=post, user=user, owner=request.user)
            else:
                if request_user.symps_count_per_day < 7:
                    request_user.symps_count_per_day += 1
                    request_user.save()
                Symp.objects.filter(post=post, user=user, owner=request.user).delete()
    comments = post.comment.all()
    if post.author.username == request.user.username:
        for comment in comments:
            user = CustomUser.objects.get(username=comment.author.username)
    else:
        user = CustomUser.objects.get(username=post.author.username)
    if post.author.privilege != "местный" and symps >= 20 and symps <= 199:
        post.author.privilege = "местный"
        post.author.save()
    elif post.author.privilege != "постоялец" and symps >= 200 and symps <= 999:
        post.author.privilege = "постоялец"
        post.author.save()
    elif post.author.privilege != "эксперт" and symps >= 1000 and symps <= 3999:
        post.author.privilege = "эксперт"
        post.author.save()
    elif post.author.privilege != "гуру" and symps >= 4000 and symps <= 9999:
        post.author.privilege = "гуру"
        post.author.save()
    elif post.author.privilege != "искусственный интелект" and symps >= 10000:
        post.author.privilege = "искусственный интелект"
        post.author.save()
    if symps < 20:
        post.author.privilege = "новорег"
        post.author.save()
    elif symps >= 20 and symps < 200:
        post.author.privilege = "местный"
        post.author.save()
    elif symps >= 200 and symps < 1000:
        post.author.privilege = "постоялец"
        post.author.save()
    elif symps >= 1000 and symps < 4000:
        post.author.privilege = "эксперт"
        post.author.save()
    elif symps >= 4000 and symps < 10000:
        post.author.privilege = "гуру"
        post.author.save()
    return redirect('forum:post_detail', post_id=post_id)


@ratelimit(key='ip', rate='50/m')
@login_required
def symps_comment_add(request, post_id, comment_id, username):
    if request.user.rank == "заблокирован":
        return banned_redirect(request)
    post = get_object_or_404(Forum, id=post_id)
    owner = get_object_or_404(User, username=username)
    comment = get_object_or_404(Comment, id=comment_id)
    if owner != request.user:
        if not CommentSymp.objects.filter(comment=comment, owner=owner, user=request.user).exists():
            owner.symps += 1
            owner.save()
            CommentSymp.objects.create(comment=comment, owner=owner, user=request.user)
        else:
            owner.symps -= 1
            owner.save()
            CommentSymp.objects.filter(comment=comment, owner=owner, user=request.user).delete()
    user = CustomUser.objects.get(username=username)
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
    if request.user.rank_lvl < "4":
        return redirect('forum:empty_page')
    users_list = CustomUser.objects.all().order_by("-date_joined")
    users_ban_list = CustomUser.objects.filter(rank="заблокирован")
    search_query = request.GET.get('search', '')
    if search_query:
        users_list = CustomUser.objects.filter(username__icontains=search_query)
    context = {
        'users_list': users_list,
        'users_ban_list': users_ban_list,
    }
    return render(request, 'forum/admin.html', context)


@login_required
def user_edit(request, username):
    user = get_object_or_404(User, username=username)
    form = UserProfileAdminForm(
        request.POST or None,
        instance=user,
    )
    if form.is_valid():
        if user.buy_privilege != form.cleaned_data.get('id_buy_privilege'):
            user.time_buy_privilege = timezone.now()
        if user.market_privilege != form.cleaned_data.get('id_market_privilege'):
            user.time_buy_market_privilege = timezone.now()
        user.save()
        form.username = username
        form.brt_day = request.POST.get('brt_day')
        form.brt_month = request.POST.get('brt_month')
        form.brt_year = request.POST.get('brt_year')
        form.save()
        return redirect('forum:admin_panel')
    return redirect('forum:admin_panel')
    # return render(request, 'forum/admin_user_edit.html', context)


@login_required
def tickets(request):
    if request.user.is_authenticated and request.user.rank == "заблокирован":
        return banned_redirect(request)
    if request.user.rank_lvl < "4":
        return redirect('forum:empty_page')
    tickets_count = HelpForum.objects.all().count()
    tickets_open = HelpForum.objects.filter(open=True)
    tickets_close = HelpForum.objects.filter(open=False)
    context = {
        'tickets_count': tickets_count,
        'tickets_open': tickets_open,
        'tickets_close': tickets_close,
    }
    return render(request, 'forum/tickets.html', context)


@ratelimit(key='ip', rate='50/m')
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


@ratelimit(key='ip', rate='50/m')
@login_required
def ticket(request, ticket_id):
    if request.user.rank == "заблокирован":
        return banned_redirect(request)
    form = AnswerForm(request.POST or None)
    ticket = get_object_or_404(HelpForum, pk=ticket_id)
    comments = ticket.answer.all()
    context = {
        'form': form,
        'ticket': ticket,
        'comments': comments,
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
            return redirect('forum:ticket', ticket_id=ticket.id)
    context = {
        'form': form
    }
    return render(request, 'forum/ticket_form.html', context)


@login_required
def ads(request):
    if request.user.rank == "заблокирован":
        return banned_redirect(request)
    if request.user.rank_lvl < "4":
        return redirect('forum:empty_page')
    form = AdsForm(request.POST or None)
    users = CustomUser.objects.all()
    ads = Ads.objects.all()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
    context = {
        'ads': ads,
        'users': users,
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
    messages = Comment.objects.all()
    users_list = CustomUser.objects.all().annotate(symps=Count("symper")).order_by("-symps")
    users_list_bySymps = CustomUser.objects.all().annotate(symps=Count("symper")).order_by("-symps", "date_joined")[:20]
    users_list_byComments = CustomUser.objects.all().annotate(user_comments=Count("comments")).order_by("-user_comments", "date_joined")[:20]
    users_list_byStaff = CustomUser.objects.filter(rank_lvl__gte="4").annotate(symps=Count("symper")).order_by("-symps")[:20]
    new_users = CustomUser.objects.order_by("-date_joined")[:7]
    users_sellers = users_list.exclude(
        market_privilege="нет привилегий",
        rank_lvl__lt="4",
        privilege__lt="постоялец",
    ).count()
    search_query = request.GET.get('search', '')
    if search_query:
        users_list_bySymps = CustomUser.objects.filter(username__icontains=search_query)
    context = {
        'posts': posts,
        'accs': accs,
        'messages': messages,
        'users_list': users_list,
        'users_list_bySymps': users_list_bySymps,
        'users_list_byComments': users_list_byComments,
        'users_list_byStaff': users_list_byStaff,
        'new_users': new_users,
        'users_sellers': users_sellers,
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
