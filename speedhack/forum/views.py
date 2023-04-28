from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from users.forms import UserProfileForm, UserUniquiForm
from users.models import CustomUser

from .forms import ProfileCommentForm, CommentForm, PostForm
from .models import Follow, Forum, User, Group


def pagination_post(request, post_list):
    paginator = Paginator(post_list, 12)
    return paginator.get_page(request.GET.get('page'))


def pagination_sub(request, sub_list):
    paginator = Paginator(sub_list, 5)
    return paginator.get_page(request.GET.get('page'))


def pagination_comments(request, comment_list):
    paginator = Paginator(comment_list, 5)
    return paginator.get_page(request.GET.get('page'))


def banned(request):
    return render(request, 'users/banned.html')


def index(request):
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


def my_topics(request):
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
    group = get_object_or_404(Group, slug=slug)
    search_query = request.GET.get('search', '')
    posts = group.posts.all()
    if search_query:
        posts = group.posts.filter(title__icontains=search_query)
    else:
        posts = group.posts.all()
    count_posts = posts.count()
    template = 'forum/template_groups.html'
    context = {
        'count_posts': count_posts,
        'group': group,
        'objects': pagination_post(request, posts),
    }
    return render(request, template, context)


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


@login_required
def info_edit(request, username):
    form = UserProfileForm(
        request.POST or None,
        files=request.FILES or None,
        instance=request.user
    )
    if form.is_valid():
        form.save()
        return redirect('forum:profile', username=username)
    context = {
        'form': form,
    }
    return render(request, 'forum/info_edit.html', context)


@login_required
def upgrade(request, username):
    form = UserUniquiForm(
        request.POST or None,
        instance=request.user
    )
    if request.method == 'POST':
        if form.is_valid():
            user = CustomUser(username=username)
            form = user.unique = True
            form.save()
            return redirect('forum:profile', username=username)
        else:
            form = UserUniquiForm()
    context = {
        'form': form,
    }
    return render(request, 'forum/upgrade.html', context)


@login_required
def add_comment_profile(request, username):
    form = ProfileCommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.save()
    return redirect('forum:profile', username=username)


def post_detail(request, post_id):
    post = get_object_or_404(Forum, id=post_id)
    form = CommentForm(request.POST or None)
    comments = post.comments.all()
    context = {
        'form': form,
        'post': post,
        'comments': comments
    }
    return render(request, 'forum/post_detail.html', context)


@login_required
def post_create(request):
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
    post = get_object_or_404(Forum, pk=post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if request.user == post.author:
        if request.method == 'POST':
            if form.is_valid():
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
def add_comment(request, post_id):
    post = get_object_or_404(Forum, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('forum:post_detail', post_id=post_id)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if author != request.user:
        if not Follow.objects.filter(author=author, user=request.user).exists():
            Follow.objects.create(author=author, user=request.user)
    return redirect('forum:profile', username=username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    author.following.filter(user=request.user).delete()
    return redirect('forum:profile', username=username)


@login_required
def admin_panel(request):
    author = Forum.objects.select_related('author').all()
    users_list = CustomUser.objects.all()
    context = {
        'author': author,
        'users': users_list,
    }
    return render(request, 'forum/admin.html', context)


def rules(request):
    return render(request, 'forum/rules.html')


def users(request):
    posts = Forum.objects.select_related('author').all()
    count_posts = posts.count()
    users_list = CustomUser.objects.all()
    count_users = users_list.count()
    search_query = request.GET.get('search', '')
    if search_query:
        users_list = CustomUser.objects.filter(username__icontains=search_query)
    count_search = users_list.count()
    author = Forum.objects.select_related('author').all()
    context = {
        'author': author,
        'users': users_list,
        'count_posts': count_posts,
        'count_users': count_users,
        'count_search': count_search,
    }
    return render(request, 'forum/users.html', context)
