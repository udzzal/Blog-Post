from django.db import models
from user_profile.models import User
from django.utils.text import slugify
from PIL import Image
# Create your models here.

class Catagory(models.Model):
    titel=models.CharField(max_length=250,unique=True)
    slug=models.SlugField(null=True,blank=True)
    created_date=models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.titel
    
    def save(self,*args, **kwargs):
        self.slug=slugify(self.titel)
        super().save(*args, **kwargs)
        

class Tag(models.Model):
    titel=models.CharField(max_length=250,unique=True)
    slug=models.SlugField(null=True,blank=True)
    created_date=models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.titel
    
    def save(self,*args, **kwargs):
        self.slug=slugify(self.titel)
        super().save(*args, **kwargs)
    

class Blog(models.Model):
    user=models.ForeignKey(User,related_name='user_blog',on_delete=models.CASCADE)
    
    catagory=models.ForeignKey(Catagory,
                               related_name='catagory_blog',
                               on_delete=models.CASCADE)
    
    tags=models.ManyToManyField(Tag,related_name='tag_blog',
                                blank=True)
    
    likes=models.ManyToManyField(User,
                                        related_name='user_likes',blank=True)
    
    titel=models.CharField(max_length=250)
    
    slug=models.SlugField(null=True,blank=True)
    
    banner=models.ImageField(upload_to='blog_banner')
    
    description=models.TextField()
    
    created_date=models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.titel
    
    def save(self,*args, **kwargs):
        self.slug=slugify(self.titel)
        super().save(*args, **kwargs)
        
    # def save(self,*args, **kwargs):
         
    #     image=Image.open(self.banner.path)
    #     if image.height > 500 or image.width > 500:
    #         output_size=(400,300) 
    #         image.thumbnail(output_size)
    #         image.save(self.banner.path) 
    #         super().save(*args, **kwargs)
            
   
   
class Comment(models.Model):
    user=models.ForeignKey(User,related_name='user_comment', on_delete=models.CASCADE)
    blog=models.ForeignKey(Blog,related_name='blog_comment',on_delete=models.CASCADE)
    text=models.TextField()
    created_date=models.DateField(auto_now_add=True)
    
    
    def __str__(self):
        return self.text
 
 
class Replay(models.Model):
    user=models.ForeignKey(User,
                           related_name='blog_replay', on_delete=models.CASCADE)
    
    comment=models.ForeignKey(Comment,related_name='blog_comment_replay',
                              on_delete=models.CASCADE)
    
    text=models.TextField()
    
    created_date=models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.text
    
     



     