from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
# from django.contrib.auth.backends import ModelBackend
# from django.contrib.auth import get_user_model
# Create your models here.


department = [
    'department_of_a',
    'department_of_b',
    'department_of_c',
    'department_of_d',
]


# class EmailBackend(ModelBackend):
#     def authenticate(self, request, email=None, password=None, **kwargs):
#         UserModel = get_user_model()
#         try:
#             user = UserModel.objects.get(email=email)
#         except UserModel.DoesNotExist:
#             return None
#         else:
#             if user.check_password(password):
#                 return user
#         return None




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

