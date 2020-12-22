
from django.urls import path
from .views import dashboard, settings
from apps.userprofile.views import userprofile, profile_settings, changePass

urlpatterns = [
    # Admin panel page urls
    path('', dashboard, name='dashboard'),
    path('settings', settings, name='settings'),
    path('userprofile', userprofile, name='userprofile'),
    path('profile_settings', profile_settings, name='profile_settings'),
    path('changePass', changePass, name='changePass'),



    # Admin panel apis

]
