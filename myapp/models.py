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
    

# File model 
class File(models.Model):
    FILE_TYPES = (
        ('pdf', 'PDF'),
        ('image', 'Image'),
        ('audio', 'Audio'),
        ('video', 'Video'),
    )
    
    title = models.CharField(max_length=100)
    description = models.TextField()
    file_type = models.CharField(max_length=10, choices=FILE_TYPES)
    file = models.FileField(upload_to='resources/')
    downloads = models.PositiveIntegerField(default=0)
    emails_sent = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    
    def downloads_count(self):
        self.downloads += 1
        self.save()

    def emails_sent_count(self):
        self.emails_sent += 1
        self.save()