from django.contrib import admin
from django.urls import path
from usertasks import views

app_name = 'usertasks'
urlpatterns = [
    path('', views.index, name='index'),
    path('user/<int:user_id>/', views.detail, name='detail'),
    path('task/', views.task, name='task'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('add_user/',views.add_user, name='add_user'),
    path('add_task/',views.add_task, name='add_task'),
    path('update_user/<int:id>/', views.update_user, name='update_user'),
    path('update_task/<int:id>/', views.update_task, name='update_task'),
    path('delete_user/<int:id>/', views.delete_user, name='delete_user'),
    path('delete_task/<int:id>/', views.delete_task, name='delete_task'),
]