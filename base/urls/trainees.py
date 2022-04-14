from django.contrib import admin
from django.urls import path, include

from base.views import users as views
from base.views import orders as order_views

urlpatterns = [
    path('', views.getTrainee, name='trainee'),
    path('update/<str:pk>/', views.updateTrainee, name='trainee-update'),
    path('create', views.createTrainee, name='trainee-create'),
    path('list/', views.AllTraineesList.as_view(), name='trainees'),
    path('mytrainer/', order_views.getMyTrainer, name='my trainers'),
    path('createnote/', views.createNote, name='notes-add'),
    path('chat/get/', views.getTraineeChats, name='my chats'),

]