
from django.urls import path
# from . import views
from .views import about, contact, membership, home
urlpatterns = [
    # website page urls
    path('', home, name='frontpage'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('membership/', membership, name='membership'),

    # website apis

]
