from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.forms import UserCreationForm
# from .forms import CreateUserForm
from django.contrib.auth.models import User

from apps.userprofile.models import Userprofile


def frontpage(request):
  return render(request, 'website/frontpage.html')

def register(request):
  if request.method == 'POST':
    form = UserCreationForm(request.POST)

    if form.is_valid():
      user = form.save()
      user.email = user.username
      user.save()

      userprofile = Userprofile.objects.create(user=user)
      messages.success(request, 'You Are Registered And Can Log In!')
      return redirect('login')
  else:
    form = UserCreationForm()
    
  return render(request, 'access/register.html', {'form': form}) 

def login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(username=username, password=password)

    if user is not None:
      auth.login(request, user)
      messages.success(request, 'You Are Now Logged In!')
      return redirect('dashboard')
    else:
      messages.error(request, 'Invalid Username Or Password!')
      return redirect('login')
  else:
    return render(request, 'access/login.html')

def logout(request):
  if request.method == 'POST':
    auth.logout(request)
    messages.success(request, 'You Are Now Logged Out!')
    return redirect('frontpage')

  return render(request, 'access/register.html')

