from django.contrib import admin
from django.urls import path, include

from base.views import users as views

urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('register/', views.registerUser, name='register'),
    path('trainees/', include('base.urls.trainees')),
    path('trainers/', include('base.urls.trainers')),

]