from django.contrib import admin
from django.urls import path, include

from base.views import users as users_views
from base.views import trainers as trainers_views

urlpatterns = [
    path('', users_views.getTrainer, name='trainer'), # get the information of trainer
    path('update/<str:pk>/', users_views.updateTrainer, name='trainer-update'),  # update the trainer
    path('create', users_views.createTrainer, name='trainer-create'),  # create the trainer after the user login
    path('list', users_views.AllTrainersList.as_view(), name='trainers-list'),  # show the list of all trainers

    path('<str:pk>/reviews/', trainers_views.createTrainerReview, name="create-review"),
    path('top/', trainers_views.getTopTrainers, name='top-trainers'),
    path('<str:pk>/', trainers_views.getTrainerById, name='trainer-by-id'),

    path('payment/create/', trainers_views.createPayment, name="payment-add"),  # create payment options part
    path('payment/get/', trainers_views.getMyPayment, name="payments"),  # get payment of trainer
    path('payment/update/', trainers_views.updatePayment, name="payment-update"),  # update the payment
    path('payment/<str:pk>/', trainers_views.getMyPaymentById, name='payment_Id'),  # get the payment by trainer_id

    path('mytrainees', users_views.getMyTrainees, name='my trainees'),  # get the trainee of trainers

    path('chat/create/', users_views.createChat, name='chats-add'),  # create the chat part
    path('chat/get/', trainers_views.getTrainerChats, name='my chats'),  # get the chat of trainer
    path('mynotes', trainers_views.getMyNotes, name='my notes'),  # get the notes of trainer
    path('note/delete/', trainers_views.deleteMyNotes, name='delete my notes'),  # delete the notes


    path('uploadFile', trainers_views.index, name='upload the video'),  # upload the video
    path('thefile', trainers_views.getIndex, name='the file'),  # show the video
    path('file/<str:pk>/', trainers_views.getIndexByid, name='get the file by id')  # get the file by trainer id
]