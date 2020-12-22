import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from apps.core.forms import ChangePasswordForm

# import models
from .models import Userprofile

@login_required
def userprofile(request):
  return render(request, 'userprofile.html')

@login_required
def profile_settings(request):
  if request.method == 'POST':
  #get from values
    first_name = request.POST.get('first_name', '')
    last_name = request.POST.get('last_name', '')
    username = request.POST.get('username', '')
    email = request.POST.get('email', '')

    user = request.user

    if username != request.user.username:
      usernames = User.objects.filter(username=username)

      if len(usernames):
        messages.error(request, 'That Username Already Exist!')
        return redirect('userprofile')
      else:
        user.username = username

    if email != request.user.email:
      useremails = User.objects.filter(email=email)
      
      if len(useremails):
        messages.error(request, 'That Email Already Exist!')
        return redirect('userprofile')
      else:
        user.email = email
    else:    
      user.first_name = first_name
      user.last_name = last_name
      user.save()

    #   user.userprofile.plan = plan
    #   user.userprofile.save() 

      messages.success(request, 'Profile Has Been Updated!')
      return redirect('userprofile')
  else:
    return render(request, 'userprofile.html')


def changePass(request):
  if request.method == 'POST':
    form = PasswordChangeForm(request.POST)
    if form.is_valid():
      user = form.save()
      # user.email = user.username
      user.save()
      messages.success(request, 'Password Has Been Updated')
      return redirect('userprofile')
  else:
    form = PasswordChangeForm()
  return render(request, 'userprofile.html', {'form': form}) 