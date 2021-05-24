from django.urls import path
from director import views

urlpatterns = [
    path('', views.index),
]
