from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page

from .models import Forum


# def pagination(request, post_list):
#     paginator = Paginator(post_list, 25)
#     return paginator.get_page(request.GET.get('page'))


@cache_page(20, key_prefix='index_page')
def index(request):
    posts = Forum.objects.select_related('author').all()
    template = 'forum/index.html'
    context = {
        'objects': posts
        # 'objects': pagination(request, posts)
    }
    return render(request, template, context)
