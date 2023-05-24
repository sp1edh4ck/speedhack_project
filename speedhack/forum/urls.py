from django.urls import path

from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.index, name='index'),
    path('forum/banned/', views.banned, name='banned'),
    path('forum/my_topics/', views.my_topics, name='my_topics'),
    path('group/<slug:slug>/', views.group_free, name='group_filter_posts'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/<str:username>/deposit/', views.deposit, name='deposit'),
    path('profile/<str:username>/ban/', views.ban, name='ban'),
    path('profile/<str:username>/info_edit/', views.info_edit, name='profile_info_edit'),
    path('profile/<str:username>/upgrade/', views.upgrade_temp, name='profile_upgrade'),
    path('profile/<str:username>/upgrade/<int:number>/', views.upgrade, name='upgrade'),
    path('forum/create_post/', views.post_create, name='post_create'),
    path('forum/<int:post_id>/', views.post_detail, name='post_detail'),
    path('forum/<int:post_id>/close/', views.post_close, name='post_close'),
    path('forum/<int:post_id>/open/', views.post_open, name='post_open'),
    path('forum/<int:post_id>/likes/', views.likes_add, name='likes_add'),
    path('forum/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('forum/<int:post_id>/delete/', views.post_delete, name='post_delete'),
    path('forum/successfully', views.successfully, name='successfully'),
    path('forum/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    # path('forum/<int:post_id>/comment/<int:comment_id>/delete', views.delete_comment, name='delete_comment'),
    path('forum/rules/', views.rules, name='rules'),
    path('forum/faq/', views.faq, name='faq'),
    path('forum/admin-panel/', views.admin_panel, name='admin_panel'),
    path('users/', views.users, name='users'),
    path('profile/<str:username>/comment', views.add_comment_profile, name='add_comment_profile'),
    path('profile/<str:username>/follow', views.profile_follow, name='profile_follow'),
    path('profile/<str:username>/unfollow', views.profile_unfollow, name='profile_unfollow'),
    path('guarantor', views.guarantor, name='guarantor'),
]
