from __future__ import unicode_literals
from datetime import date
from random import random
from datetime import datetime

from django.db.models import DateField
# Create your views here.
from django.forms import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError

import ToDoList.models


# Create your views here.


def index(request):
    tasks = ToDoList.models.Task.objects.all()
    categories = ToDoList.models.Category.objects.all()


    if request.method == "POST":
        if "taskAdd" in request.POST:
            task_name = request.POST["task_name"]
            category_name = request.POST["category_name"]

            try:
                deadline_date = str(request.POST["deadline_date"])
            except MultiValueDictKeyError:
                deadline_date = DateField(auto_now=True)

            description = request.POST["description"]

            Todo = ToDoList.models.Task(task_name=task_name, description=description, deadline_date=deadline_date,
                                        category=ToDoList.models.Category.objects.get(category_name=category_name))
            Todo.save()
            return redirect("/")

        if "taskDelete" in request.POST:
            tasks_to_delete = request.POST.getlist('checkbox', False)
            for task_to_delete in tasks_to_delete:
                todo = ToDoList.models.Task.objects.get(id=int(task_to_delete))
                todo.delete()

    return render(request, "index.html", {"tasks": tasks, "categories": categories})