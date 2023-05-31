from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# User models that includes employee and employers
class User(AbstractUser):
    is_email_verified = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    
    # log in with email instead of username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email