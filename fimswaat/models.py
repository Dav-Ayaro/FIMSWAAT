from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
import uuid
from django.contrib.auth.models import Group


department = [
    'department_of_ICT',
    'department_of_Business_and_Accounting',
    'department_of_Public_Administration_And_Management',
    'department_of_Law_Social_Science'
]




class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class UserAccounts(AbstractUser):
    email = models.EmailField(unique=True)
    user_id = models.UUIDField(default=uuid.uuid4, unique=True)

    def __str__(self):
        return self.username

class Registration(models.Model):
    user = models.ForeignKey(UserAccounts, on_delete=models.CASCADE)
    fullName = models.CharField(max_length=255)
    department = models.CharField(max_length=100)
    empId = models.CharField(max_length=15)
    officeName = models.CharField(max_length=255)
    officeCode = models.CharField(max_length=10)


class Location(models.Model):
    location = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    gps_coordinates = models.CharField(max_length=100)
    item = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    year = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    condition = models.CharField(max_length=100, choices=[
        ('GOOD', 'Good'),
        ('SERVE', 'Serve'),
        ('UNSERVE', 'Unserve'),
    ])

    def __str__(self):
        return self.item

        
class Product(models.Model):
    product_id = models.CharField(max_length=100)
    barcode = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    quantity = models.IntegerField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    vendor = models.CharField(max_length=100)

    def __str__(self):
        return self.description

class Transaction(models.Model):
    transaction_id = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    user_id = models.CharField(max_length=100)

    def __str__(self):
        return self.transaction_id
