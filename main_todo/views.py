from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User 
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.utils import timezone
from .forms import TodoForm
from .models import Todo


def sing_up(request):
    if request.method == 'GET':
        return render(request, 'main_todo/sing_up.html', {'form':UserCreationForm() })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'])
                user.set_password(request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('current_todo')
            except IntegrityError:
                return render(request, 'main_todo/sing_up.html', {'form':UserCreationForm(), 
                                                                "error": "Имя занято" })                
        else:
            return render(request, 'main_todo/sing_up.html', {'form':UserCreationForm(), 
                                                                "error": "пароли не совподают" })

        return render(request, 'main_todo/sing_up.html', {'form':UserCreationForm() })

def current_todo(request):
    todos = Todo.objects.filter(user=request.user, date_done__isnull=True)
    return render(request, 'main_todo/current_todo.html', {'todos':todos})

def log_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def log_in(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is None: 
            return render(request, 'main_todo/log_in.html', {'form':AuthenticationForm(),
                                            "error": "Неверный логин или пароль"})
        else:
            login(request, user)
            return redirect('current_todo')

    else:
        return render(request, 'main_todo/log_in.html', {'form':AuthenticationForm()})

def createtodo(request):
    if request.method == 'GET':
        return render(request, 'main_todo/createtodo.html', {'form':TodoForm() })
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('current_todo')
        except ValueError:
            return render(request, 'main_todo/createtodo.html', {'form':TodoForm(), 'error': "не верные данные, или пользователь не авторизован!!!" })


def home(request):
    return render(request, 'main_todo/home.html', {})
# Create your views here.

def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'main_todo/viewtodo.html', {"todo":todo, "form":form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('current_todo')
        except ValueError:
            return render(request, 'main_todo/viewtodo.html', {"todo":todo, "form":form, 'error': "не верные данные" })

def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.date_done = timezone.now()
        todo.save()
        return redirect('current_todo')

def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('current_todo')