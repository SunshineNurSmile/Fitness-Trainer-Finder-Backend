from django.contrib import admin
from django.urls import path, include

from base.views import users as users_views
from base.views import trainers as trainers_views

urlpatterns = [
    path('', users_views.getTrainer, name='trainer'),
    path('update/<str:pk>/', users_views.updateTrainer, name='trainer-update'),
    path('create', users_views.createTrainer, name='trainer-create'),
    path('list', users_views.TrainerList.as_view(), name='trainers-list'),

    path('<str:pk>/reviews/', trainers_views.createTrainerReview, name="create-review"),
    path('top/', trainers_views.getTopTrainers, name='top-trainers'),
    path('<str:pk>/', trainers_views.getTrainerById, name='trainer-by-id'),

    # path('update/<str:pk>/', views.updateProduct, name="product-update"),
    # path('delete/<str:pk>/', views.deleteTrainer, name="product-delete")
]