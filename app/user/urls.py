from django.urls import path
from user import views

urlpatterns = [
    path('change-data/', views.change_data_user, name='change-data'),
    path('list-tasks/', views.tasks, name='list-tasks'),
    path('change-password/', views.change_password_user, name='change-password'),
    path('', views.index),
]
