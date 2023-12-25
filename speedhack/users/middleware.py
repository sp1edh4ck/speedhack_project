from django.core.cache import cache
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

from .models import CustomUser


class ActiveUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated and request.session.session_key:
            cache_key = f'last-seen-{request.user.id}'
            last_login = cache.get(cache_key)
            if not last_login:
                CustomUser.objects.filter(id=request.user.id).update(last_login=timezone.now())
                cache.set(cache_key, timezone.now(), 60)
