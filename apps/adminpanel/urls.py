
from django.urls import path, include
from .views import dashboard, settings, view_user
from apps.userprofile.views import userprofile, profile_settings, changePass

urlpatterns = [
    # Admin panel page urls
    path('dashboard/', dashboard, name='dashboard'),
    path('settings/', settings, name='settings'),
    path('userprofile/', userprofile, name='userprofile'),
    path('profile_settings/', profile_settings, name='profile_settings'),
    path('changePass/', changePass, name='changePass'),


    #Team Urls
    path('teams/', include('apps.team.urls')),

    #Project Urls
    path('projects/', include('apps.project.urls')),

    # User urls
    path('<int:user_id>/', view_user, name='view_user'),

]
