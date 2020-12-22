from django.shortcuts import render, redirect
from django.contrib import messages, auth
# from django.contrib.auth.forms import UserCreationForm
# from .forms import CreateUserForm
from django.contrib.auth.models import User

from apps.userprofile.models import Userprofile


def frontpage(request):
  return render(request, 'website/frontpage.html')

def register(request):
  if request.method == 'POST':
    #get from values
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password1']
    password2 = request.POST['password2']

    #validation
    if password == password2:
      #check username
      if User.objects.filter(username=username).exists():
        messages.error(request, 'That Username Is Taken!')
        return redirect('register')
      else:
        if User.objects.filter(email=email).exists():
          messages.error(request, 'That Email Is Being Used!')
          return redirect('register')
        else:
          #save user
          user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
          #login after register
          # auth.login(request, user)
          # messages.success(request, 'You Are Logged In!')
          # return redirect('dashboard')
          user.save()
          messages.success(request, 'You Are Now Registered And Can Log In!')
          return redirect('login')

    else:
      messages.error(request, 'Password Do No Matched!')
      return redirect('register')
  else:
    return render(request, 'access/register.html')


# def register(request):
#   if request.method == 'POST':
#     form = UserCreationForm(request.POST)
#     if form.is_valid():
#       user = form.save()
#       # user.email = user.username
#       user.save()
#       userprofile = Userprofile.objects.create(user=user)
#       messages.success(request, 'You Are Registered And Can Log In!')
#       return redirect('login')
#   else:
#     form = UserCreationForm()
#   return render(request, 'access/register.html', {'form': form}) 

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

