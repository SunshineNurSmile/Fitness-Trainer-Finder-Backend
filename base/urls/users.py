from django.contrib import admin
from django.urls import path, include

from base.views import users as views

urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('register/', views.registerUser, name='register'),
    path('profile/', views.getUserProfile, name='user-profile'),
    path('profile/update/<str:pk>/', views.updateUserProfile, name='user-update-profile'),
    path('profile/create', views.createProfile, name='user-create-profile'),
    path('', views.UserList.as_view(), name='users'),

    # path('<str:pk>/', views.getUserById, name='user'),
    #
    # path('update/<str:pk>/', views.updateUser, name='user-update'),
    #
    # path('delete/<str:pk>/', views.deleteUser, name='user-delete'),
]