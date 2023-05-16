from django.urls import path

from . import views

app_name = 'market'

urlpatterns = [
    path('', views.market, name='index'),
    path('close/', views.close, name='close'),
    path('group/<slug:slug>/', views.group_free, name='group_free'),
    path('my_accs/', views.my_accs, name='my_accs'),
    path('<int:acc_id>/', views.acc_detail, name='acc_detail'),
    path('<int:acc_id>/buy/', views.acc_buy, name='acc_buy'),
    path('acc_sell/', views.acc_sell, name='acc_sell'),
    path('rules/', views.rules, name='rules'),
]
