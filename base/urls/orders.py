from django.urls import path
from base.views import orders as views

urlpatterns = [
    path('create/', views.createOrder, name="orders-add"),  # To Creat order
    path('myorders/', views.getMyOrders, name='my_orders'),  # To show the user's order
    path('<str:pk>/', views.getOrderById, name='users-order'),  # Get the order by the order id
    path('<str:pk>/pay/', views.updateOrderToPaid, name='pay'),  # Update the order after being paid
]