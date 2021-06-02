from django.urls import path
from administrator import views

urlpatterns = [
    path('company-list/', views.company_list, name='company-list'),
    path('company/<id>/', views.edit_company, name='edit-company'),
    path('company/', views.edit_company, name='add-company'),
    path('delete-company/<id>/', views.delete_company, name='delete-company'),
    path('user/<id>/', views.change_user, name='user'),
    path('delete-user/<id>/', views.delete_user, name='delete-user'),
    path('invitation/', views.invite_user, name='invitation'),
    path('', views.index, name='administrator-page'),
]