from django.urls import path
from . views import *

urlpatterns = [
    path('', index_view, name='index_view'),
    path('admin', admin_view, name='admin_view'),
    path('manager', manager_view, name='manager_view'),
    path('login', login_view, name='login_view'),
    path('logout', logout_view, name='logout_view'),
]