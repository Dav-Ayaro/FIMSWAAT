from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
# Create your models here.



class UserAccounts(AbstractUser):
    email = models.EmailField(unique=True)
    user_id = models.UUIDField(default=uuid.uuid4, unique=True)