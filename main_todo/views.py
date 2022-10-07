from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User 
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError


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
    return render(request, 'main_todo/current_todo.html', {})

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


def home(request):
    return render(request, 'main_todo/home.html', {})
# Create your views here.
