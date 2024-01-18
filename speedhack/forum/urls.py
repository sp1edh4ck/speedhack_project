from django.urls import path

from . import views

app_name = 'forum'

urlpatterns = [
    # * ссылки на страницы
    path('', views.index, name='index'),
    # ? ----------
    # * страница, для отображения ошибки 403 (может пригодится)
    # path('ratelimited/', views.ratelimited, name='ratelimited'),
    # ? ----------
    path('forum/my_topics/', views.my_topics, name='my_topics'),
    path('forum/favourites/', views.favourites, name='favourites'),
    path('forum/tickets/open/', views.ticket_form, name='ticket_form'),
    path('group/<slug:slug>/', views.group_free, name='group_filter_posts'),
    path('profile/<str:username>/', views.profile, name='profile'),
    # ? ----------
    # TODO: сделать для пользователей с привилегиями короткие ссылки на профиль
    # path('<str:username>/', views.profile, name='profile'),
    # ? ----------
    path('profile/<str:username>/symps/', views.symps_view, name='symps_view'),
    path('profile/<str:username>/messages/', views.messages_view, name='messages_view'),
    path('profile/<str:username>/subscriptions/', views.subscriptions_view, name='subscriptions_view'),
    path('profile/<str:username>/subscribers/', views.subscribers_view, name='subscribers_view'),
    path('profile/<str:username>/info-edit/', views.info_edit, name='profile_info_edit'),
    path('profile/<str:username>/upgrade/', views.upgrade_temp, name='profile_upgrade'),
    path('forum/create_post/', views.post_create, name='post_create'),
    path('forum/<int:post_id>/', views.post_detail, name='post_detail'),
    path('forum/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/tickets/', views.tickets, name='tickets'),
    path('admin-panel/ads/', views.ads, name='ads'),
    path('tickets/<str:username>/', views.my_tickets, name='my_tickets'),
    path('ticket/<int:ticket_id>/', views.ticket, name='ticket'),
    path('<str:username>/complaint/', views.complaint, name='complaint'),
    path('users/', views.users, name='users'),
    path('misc/banned/', views.banned, name='banned'),
    path('misc/empty-page/', views.empty_page, name='empty_page'),
    path('misc/rules/', views.rules, name='rules'),
    path('misc/words/', views.words, name='words'),
    path('misc/faq/', views.faq, name='faq'),
    path('misc/successfully/', views.successfully, name='successfully'),
    path('misc/guarantor/', views.guarantor, name='guarantor'),
    path('misc/about/', views.about_us, name='about_us'),
    # * ссылки на действия
    path('profile/<str:username>/deposit/<int:number>/', views.deposit, name='deposit'),
    path('profile/<str:username>/ban/', views.ban, name='ban'),
    path('profile/<str:username>/upgrade/<int:number>/', views.upgrade, name='upgrade'),
    path('profile/<str:username>/comment/<str:author>/<int:comment_id>/', views.delete_profile_comment, name='delete_profile_comment'),
    path('profile/<str:username>/follow/<int:number>/', views.profile_uf, name='profile_uf'),
    path('forum/<int:post_id>/favourites-post-save/<int:number>/', views.favourites_post_save, name='favourites_post_save'),
    path('forum/<int:post_id>/close/<int:number>/', views.post_oc, name='post_oc'),
    path('forum/<int:post_id>/symps/<str:username>/', views.symps_add, name='symps_add'),
    path('forum/<int:post_id>/delete/', views.post_delete, name='post_delete'),
    path('forum/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    # path('forum/<int:post_id>/symps-comment/<int:comment_id>/<str:username>/', views.symps_comment_add, name='symps_comment_add'),
    path('forum/<int:post_id>/comment/edit/', views.edit_comment, name='edit_comment'),
    path('forum/<int:post_id>/del-comment/<int:id>/', views.delete_comment, name='delete_comment'),
    path('admin-panel/user-edit/<str:username>/', views.admin_user_edit, name='admin_user_edit'),
    path('admin-panel/<str:username>/ban/', views.admin_ban, name='admin_ban'),
    path('admin-panel/ticket/<int:ticket_id>/close/<int:number>/', views.ticket_oc, name='ticket_oc'),
    path('admin-panel/ticket/<int:ticket_id>/delete/', views.ticket_delete, name='ticket_delete'),
    path('ticket/<int:ticket_id>/comment/', views.add_answer, name='add_answer'),

    # Система личных сообщений
    # path('dialogs/', views.dialogs, name='dialogs'),
    # path('dialogs/create/(?P<user_id>\d+)/', views.create_dialog, name='create_dialog'),
    # path('dialogs/(?P<chat_id>\d+)/', views.messages, name='messages'),
]
