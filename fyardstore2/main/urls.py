# from urllib.parse import urlparse
from xml.etree.ElementInclude import include
from django.urls import path, include
from . import views

app_name = 'homepage'

urlpatterns = [
    path('', views.index, name='home'),
]