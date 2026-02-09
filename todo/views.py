from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import TaskList, Task

# Registro de nuevos usuarios
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# Ver y crear listas (Solo si estás logueado)
@login_required
def index(request):
    lists = TaskList.objects.filter(user=request.user)
    if request.method == 'POST':
        name = request.POST.get('name')
        TaskList.objects.create(user=request.user, name=name)
        return redirect('index')
    return render(request, 'todo/index.html', {'lists': lists})

# Borrar una lista entera
@login_required
def delete_list(request, list_id):
    list_obj = get_object_or_404(TaskList, id=list_id, user=request.user)
    list_obj.delete()
    return redirect('index')

# Ver y añadir tareas a una lista específica
@login_required
def task_detail(request, list_id):
    list_obj = get_object_or_404(TaskList, id=list_id, user=request.user)
    tasks = list_obj.tasks.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        Task.objects.create(task_list=list_obj, title=title)
        return redirect('task_detail', list_id=list_id)
    return render(request, 'todo/tasks.html', {'list': list_obj, 'tasks': tasks})

# Marcar como completada o pendiente
@login_required
def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, task_list__user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('task_detail', list_id=task.task_list.id)

# Borrar una tarea individual
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, task_list__user=request.user)
    list_id = task.task_list.id
    task.delete()
    return redirect('task_detail', list_id=list_id)