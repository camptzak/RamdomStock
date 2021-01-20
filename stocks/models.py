from django.db import models
from zinnia.models_bases.entry import AbstractEntry


class Securitie(models.Model):
    symbol = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    exchange = models.CharField(max_length=255)


class Crypto(models.Model):
    symbol = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    lookup = models.CharField(max_length=255)


class Quote(models.Model):
    quote = models.CharField(max_length=1000)
    author = models.CharField(max_length=255)



