from django.urls import path

from . import views

app_name = 'forum'

urlpatterns = [
	path('', views.index, name='index'),
	path('forum/my_topics/', views.my_topics, name='my_topics'),
	path('group/<slug:slug>/', views.group_free, name='group_filter_posts'),
	path('profile/<str:username>/', views.profile, name='profile'),
	path('profile/<str:username>/info_edit/', views.info_edit, name='profile_info_edit'),
	path('profile/<str:username>/upgrade/', views.upgrade, name='profile_upgrade'),
	path('forum/create_post/', views.post_create, name='post_create'),
	path('forum/<int:post_id>/', views.post_detail, name='post_detail'),
	path('forum/<int:post_id>/comment/', views.add_comment, name='add_comment'),
	path('forum/rules/', views.rules, name='rules'),
	path('forum/admin-panel/', views.admin_panel, name='admin_panel'),
	path('users/', views.users, name='users'),
	path('profile/<str:username>/comment', views.add_comment_profile, name='add_comment_profile'),
	path('profile/<str:username>/follow', views.profile_follow, name='profile_follow'),
	path('profile/<str:username>/unfollow', views.profile_unfollow, name='profile_unfollow'),
]
