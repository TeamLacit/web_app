from django.urls import path
from administrator import views

urlpatterns = [
    path('invitation/', views.invite_user, name='invitation'),
    path('', views.index, name='administrator-page'),
]