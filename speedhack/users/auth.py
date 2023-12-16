import datetime
import hashlib

from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.core.cache import cache


class BruteForceProtectedAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        if username is None:
            return None

        if getattr(settings, 'AUTH_BLOCK_RATE', None):
            now = datetime.datetime.now()
            key = hashlib.md5(username.encode('utf-8')).hexdigest()
            last_user_login = cache.get(key + '-login-timestamp', now - datetime.timedelta(days=1))
            cache.set(key + '-login-timestamp', now)
            if (now - last_user_login) < datetime.timedelta(seconds=settings.AUTH_BLOCK_RATE):
                return None

        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None