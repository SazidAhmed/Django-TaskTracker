import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from apps.core.forms import ChangePasswordForm
#file storage
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# import models
from .models import Userprofile
from apps.team.models import Team, Invitation

@login_required
def userprofile(request):
  teams = request.user.teams.exclude(pk=request.user.userprofile.active_team_id)
  invitations = Invitation.objects.filter(email=request.user.email, status=Invitation.INVITED)
  return render(request, 'userprofile.html', {'teams': teams, 'invitations': invitations})

@login_required
def profile_settings(request):
  if request.method == 'POST':
    #get from values
    first_name = request.POST.get('first_name', '')
    last_name = request.POST.get('last_name', '')
    username = request.POST.get('username', '')
    email = request.POST.get('email', '')

    if request.FILES:
      avatar = request.FILES['avatar']
      userprofile = request.user.userprofile
      userprofile.avatar = avatar
      userprofile.save()

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

      messages.success(request, 'Profile Has Been Updated!')
      return redirect('userprofile')

  else:
    return render(request, 'profile_settings.html')

@login_required
def accept_invitation(request):
    if request.method == 'POST':
        code = request.POST.get('code')

        invitations = Invitation.objects.filter(code=code, email=request.user.email)

        if invitations:
            invitation = invitations[0]
            invitation.status = Invitation.ACCEPTED
            invitation.save()

            team = invitation.team
            team.members.add(request.user)
            team.save()

            userprofile = request.user.userprofile
            userprofile.active_team_id = team.id
            userprofile.save()

            messages.info(request, 'Invitation accepted')

            send_invitation_accepted(team, invitation)

            return redirect('team:team', team_id=team.id)
        else:
            messages.info(request, 'Invitation was not found')
    else:
        return render(request, 'userprofile/accept_invitation.html')

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
  return render(request, 'profile_settings.html', {'form': form}) 