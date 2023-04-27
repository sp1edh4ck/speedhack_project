from django.urls import path

from . import views

app_name = 'market'

urlpatterns = [
    path('', views.market, name='index'),
    path('<int:acc_id>/', views.acc_detail, name='acc_detail'),
    path('acc_sell/', views.acc_sell, name='acc_sell'),
]
