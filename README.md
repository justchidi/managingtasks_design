# managingtasks_design
High-level design for a full-stack web application for managing user tasks, using a python-based web server. 
# Managingtasks Design
# Project Name: managingtasks
# App name: usertasks
# App Design steps:

# (1.) Models(models.py:)
	from django.db import models
	from django.contrib.auth.models import AbstractBaseUser
	from django.contrib.auth.models import BaseUserManager
	from django.contrib.auth.models import PermissionsMixin


	# Create your models here.    
	class UserManager(BaseUserManager):
		def create_user(self, email, name, password=None):
			if not email:
				raise ValueError('Email must be set!')
			users = self.model(email=email, name=name)
			users.set_password(password)
			users.save(using=self._db)
			return users

		def create_superuser(self, email, name, password):
			users = self.create_user(email, name, password)
			users.is_superuser = True
			users.is_staff = True
			users.is_active = True
			users.save(using=self._db)
			return users
			

		def get_by_natural_key(self, email_):
			return self.get(email=email_)
		

	class User(AbstractBaseUser, PermissionsMixin):
		def __str__(self):
			return self.email
		name = models.CharField(max_length=100, blank=True)
		email = models.EmailField(('email address'), unique=True)
		manager = models.CharField(max_length=100)
		photo_image = models.ImageField(default='default.jpg',upload_to='photo_images/')
		tasks = models.CharField(max_length=100, blank=True, null=True)
		is_staff = models.BooleanField(default=False)
		is_active = models.BooleanField(default=True)

		objects = UserManager()

		USERNAME_FIELD = ('email')
		REQUIRED_FIELDS = ['name']

		def get_by_natural_key(self, email_):
			return self.get(email=email_)
		
		@property
		def task_title(self):
			return self.task.title
		
		@property
		def is_anonymous(self):
			return False
		
		@property
		def is_authenticated(self):
			return False

	   
	class Task(models.Model):
		def __str__(self):
			return self.title  
		title = models.CharField(max_length=200, help_text='taskname', blank=True)
		desc = models.CharField(max_length=100, blank=True, null=True)
		status = models.CharField(max_length=100)
		start_date = models.CharField(max_length=100, blank=True, null=True)
		end_date = models.CharField(max_length=100, blank=True, null=True)
		completed = models.BooleanField(default=False)
		assigned_users = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)

		@property
		def user_name(self):
			return self.user.name
	class UserTasks(models.Model):
		tasks = models.ForeignKey(Task, on_delete=models.DO_NOTHING)
		users = models.ManyToManyField(User)
		
		
		
# (2.) Forms(forms.py)
	from django import forms
	from .models import User, Task

	class UserForm(forms.ModelForm):
		class Meta:
			model = User
			# fields = [ 'name', 'password', 'email', 'manager', 'tasks', 'photo_image']
			fields = [ 'name',  'email', 'manager', 'tasks', 'photo_image', 'is_staff', 'is_active']

	class TaskForm(forms.ModelForm):
		class Meta:
			model = Task
			fields = ['title', 'desc', 'status', 'start_date', 'end_date','completed','assigned_users']

# (3.) Views(views.py)
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

# (4.) User html templates files: ("\usertasks\templates\usertasks")
# -(a.) template 1(base.html):
	{% load static %}
	<!DOCTYPE html>
	<html lang="en">
	  <head>
		<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
		<link rel="stylesheet" href="{% static 'usertasks/style.css'%}">
		<title>My Website</title>

	  </head>
	  <body>
		<nav class="navbar navbar-dark bg-dark">
			<a class="navbar-brand" href="#">
				Managing User Tasks
			</a>
		</nav>
		{% block body %}

		{% endblock%}

	  </body>
	</html>
	
# -(b.) template 2(index.html):
	{%  extends 'usertasks/base.html' %}
	{% block body%}
	<h3>Users Main Page<span class="badge badge-secondary"></span></h3>
	<div class="container">
		<div class="row">
			{% for user in user_list %}
			<div class="col-md-2">
				<div class="card">
					<img src="{{user.photo_image.url}}" class="card-img-top" alt="">
					<div class="card_body">
						<h5 class="card-title">{{user.name}} </h5>

							{% if user.tasks %}

							{% for task in task_list %}
								{% if user.tasks == task.title %}

									<a href="task/{{task.id}}"> {{user.tasks}}</a> <br> 

								{% endif %}
							
							{% endfor %}

							{% else %}
								This user has no task.
							{% endif %}
						 
						<a class="btn btn-warning" href="{%  url 'usertasks:detail' user.id %}">View Details</a> 
					</div>
				</div>
			</div>
			{% endfor%}
		</div>
	</div>
	{% endblock %}
	
# -(c.) template 3(detail.html):
	{%  extends 'usertasks/base.html' %}
	{% block body%}
	<h3>User Detail Page<span class="badge badge-secondary"></span></h3>
	<div class="container">

		<div class="row">
			<div class="col-md-6">
				<img width="300" height="300" src="{{user.photo_image.url}}">
			</div>

			<div class="col-md-6">
				<h2>{{user.name}}</h2>
				<h6>{{user.email}}</h6>
				<h6>{{user.manager}}</h6>
				<h6>{{user.tasks}}</h6> <br>
				<!-- <h6>{{user.is_staff}}</h6> <br>
				<h6>{{user.is_active}}</h6> <br> -->
				<a class="btn btn-warning" href="{% url 'usertasks:update_user' user.id %}">Update</a>
				<a class="btn btn-danger" href="{% url 'usertasks:delete_user' user.id %}">Delete</a>

			</div>

		</div>

	</div>
	{% endblock %}
	
