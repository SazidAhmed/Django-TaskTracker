# Import python
import random
from datetime import datetime

# Import Django
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

# Import models
from .models import Team, Invitation

# Import helpers
from .utilities import send_invitation, send_invitation_accepted

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

# from user profile team list
@login_required
def teamList(request):
    teamList = request.user.teams.exclude(pk=request.user.userprofile.active_team_id)
    return render(request, 'teamList.html', {'teamList': teamList})

# Team Details
@login_required
def teamDetails(request, team_id):
    team = get_object_or_404(Team, pk=team_id, status=Team.ACTIVE, members__in=[request.user])
    invitations = team.invitations.filter(status=Invitation.INVITED)
    return render(request, 'teamDetails.html', {'team': team, 'invitations':invitations})

# Team Activate
@login_required
def activate_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id, status=Team.ACTIVE, members__in=[request.user])
    userprofile = request.user.userprofile
    userprofile.active_team_id = team.id
    userprofile.save()

    messages.info(request, 'The team was activated')
    # return redirect('team:teamDetails', team_id=team.id)
    return redirect('team:teamList')

# Team Delete
@login_required
def deleteTeam(request, team_id):
    team = get_object_or_404(Team, pk=team_id, status=Team.ACTIVE, members__in=[request.user])
    team.delete()

    messages.info(request, 'Team is deleted')
    return redirect('team:teamList')

# Email Invitation
@login_required
def invite(request):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)

    if request.method == 'POST':
        email = request.POST.get('email')

        if email:
            invitations = Invitation.objects.filter(team=team, email=email)

            if not invitations:
                code = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz123456789') for i in range(4))
                invitation = Invitation.objects.create(team=team, email=email, code=code)

                messages.info(request, 'The user was invited')

                send_invitation(email, code, team)

                return redirect('team:teamDetails', team_id=team.id)
            else:
                messages.info(request, 'The users has already been invited')

    return render(request, 'email/invite.html', {'team': team})

# Email Invitation
@login_required
def accept_invitation(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        invitations = Invitation.objects.filter(code=code, email=request.user.email)
        if invitations:
            invitation = invitations[0]
            invitation.status=Invitation.ACCEPTED
            invitation.save()

            #add in team members
            team = invitation.team
            team.members.add(request.user)
            team.save()

            #update userprofile
            userprofile = request.user.userprofile
            userprofile.activate_team_id = team.id
            userprofile.save()

            messages.info(request, 'Invitation Has Been Accepted')

            send_invitation_accepted(team, invitation)

            return redirect('team:teamDetails', team_id=team.id)
        else:
            messages.info(request, 'Invitation Was Not Found')
    else:
        return render(request, 'email/accept_invitaion.html')


@login_required
def plans(request):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)

    context = {
        'team': team,
    }

    return render(request, 'plans.html', context)

