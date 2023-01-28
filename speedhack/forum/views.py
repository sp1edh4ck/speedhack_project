from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page

from users.models import CustomUser

from .forms import CommentForm, PostForm
from .models import Follow, Forum, Ip, User


def pagination(request, post_list):
    paginator = Paginator(post_list, 12)
    return paginator.get_page(request.GET.get('page'))


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def post_view(request, slug):
    post = Forum.objects.get(slug=slug)

    ip = get_client_ip(request)

    if Ip.objects.filter(ip=ip).exists():
        post.views.add(Ip.objects.get(ip=ip))
    else:
        Ip.objects.create(ip=ip)
        post.views.add(Ip.objects.get(ip=ip))  
    
    context = {
        'post' : post,
    }
    return render(request, 'main/post.html', context)


# @cache_page(20, key_prefix='index_page')
def index(request):
    posts = Forum.objects.select_related('author').all()
    template = 'forum/index.html'
    context = {
        'objects': pagination(request, posts)
    }
    return render(request, template, context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    following = (
				author.following.filter(user_id=request.user.id).exists()
				if request.user.is_authenticated
				else False
		)
    count_posts = posts.count()
    template = 'forum/profile.html'
    context = {
        'author': author,
        'following': following,
        'count_posts': count_posts,
        'objects': pagination(request, posts),
    }
    return render(request, template, context)


def post_detail(request, post_id):
    post = get_object_or_404(Forum, id=post_id)
    form = CommentForm(request.POST or None)
    comments = post.comments.all()
    ip = get_client_ip(request)
    if Ip.objects.filter(ip=ip).exists():
        post.views.add(Ip.objects.get(ip=ip))
    else:
        Ip.objects.create(ip=ip)
        post.views.add(Ip.objects.get(ip=ip))
    template = 'forum/post_detail.html'
    context = {
				'form': form,
        'post': post,
        'comments': comments
    }
    return render(request, template, context)


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
    template = 'forum/post_create.html'
    context = {
        'form': form
    }
    return render(request, template, context)


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


"""
@login_required
def follow_index(request):
		template = 'forum/follow.html'
 		post_list = Forum.objects.filter(author__following__user=request.user).all()
 		context = {
 				'objects': pagination(request, post_list)
 		}
 		return render(request, template, context)
"""


@login_required
def profile_follow(request, username):
		author = get_object_or_404(User, username=username)
		sub = request.user.subscriber
		if author != request.user:
				if not Follow.objects.filter(author=author, user=request.user).exists():
						Follow.objects.create(author=author, user=request.user)
						sub += 1
				sub -= 1
		return redirect('forum:profile', username=username)


@login_required
def profile_unfollow(request, username):
		author = get_object_or_404(User, username=username)
		author.following.filter(user=request.user).delete()
		return redirect('forum:profile', username=username)


@login_required
def admin_panel(request):
		template = 'forum/admin.html'
		author = Forum.objects.select_related('author').all()
		users_list = CustomUser.objects.all()
		context = {
				'author': author,
				'users': users_list,
		}
		return render(request, template, context)
