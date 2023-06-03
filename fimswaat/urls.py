from django.urls import path
from . views import *

urlpatterns = [
    path('', admin_dash, name='admin_dash'),
    path('login/',login_view, name='login_view'),
    path('user_dash', user_dash_view, name='user_dash_view'),
    path('logout/',logout_view, name='logout_view'),
]