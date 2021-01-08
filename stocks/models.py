from django.db import models
from zinnia.models_bases.entry import AbstractEntry


class Securitie(models.Model):
    symbol = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    exchange = models.CharField(max_length=255)


class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password_hash = models.CharField(max_length=1000)
    email = models.CharField(max_length=255, unique=True)
    bio = models.CharField(max_length=2000)
    type = models.CharField(choices=(('A', 'admin'), ('C', 'common'), ('W', 'writer'),),
                            max_length=255, default=('C', 'common'))

    def __str__(self):
        return 'User: ' + self.username


class Crypto(models.Model):
    symbol = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    lookup = models.CharField(max_length=255)


class Quote(models.Model):
    quote = models.CharField(max_length=1000)
    author = models.CharField(max_length=255)


# data not moved, need to create blog class first, is article the blog id?
class Comment(models.Model):
    article = models.CharField(max_length=255)
    comment = models.CharField(max_length=1000)
    # user = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # date = register/models.TextField()
    # time = models.TextField()
    likes = models.IntegerField()


class BlogInfo(AbstractEntry):
    text = models.CharField(max_length=1000)
    brief_description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta(AbstractEntry.Meta):
        abstract = True
