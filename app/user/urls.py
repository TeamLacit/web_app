from django.urls import path
from user import views

urlpatterns = [
    path('change-data/', views.change_data_user, name='change-data'),
    path('', views.index),
]
