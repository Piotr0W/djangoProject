from django.db import models
from django.utils import timezone

# Create your models here.

MAX_LENGTH = 256


class Category(models.Model):
    objects = models.Manager()
    category_name = models.CharField(max_length=MAX_LENGTH)

    class Meta:
        verbose_name = ("Category")
        verbose_name_plural = ("Categories")

    def __str__(self):
        return self.category_name


class Task(models.Model):
    objects = models.Manager()
    task_name = models.CharField(max_length=MAX_LENGTH)
    description = models.TextField(blank=True)
    created_at = models.DateField(default=timezone.now().strftime("%Y-%m-%d"))
    deadline_date = models.DateField(default=timezone.now().strftime("%Y-%m-%d"))
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.task_name
