from django.db import models
from django.contrib.auth.models import User

# Esta es la tabla para las listas de tareas
class TaskList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Cada lista pertenece a un usuario
    name = models.CharField(max_length=200) # Nombre de la lista
    created_at = models.DateTimeField(auto_now_add=True) # Fecha automática

    def __str__(self):
        return self.name

# Esta es la tabla para las tareas individuales
class Task(models.Model):
    task_list = models.ForeignKey(TaskList, on_delete=models.CASCADE, related_name="tasks") # Relación con la lista
    title = models.CharField(max_length=200) # Descripción de la tarea
    completed = models.BooleanField(default=False) # ¿Hecha o pendiente?
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title