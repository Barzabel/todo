from .models import Todo
from django.contrib.auth.models import User 
from django.forms import ModelForm


class TodoForm(ModelForm):
	class Meta:
		model = Todo
		fields = ['titel', 'memo', 'imported' ]