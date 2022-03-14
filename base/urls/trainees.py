from django.contrib import admin
from django.urls import path, include

from base.views import users as views

urlpatterns = [
    path('', views.getTrainee, name='trainee'),
    path('update/<str:pk>/', views.updateTrainee, name='trainee-update'),
    path('create', views.createTrainee, name='trainee-create'),
    path('list/', views.TraineeList.as_view(), name='trainees'),
]