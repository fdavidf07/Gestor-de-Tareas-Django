from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')), # Login y Logout automáticos
    path('register/', views.register, name='register'),
    path('lists/delete/<int:list_id>/', views.delete_list, name='delete_list'),
    path('lists/<int:list_id>/tasks/', views.task_detail, name='task_detail'),
    path('tasks/toggle/<int:task_id>/', views.toggle_task, name='toggle_task'),
    path('tasks/delete/<int:task_id>/', views.delete_task, name='delete_task'),
]