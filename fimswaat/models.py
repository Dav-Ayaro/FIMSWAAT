from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
# Create your models here.


department = [
    'department_of_a',
    'department_of_b',
    'department_of_c',
    'department_of_d',
]


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
