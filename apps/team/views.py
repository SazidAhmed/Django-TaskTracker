# Import python
from datetime import datetime

# Import Django
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

# Import models
from .models import Team


@login_required
def teamAdd(request):
    if request.method == 'POST':
        title = request.POST.get('title')

        if title:
            team = Team.objects.create(title=title, created_by=request.user)
            team.members.add(request.user)
            team.save()

            # userprofile = request.user.userprofile
            # userprofile.active_team_id = team.id
            # userprofile.save()

            return redirect('team:teamList')

    return render(request, 'teamAdd.html')

# Active team edit
@login_required
def activeTeamEdit(request):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE, members__in=[request.user])

    if request.method == 'POST':
        title = request.POST.get('title')

        if title:
            team.title = title
            team.save()

            messages.info(request, 'The changes was saved')

            return redirect('team:teamDetails', team_id=team.id)

    return render(request, 'activeTeamEdit.html', {'team': team})

# Team edit
@login_required
def teamEdit(request, team_id):
    team = get_object_or_404(Team, pk=team_id, status=Team.ACTIVE, members__in=[request.user])
    print(team.title)
    if request.method == 'POST':
        title = request.POST.get('title')

        if title:
            team.title = title
            team.save()

            messages.info(request, 'The changes was saved')
            return redirect('team:teamList')
    else:
        return render(request, 'teamEdit.html', {'team': team})

# from user profile
@login_required
def teamList(request):
    teamList = request.user.teams.exclude(pk=request.user.userprofile.active_team_id)
    return render(request, 'teamList.html', {'teamList': teamList})

# Team Details
@login_required
def teamDetails(request, team_id):
    team = get_object_or_404(Team, pk=team_id, status=Team.ACTIVE, members__in=[request.user])
    return render(request, 'teamDetails.html', {'team': team})

# Team Activate
@login_required
def activate_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id, status=Team.ACTIVE, members__in=[request.user])
    userprofile = request.user.userprofile
    userprofile.active_team_id = team.id
    userprofile.save()

    messages.info(request, 'The team was activated')
    return redirect('team:teamDetails', team_id=team.id)

# Team Delete
@login_required
def deleteTeam(request, team_id):
    team = get_object_or_404(Team, pk=team_id, status=Team.ACTIVE, members__in=[request.user])
    team.delete()

    messages.info(request, 'Team is deleted')
    return redirect('team:teamList')