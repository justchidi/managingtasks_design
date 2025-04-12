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
        

