from django.db import models
from django.contrib.auth.models import User
import uuid

from django.db.models.deletion import SET_NULL

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=200,null=True,blank=True)
    username = models.CharField(max_length=200,null=True,blank=True)
    email = models.EmailField(max_length=200,null=True,blank=True)
    short_intro = models.CharField(max_length=200,null=True,blank=True)
    location = models.CharField(max_length=200,null=True,blank=True)
    bio = models.TextField(null=True,blank=True)
    profile_image = models.ImageField(null=True,blank=True,upload_to='profiles/',default="profiles/user-default.png")
    social_github = models.CharField(max_length=500,null=True,blank=True)
    social_twitter = models.CharField(max_length=500,null=True,blank=True)
    social_website = models.CharField(max_length=500,null=True,blank=True)
    social_linkedin = models.CharField(max_length=500,null=True,blank=True)
    social_facebook = models.CharField(max_length=500,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self):
        return str(self.username)

    @property
    def imageURL(self):
        try:
            url = self.profile_image.url
        except:
            url = ""
        return url

    class Meta:
        ordering = ['created']

class Skill(models.Model):
    owner = models.ForeignKey(Profile,null=True,blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False,unique=True)

    def __str__(self):
        return str(self.name)

class Message(models.Model):
    sender = models.ForeignKey(Profile,null=True,blank=True,on_delete=models.SET_NULL)
    recepient = models.ForeignKey(Profile,null=True,blank=True,on_delete=models.SET_NULL,related_name='messages')
    sender_name = models.CharField(max_length=200,null=True,blank=True)
    email = models.EmailField(max_length=200,null=True,blank=True)
    subject = models.CharField(max_length=200,null=True,blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False,unique=True)

    def __str__(self):
        return str(self.subject)

    class Meta:
        ordering = ['is_read','-created']
