from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import Mycustommannager

# Create your models here.
class User(AbstractUser):
    email=models.EmailField(max_length=200,unique=True,error_messages= {"unique":"email must be unique"})
    profile_image=models.ImageField(null=True,blank=True,upload_to='progile_img')
    
    REQUIRED_FIELDS=['email']
    objects=Mycustommannager()
    
    def __str__(self):
        return self.username
    
    def get_profile_picture(self):
        url=""
        try:
            url=self.profile_image.url
        except:
            url=""
        return url    
        


