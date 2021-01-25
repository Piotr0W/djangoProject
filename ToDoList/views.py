from __future__ import unicode_literals

from datetime import date, datetime

# Create your views here.
from django.forms import forms
from django.shortcuts import render, redirect

import ToDoList.models


# Create your views here.


def index(request):
    tasks = ToDoList.models.Task.objects.all()
    categories = ToDoList.models.Category.objects.all()
    if not categories:
        create_data()
        # pass
    if request.method == "POST":
        if "taskAdd" in request.POST:
            task_name = request.POST["task_name"]
            category_name = request.POST["category_name"]
            deadline_date = str(request.POST["deadline_date"])

            # try:
            #     deadline_date = str(request.POST["deadline_date"])
            # except MultiValueDictKeyError:
            #     deadline_date = DateField(auto_now=True)
            y2, m2, d2 = [int(x) for x in deadline_date.split('-')]
            if date(y2, m2, d2) < date.today():
                raise forms.ValidationError(message='Deadline date cannot be in past!')

            description = request.POST["description"]


            date_format = "%Y/%m/%d"
            time_interval = int(abs((datetime.strptime(date.today().strftime("%Y/%m/%d"), date_format) - datetime.strptime(deadline_date.replace('-', '/'), date_format)).days))



            Todo = ToDoList.models.Task(task_name=task_name, description=description, deadline_date=deadline_date, time_interval=time_interval,
                                        category=ToDoList.models.Category.objects.get(category_name=category_name))
            Todo.save()
            return redirect("/")

        if "taskDelete" in request.POST:
            tasks_to_delete = request.POST.getlist('checkbox', False)
            for task_to_delete in tasks_to_delete:
                todo = ToDoList.models.Task.objects.get(id=int(task_to_delete))
                todo.delete()

    return render(request, "index.html", {"tasks": tasks, "categories": categories})


def create_data():
    names = ["Study", "Work", "Family", "Sport", "Personal", "Friends", "Shopping", "General", "Other", "Test"]
    for name in range(len(names)):
        ToDoList.models.Category.objects.create(category_name=names[name])


def calculate_diff_date(created_at, deadline_date):
    deadline_date_string = str(deadline_date)
    y2, m2, d2 = [int(x) for x in deadline_date_string.split('-')]
    d1 = date(y2, m2, d2)
    created_at_string = str(created_at)
    y2, m2, d2 = [int(x) for x in created_at_string.split('-')]
    d2 = date(y2, m2, d2)
    return d1 - d2


# def Showcal(request):
#     return render(request, "Index.html")
# def handler404(request, *args, **argv):
#     return render(request, "404.html")
