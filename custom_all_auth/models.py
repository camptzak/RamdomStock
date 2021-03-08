from django.db import models
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import pre_save

User = get_user_model()


class UserProfile(models.Model):

    user = models.OneToOneField(User,  on_delete=models.CASCADE, related_name='User_Profile')
    profile_picture = models.ImageField(upload_to='profile_pictures/')
    description = models.TextField(blank=True)
    facebook_url = models.CharField(max_length=255, blank=True)
    twitter_url = models.CharField(max_length=255, blank=True)
    instagram_url = models.CharField(max_length=255, blank=True)
    website_url = models.CharField(max_length=255, blank=True)

