from django.db import models

# done
class Securities(models.Model):
    symbol = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    exchange = models.CharField(max_length=255)

# done
class Users(models.Model):
    username = models.CharField(max_length=255, unique=True)
    hash = models.CharField(max_length=1000)
    email = models.CharField(max_length=255, unique=True)

# done
class Crypto(models.Model):
    symbol = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    lookup = models.CharField(max_length=255)

# done
class Quotes(models.Model):
    quote = models.CharField(max_length=1000)
    author = models.CharField(max_length=255)

# data not moved, need to create blog class first, is article the blog id?
class Comments(models.Model):
    article = models.CharField(max_length=255)
    comment = models.CharField(max_length=1000)
    # user = models.CharField(max_length=255)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # date = models.TextField()
    # time = models.TextField()
    likes = models.IntegerField()
