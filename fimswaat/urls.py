from django.urls import path
from . views import *
from . import views
from .views import index_view
app_name = 'fimswaat'

urlpatterns = [
    path('', views.index_view, name='index_view'),
    path('login', login_view, name='login_view'),
    path('admin', admin_view, name='admin_view'),
    path('manager/', manager_view, name='manager_view'),
    path('enrollment/<str:group_id>', enrollment_view, name='enrollment_view'),
    path('manager/settings', manager_settings_view, name='manager_settings_view'),
    path('manager/chnage_password/success', changed_view, name='changed_view'),
    path('logout', logout_view, name='logout_view'),
    path('product/<str:barcode>/', views.product_details, name='product_details'),
    path('report/', views.generate_report, name='generate_report'),
    path('location-table/', views.location_table_view, name='location_table'),
]