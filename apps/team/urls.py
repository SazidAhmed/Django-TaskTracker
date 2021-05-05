
from django.urls import path
from .views import teamAdd, teamList, teamDetails, teamEdit, activeTeamEdit, activate_team, deleteTeam, invite, accept_invitation, plans

#name Space
app_name = 'team'

urlpatterns = [
    path('teamAdd/', teamAdd, name='teamAdd'),
    path('teamList/', teamList, name='teamList'),
    path('teamDetails/<int:team_id>/', teamDetails, name='teamDetails'),
    path('activate_team/<int:team_id>/', activate_team, name='activate_team'),

    path('activeTeamEdit/', activeTeamEdit, name='activeTeamEdit'),
    path('teamEdit/<int:team_id>/', teamEdit, name='teamEdit'),
    path('deleteTeam/<int:team_id>/', deleteTeam, name='deleteTeam'),

    path('invite/', invite, name='invite'),
    path('accept_invitation/', accept_invitation, name='accept_invitation'),

    path('plans/', plans, name='plans'),
]