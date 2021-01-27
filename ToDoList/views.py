from abc import ABC, abstractmethod
from datetime import date, datetime

from django.db.models import Q
from django.db.models.functions import Lower
from django.forms import forms
from django.shortcuts import render, redirect
from django.views.generic import ListView

from ToDoList.models import *


# Create your views here.

class AbstractClass(ABC, ListView):
    model = Task
    template_name = 'index.html'

    @abstractmethod
    def get_queryset(self):
        pass


class OrderByName(AbstractClass):
    def get_queryset(self):
        return Task.objects.all().order_by(Lower('task_name'))


class OrderByDeadline(AbstractClass):
    def get_queryset(self):
        return Task.objects.all().order_by('deadline_date')


class OrderByCategory(AbstractClass):
    def get_queryset(self):
        return Task.objects.all().order_by('category')


class SearchResultsView(AbstractClass):
    def get_queryset(self):
        return Task.objects.filter(Q(task_name__icontains=self.request.GET.get('query')))


def index(request):
    tasks = Task.objects.all()
    categories = Category.objects.all()
    if not categories:
        create_data()
        # pass
    if request.method == "POST":
        if "taskAdd" in request.POST:
            task_name = request.POST["task_name"]
            category_name = request.POST["category_name"]
            deadline_date = str(request.POST["deadline_date"])

            y2, m2, d2 = [int(x) for x in deadline_date.split('-')]
            if date(y2, m2, d2) < date.today():
                raise forms.ValidationError(message='Deadline date cannot be in past!')

            description = request.POST["description"]
            date_format = "%Y/%m/%d"
            time_interval = int(abs((datetime.strptime(date.today().strftime("%Y/%m/%d"),
                                                       date_format) - datetime.strptime(deadline_date.replace('-', '/'),
                                                                                        date_format)).days))

            Todo = Task(task_name=task_name, description=description, deadline_date=deadline_date,
                        time_interval=time_interval,
                        category=Category.objects.get(category_name=category_name))
            Todo.save()
            return redirect("/")

        if "taskDelete" in request.POST:
            tasks_to_delete = request.POST.getlist('checkbox', False)
            for task_to_delete in tasks_to_delete:
                todo = Task.objects.get(id=int(task_to_delete))
                todo.delete()

    return render(request, "index.html", {"object_list": tasks, "categories": categories})


def create_data():
    names = ["Study", "Work", "Family", "Sport", "Personal", "Friends", "Shopping", "Test", "General", "Other"]
    for name in range(len(names)):
        Category.objects.create(category_name=names[name])
