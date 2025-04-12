from django.shortcuts import redirect, render
from django.http import HttpResponse

from .models import User, Task, UserTasks
from .forms import UserForm, TaskForm



def index(request):
    context = {}
    context['user_list'] = User.objects.all()
    context['task_list'] = Task.objects.all()
    return render(request, 'usertasks/index.html', context)

def detail(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, 'usertasks/detail.html', {'user':user})


def task(request):
    task_list = Task.objects.all()
    context = {
        'task_list':task_list
    }
    return render(request, 'usertasks/task.html', context) 

def task_detail(request, task_id):
    task = Task.objects.get(id=task_id)
    return render(request, 'usertasks/task_detail.html', {'task':task}) 

def add_user(request):
    if request.method == 'POST':
        name = request.POST.get('name',)
        email = request.POST.get('email',)
        manager = request.POST.get('manager',)
        photo_image = request.POST.get('photo_image',)
        tasks = request.POST.get('tasks',)
        is_staff = request.POST.get('is_staff',)
        is_active = request.POST.get('is_active',)
        user = User(name=name,email=email, manager=manager,photo_image=photo_image, tasks=tasks, is_staff=is_staff, is_active=is_active)
        user.save()
    return render(request, 'usertasks/add_user.html')

def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title',)
        desc = request.POST.get('desc',)
        status = request.POST.get('status',)
        start_date = request.POST.get('start_date',)
        end_date = request.POST.get('end_date',)
        completed = request.POST.get('completed',)
        assigned_users = request.POST.get('assigned_users',)
        task = Task(title=title,desc=desc, status=status,
                    start_date=start_date,end_date=end_date,completed=completed,assigned_users=assigned_users)
        task.save()
    return render(request, 'usertasks/add_task.html')

def update_user(request, id):
    user = User.objects.get(id=id)
    form = UserForm(request.POST or None, request.FILES, instance=user)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request, 'usertasks/edit.html', {'form':form, 'user':user})


def update_task(request, id):
    task = Task.objects.get(id=id)
    form = TaskForm(request.POST or None, request.FILES, instance=task)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request, 'usertasks/edit_task.html', {'form':form, 'task':task})

def delete_user(request, id):
    if request.method == 'POST':
        user = User.objects.get(id=id)
        user.delete()
        return redirect('/')
    return render(request, 'usertasks/delete.html')

def delete_task(request, id):
    if request.method == 'POST':
        task = Task.objects.get(id=id)
        task.delete()
        return redirect('/')
    return render(request, 'usertasks/delete.html')




      