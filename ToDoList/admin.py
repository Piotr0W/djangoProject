# from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from ToDoList import models


class ToDoListAdmin(admin.ModelAdmin):
    list_display = ("task_name", "description", "deadline_date")


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("category_name",)


admin.site.register(models.Task, ToDoListAdmin)
admin.site.register(models.Category, CategoryAdmin)
