from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseNotAllowed
from .models import TaskList, Task

# GET /lists/ y POST /lists/
@login_required
def lists_root(request):
    if request.method == 'GET':
        lists = TaskList.objects.filter(user=request.user)
        return render(request, 'todo/index.html', {'lists': lists})
        
    elif request.method == 'POST':
        name = request.POST.get('name')
        TaskList.objects.create(user=request.user, name=name)
        return redirect('lists_root')
        
    return HttpResponseNotAllowed(['GET', 'POST'])

# DELETE /lists/<list_id>/
@login_required
def list_detail_api(request, list_id):
    list_obj = get_object_or_404(TaskList, id=list_id, user=request.user)
    
    if request.method == 'DELETE':
        list_obj.delete()
        return JsonResponse({}, status=204) # 204 No Content (Éxito en DELETE)
        
    return HttpResponseNotAllowed(['DELETE'])

# GET /lists/<list_id>/tasks/ y POST /lists/<list_id>/tasks/
@login_required
def task_detail(request, list_id):
    list_obj = get_object_or_404(TaskList, id=list_id, user=request.user)
    
    if request.method == 'GET':
        tasks = list_obj.tasks.all()
        return render(request, 'todo/tasks.html', {'list': list_obj, 'tasks': tasks})
        
    elif request.method == 'POST':
        title = request.POST.get('title')
        Task.objects.create(task_list=list_obj, title=title)
        return redirect('task_detail', list_id=list_id)
        
    return HttpResponseNotAllowed(['GET', 'POST'])

# PATCH /lists/<list_id>/tasks/<task_id>/ y DELETE /lists/<list_id>/tasks/<task_id>/
@login_required
def task_actions_api(request, list_id, task_id):
    task = get_object_or_404(Task, id=task_id, task_list__id=list_id, task_list__user=request.user)
    
    if request.method == 'PATCH':
        # Cambiamos el estado (Toggle)
        task.completed = not task.completed
        task.save()
        return JsonResponse({'completed': task.completed}, status=200)
        
    elif request.method == 'DELETE':
        task.delete()
        return JsonResponse({}, status=204)
        
    return HttpResponseNotAllowed(['PATCH', 'DELETE'])
