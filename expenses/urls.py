from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.user_list),
    path('users/<int:pk>/', views.user_detail),
    path('users/create/', views.user_create),
    path('expenses/', views.expense_list),
    path('expenses/<int:pk>/', views.expense_detail),
    path('expenses/create/', views.expense_create),
]
