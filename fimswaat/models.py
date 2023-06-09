from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
import uuid
from django.contrib.auth.models import Group


department = [
    'department_of_ICT',
    'department_of_Business_and_Accounting',
    'department_of_Public_Administration_And_Management'
    'department_of_Law_Social_Science'
]




class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class UserAccounts(AbstractUser):
    email = models.EmailField(unique=True)
    user_id = models.UUIDField(default=uuid.uuid4, unique=True)

class Registration(models.Model):
    user = models.ForeignKey(UserAccounts, on_delete=models.CASCADE)
    fullName = models.CharField(max_length=255)
    department = models.CharField(max_length=100)
    empId = models.IntegerField()
    officeName = models.CharField(max_length=255)
    officeCode = models.CharField(max_length=10)
