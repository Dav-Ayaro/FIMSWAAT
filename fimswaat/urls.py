from django.urls import path
from . views import *

urlpatterns = [
    path('', admin_dash, name='admin_dash')
]