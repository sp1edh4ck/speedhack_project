from django.urls import path

from .views import GetUser, GetUsers, GetUserTgLink

urlpatterns = [
    path('get_users/', GetUsers.as_view()),
    path('get_user/<str:username>/', GetUser.as_view()),
    path('get_user_tg/<str:tg_link>/', GetUserTgLink.as_view()),
]
