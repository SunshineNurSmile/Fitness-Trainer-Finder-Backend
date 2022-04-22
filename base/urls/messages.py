from django.urls import path
from base.views import users as views

urlpatterns = [
    path('create/', views.sendMessage, name="messages-send"),  # To send message
    path('list/<str:userid>/', views.AllMessages, name='show_all_messages'),  # To show the list of message
]