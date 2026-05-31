from django.urls import path, include
from . import views

urlpatterns = [
    # Cuentas y registro
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    
    # 1. Listas de tareas
    path('lists/', views.lists_root, name='lists_root'), 
    path('lists/<int:list_id>/', views.list_detail_api, name='list_detail_api'),
    
    # 2. Tareas dentro de una lista
    path('lists/<int:list_id>/tasks/', views.task_detail, name='task_detail'),
    path('lists/<int:list_id>/tasks/<int:task_id>/', views.task_actions_api, name='task_actions_api'),
]
