from django.urls import path

from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('forum/create_post/', views.post_create, name='post_create'),
    path('forum/<int:post_id>/', views.post_detail, name='post_detail'),
    path('forum/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('forum/faq/', views.faq, name='faq'),
    path('forum/admin-panel/', views.admin_panel, name='admin_panel'),
    path('users/', views.users, name='users'),
    path('profile/<str:username>/follow', views.profile_follow, name='profile_follow'),
    path('profile/<str:username>/unfollow', views.profile_unfollow, name='profile_unfollow'),
]
