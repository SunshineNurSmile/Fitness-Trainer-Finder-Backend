from django.contrib import admin
from django.urls import path, include

from base.views import users as views
from base.views import orders as order_views

urlpatterns = [

    path('', views.getTrainee, name='trainee'),  # get the information of trainee
    path('update/<str:pk>/', views.updateTrainee, name='trainee-update'),  # update the trainee's information
    path('create', views.createTrainee, name='trainee-create'),  # create trainee after they log_in
    path('list/', views.AllTraineesList.as_view(), name='trainees'),  # show all the trainees
    path('mytrainer/', order_views.getMyTrainer, name='my trainers'),  # show the trainers of trainee
    path('createnote/', views.createNote, name='notes-add'),  # create the notification
    path('chat/get/', views.getTraineeChats, name='my chats'),  # get the chat(trainer)
    path('<str:pk>/', views.getTraineeById, name='traineeByid')  # get trainee By trainee_id

]