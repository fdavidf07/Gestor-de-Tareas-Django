from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('todo.urls')), # Esto le dice a Django que use las URLs de nuestra app
]