# -(d.) template 4(add_user.html) for adding new user form.
	<form method="POST" enctype="multipart/form-data">
    {% csrf_token %}
    <input type="text" name="name" id="name" placeholder="Enter name of user">
    <input type="text" name="email" id="email" placeholder="Enter email address">
    <input type="text" name="manager" id="manager" placeholder="Enter user's manager">
    <input type="text" name="tasks" id="tasks" placeholder="Enter user's tasks">
    <input type="file" name="photo_image" id="photo_image">
    <input type="submit" name="" id="">
	</form>

# -(e.) template 5(edit.html) for user updates function.
	<form method="POST" enctype="multipart/form-data">
    {% csrf_token%}
    <h3>User Update Page<span class="badge badge-secondary"></span></h3>
    {{form.as_p}}
    <input type="submit" name="" id="">
	</form>

# -(f.) template 6(delete.html) for deleting user function.
	<form method="POST">
    {% csrf_token %}
    Are you sure you want to delete this user?
    <input type="submit">
	</form>

# (5.) Task html templates files: 
# -(a.) template 1(task.html):
	{%  extends 'usertasks/base.html' %}
	{% block body%}
		<h3>Tasks Main Page<span class="badge badge-secondary"></span></h3>
	<div class="container">
		<div class="row">
			{% for task in task_list %}
			<div class="col-md-3">
				<div class="card">
					<div class="card_body">
						<h5 class="card-title">{{task.title}} </h5>
						<p class="card_text">{{task.desc}}</p>
						<a class="btn btn-warning" href="{%  url 'usertasks:task_detail' task.id %}">View Details</a> 
					</div>
				</div>
			</div>
			{% endfor%}
		</div>
	</div>
	{% endblock %}
	
 # -(b.) template 2(task_detail.html):
	{%  extends 'usertasks/base.html' %}
	{% block body%}
	<h3>Task Detail Page<span class="badge badge-secondary"></span></h3>

	<h2>{{task.title}}</h2>
	<h4>{{task.desc}}</h4>
	<h6>{{task.status}}</h6>
	<h6>{{task.start_date}}</h6>
	<h6>{{task.end_date}}</h6>
	<h6>{{task.completed}}</h6> 
	<h6>{{task.assigned_user}}</h6><br>

	<a class="btn btn-warning" href="{% url 'usertasks:update_task' task.id %}">Update</a>
	<a class="btn btn-danger" href="{% url 'usertasks:delete_task' task.id %}">Delete</a>
	 
	{% endblock %}
	
#-(c.) template 3(add_task.html):
	<form method="POST" enctype="multipart/form-data">
    {% csrf_token %}
    <input type="text" name="title" id="title" placeholder="Enter task title ">
    <input type="text" name="desc" id="desc" placeholder="Enter description">
    <input type="text" name="status" id="status" placeholder="Enter task status">
    <input type="text" name="start_date" id="start_date" placeholder="Enter task start date">
    <input type="text" name="end_date" id="end_date" placeholder="Enter task end date">
    <input type="text" name="completed" id="completed" placeholder="Enter task end date">
    <input type="text" name="assigned_user" id="assigned_user" placeholder="Enter assigned user">
    <input type="submit" name="" id="">
	</form>
	
	
	

# -(d.) template 4(edit_task.html):
	<form method="POST" enctype="multipart/form-data">
    {% csrf_token%}
    <h3>Task Update Page<span class="badge badge-secondary"></span></h3>
    {{form.as_p}}
    <input type="submit" name="" id="">
	</form>
	
	
# -(e.) template 5(delete_task.html):
	<form method="POST">
    {% csrf_token %}
    Are you sure you want to delete this task?
    <input type="submit">
	</form>
	

# (6.) Urls(urls.py)
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
	

# (7.) Note: static path ("\usertasks\static\usertasks") for background color scheme, however currently disabled.
	/* body{
		background-color: aqua;

	} */
	
#(8.) Note: media path ("managingtasks\media") for default image and other photo images ("managingtasks\media\photo_images")
	(a.) default.jpg
	(b.) photo images:
		- image1.jpg
		- etc.,

# (9.) Project(managingtasks) level files.
# -(a.) URL path(urls.py)
	from django.contrib import admin
	from django.urls import path, include
	from usertasks import views
	from .import settings
	from django.conf.urls.static import static

	urlpatterns = [
		path('admin/', admin.site.urls),
		path('', include('usertasks.urls')),
	]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# (10.) Project settings (settings.py):
# (a.) App(usertasks) added to "INSTALLED_APPS" array.
	-INSTALLED_APPS = [
		'usertasks',
		'django.contrib.postgres',
		'django.contrib.admin',
		'django.contrib.auth',
		'django.contrib.contenttypes',
		'django.contrib.sessions',
		'django.contrib.messages',
		'django.contrib.staticfiles',
	]
	
# (b.) other configurations added to settings are as follows:
	AUTH_USER_MODEL = 'usertasks.User'
	STATIC_URL = '/static/'
	MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
	MEDIA_URL = '/media/'
	SILENCED_SYSTEM_CHECKS = ["auth.E003",  ]

# (c.) Backed database used is "db.sqlite3":
	DATABASES = {
     'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
