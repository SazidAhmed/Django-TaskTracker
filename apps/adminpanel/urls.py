
from django.urls import path
from .views import dashboard, settings

urlpatterns = [
    # Admin panel page urls
    path('', dashboard, name='dashboard'),
    path('settings', settings, name='settings'),



    # Admin panel apis

]
