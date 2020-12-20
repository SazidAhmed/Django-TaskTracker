
from django.urls import path
# from . import views
from .views import about, contact
urlpatterns = [
    # website page urls
    path('', about, name='about'),
    path('contact/', contact, name='contact'),


    # website apis

]
