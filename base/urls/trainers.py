from django.contrib import admin
from django.urls import path, include

from base.views import users as users_views
from base.views import trainers as trainers_views

urlpatterns = [
    path('', users_views.getTrainer, name='trainer'),
    path('update/<str:pk>/', users_views.updateTrainer, name='trainer-update'),
    path('create', users_views.createTrainer, name='trainer-create'),
    path('list', users_views.AllTrainersList.as_view(), name='trainers-list'),

    path('<str:pk>/reviews/', trainers_views.createTrainerReview, name="create-review"),
    path('top/', trainers_views.getTopTrainers, name='top-trainers'),
    path('<str:pk>/', trainers_views.getTrainerById, name='trainer-by-id'),

    path('payment/create/', trainers_views.createPayment, name="payment-add"),
    path('payment/get/', trainers_views.getMyPayment, name="payments"),
    path('payment/update/', trainers_views.updatePayment, name="payment-update"),

    path('mytrainees', users_views.getMyTrainees, name='my trainees'),

    path('mychats', trainers_views.getMyChats, name='my chats'),
    path('mynotes', trainers_views.getMyNotes, name='my notes'),
    path('toaccept/<str:pk>/', users_views.updateChatAccepted, name='accept chat'),
    path('myacceptedtrainees', users_views.getMyAcceptedTrainees, name='my accepted trainees'),

    path('uploadFile', trainers_views.index, name='upload the video'),
    path('thefile', trainers_views.getindex, name='the file'),
    path('file/<str:pk>/', trainers_views.getindexByid, name='get the file by id')


    # path('update/<str:pk>/', views.updateProduct, name="product-update"),
    # path('delete/<str:pk>/', views.deleteTrainer, name="product-delete")
]