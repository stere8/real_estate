# orders/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('<int:pk>/', views.order_detail, name='order_detail'),
    path('cancel-order/<int:pk>/', views.cancel_order, name='cancel_order'),
    path('accept-order/<int:pk>/', views.accept_order, name='accept_order'),
]
