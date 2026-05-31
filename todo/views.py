from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseNotAllowed
from .models import TaskList, Task

# ==========================================
# 1. AUTENTICACIÓN Y REGISTRO DE USUARIOS
# ==========================================

def register(request):
    """Registro de nuevos usuarios en la aplicación."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('lists_root') # Te manda directo a tus listas tras registrarte
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


# ==========================================
# 2. ENDPOINTS PARA LISTAS DE TAREAS
# ==========================================

@login_required
def lists_root(request):
    """
    Maneja la raíz de listas de tareas.
    GET: Visualizar todas las listas del usuario logueado.
    POST: Crear una nueva lista de tareas.
    """
    if request.method == 'GET':
        lists = TaskList.objects.filter(user=request.user)
        return render(request, 'todo/index.html', {'lists': lists})
        
    elif request.method == 'POST':
        name = request.POST.get('name')
        if name:
            TaskList.objects.create(user=request.user, name=name)
        return redirect('lists_root')
        
    return HttpResponseNotAllowed(['GET', 'POST'])


@login_required
def list_detail_api(request, list_id):
    """
    Maneja acciones específicas sobre una lista.
    DELETE: Eliminar una lista entera junto con sus tareas (on_delete=CASCADE).
    """
    list_obj = get_object_or_404(TaskList, id=list_id, user=request.user)
    
    if request.method == 'DELETE':
        list_obj.delete()
        return JsonResponse({}, status=204) # 204 No Content para borrados exitosos
        
    return HttpResponseNotAllowed(['DELETE'])


# ==========================================
# 3. ENDPOINTS PARA TAREAS INDIVIDUALES
# ==========================================

@login_required
def task_detail(request, list_id):
    """
    Maneja las tareas pertenecientes a una lista específica.
    GET: Visualizar todas las tareas de la lista.
    POST: Añadir una nueva tarea a la lista.
    """
    list_obj = get_object_or_404(TaskList, id=list_id, user=request.user)
    
    if request.method == 'GET':
        tasks = list_obj.tasks.all()
        return render(request, 'todo/tasks.html', {'list': list_obj, 'tasks': tasks})
        
    elif request.method == 'POST':
        title = request.POST.get('title')
        if title:
            Task.objects.create(task_list=list_obj, title=title)
        return redirect('task_detail', list_id=list_id)
        
    return HttpResponseNotAllowed(['GET', 'POST'])


@login_required
def task_actions_api(request, list_id, task_id):
    """
    Maneja operaciones REST directas sobre una tarea específica.
    PATCH: Cambiar el estado de completado o pendiente (Toggle).
    DELETE: Eliminar la tarea de forma individual.
    """
    # Buscamos la tarea asegurando que pertenezca a la lista correcta y al usuario logueado
    task = get_object_or_404(Task, id=task_id, task_list__id=list_id, task_list__user=request.user)
    
    if request.method == 'PATCH':
        # Alternamos el valor booleano del campo completed
        task.completed = not task.completed
        task.save()
        return JsonResponse({'completed': task.completed}, status=200) # 200 OK con el nuevo estado
        
    elif request.method == 'DELETE':
        task.delete()
        return JsonResponse({}, status=204) # 204 No Content tras eliminarla
        
    return HttpResponseNotAllowed(['PATCH', 'DELETE'])