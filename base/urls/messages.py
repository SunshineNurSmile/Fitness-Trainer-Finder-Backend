from django.urls import path
from base.views import users as views

urlpatterns = [
    path('create/', views.sendMessage, name="messages-send"),
    path('list/<str:userid>/', views.AllMessages, name='show_all_messages'),
]