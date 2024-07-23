from django.urls import path

from .views import GetUserThroughTgLink, get_user_through_tg_link

urlpatterns = [
    path('get_users/', GetUserThroughTgLink.as_view()),
    path('get_user_through_tg_link/', get_user_through_tg_link),
]
