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

