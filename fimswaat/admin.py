from django.contrib import admin

from . models import *
# Register your models here.

class UserAccountsView(admin.ModelAdmin):
    list_display = ['user_id', 'is_staff', 'is_superuser','email']

class RegistrationView(admin.ModelAdmin):
    list_display = ['fullName','department','empId','officeName','officeCode']

admin.site.register(UserAccounts, UserAccountsView)
admin.site.register(Registration, RegistrationView)