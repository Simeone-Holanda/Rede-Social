from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    
    bio = models.TextField(max_length=150)
    foto = models.ImageField(blank=True,upload_to='foto/%y/%m')
    