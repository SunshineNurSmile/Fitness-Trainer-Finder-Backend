from django.urls import path
from base.views import orders as views

urlpatterns = [
    path('create/', views.createOrder, name="orders-add"),
    path('<str:pk>/myorders/', views.getMyOrders, name='myorders'),
    path('<str:pk>/', views.getOrderById, name='users-order'),
    path('<str:pk>/pay/', views.updateOrderToPaid, name='pay')
]