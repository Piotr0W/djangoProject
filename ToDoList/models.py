from django.db import models


# Create your models here.

class Category(models.Model):
    objects = models.Manager()
    pass


class Task(models.Model):
    objects = models.Manager()
    pass
