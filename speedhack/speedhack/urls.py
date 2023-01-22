from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('forum.urls', namespace='forum')),
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls', namespace='users')),
    path('auth/', include('django.contrib.auth.urls')),
]
