from django.db.utils import DataError
from django.shortcuts import get_object_or_404, render, redirect, get_list_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from todooo.models import Todo
from .forms import TodoForm


# Create your views here.
def home(request):
    return render(request, 'todooo/home.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todooo/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'], email = request.POST['email'])
                user.save()
                login(request, user) 
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todooo/signupuser.html', {'form':UserCreationForm(), 'error':'This username has been already taken! Please create another one.'})
        else:
            return render(request, 'todooo/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords did not match!'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todooo/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todooo/loginuser.html', {'form':AuthenticationForm(), 'error':'Passwords or Username did not match!'})
        else:
            login(request, user) 
            return redirect('currenttodos')

@login_required
def logoutuser(request):
    if request.method == 'POST':
         logout(request)
         return redirect('home')

@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todooo/createtodo.html', {'form':TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todooo/createtodo.html', {'form':TodoForm(), 'error':'Bad data passed in!'})

@login_required
def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, datecomplited__isnull=True)
    return render(request, 'todooo/currenttodos.html', {'todos':todos})

@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk = todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todooo/viewtodo.html', {'todo':todo, 'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todooo/viewtodo.html', {'todo':todo, 'form':form, 'error':'Bad data passed in!'})

@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk = todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecomplited = timezone.now()
        todo.save()
        return redirect('currenttodos')

@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk = todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')

@login_required 
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user, datecomplited__isnull=False).order_by('datecomplited')
    return render(request, 'todooo/completedtodos.html', {'todos':todos})
