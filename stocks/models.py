from django.db import models
from django.contrib.auth import get_user_model
from zinnia.models_bases.entry import AbstractEntry


class Securitie(models.Model):
    symbol = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    exchange = models.CharField(max_length=255)


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='profile')
    bio = models.CharField(max_length=2000)
    type = models.CharField(choices=(('A', 'admin'), ('C', 'common'), ('W', 'writer'),),
                            max_length=255, default=('C', 'common'))

    def __str__(self):
        return 'User: ' + get_user_model().username


class Crypto(models.Model):
    symbol = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    lookup = models.CharField(max_length=255)


class Quote(models.Model):
    quote = models.CharField(max_length=1000)
    author = models.CharField(max_length=255)


class BlogInfo(AbstractEntry):
    text = models.CharField(max_length=1000)
    brief_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta(AbstractEntry.Meta):
        abstract = True


# data not moved, need to create blog class first, is article the blog id?
class Comment(models.Model):
    # blog = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name='blog_id')
    comment = models.CharField(max_length=1000)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.IntegerField()
