from django.contrib import admin
from django.db import connection, utils
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from .models import UserAccounts, Registration, Department, Location, Product, Transaction

User = get_user_model()


class UserAccountsView(admin.ModelAdmin):
    list_display = ['username', 'is_staff', 'is_superuser', 'email']


class RegistrationView(admin.ModelAdmin):
    list_display = ['fullName', 'department', 'empId', 'officeName', 'officeCode']


class DepartmentView(admin.ModelAdmin):
    list_display = ['id', 'name']


class LocationView(admin.ModelAdmin):
    list_display = ['name', 'location', 'gps_coordinates','item', 'code', 'year', 'quantity', 'condition']


class ProductView(admin.ModelAdmin):
    list_display = ['product_id', 'barcode', 'description', 'quantity', 'location', 'price', 'vendor']


class TransactionView(admin.ModelAdmin):
    list_display = ['transaction_id', 'product', 'quantity', 'location', 'date_time', 'user_id']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        group, created = Group.objects.get_or_create(name=obj.department.name)

        if created:
            admin_user = User.objects.get(username=request.user.username)
            admin_user.groups.add(group)

        # Dynamically create some tables for the department
        table_name = f"department_{_clean_table_name(obj.name)}"
        table_sql = f"""
            CREATE TABLE {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            );
        """
        with connection.cursor() as cursor:
            try:
                cursor.execute(table_sql)
            except utils.DatabaseError as e:
                print(f"Error creating table for department {obj.name}: {str(e)}")


def _clean_table_name(name):
    valid_chars = [c if c.isalnum() else '_' for c in name]
    return ''.join(valid_chars)


admin.site.register(UserAccounts, UserAccountsView)
admin.site.register(Registration, RegistrationView)
admin.site.register(Department, DepartmentView)
admin.site.register(Location, LocationView)
admin.site.register(Product, ProductView)
admin.site.register(Transaction, TransactionView)
