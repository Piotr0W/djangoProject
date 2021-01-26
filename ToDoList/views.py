from __future__ import unicode_literals

from datetime import date, datetime

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.db.models.functions import Lower
from django.forms import forms
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.urls import resolve
from ToDoList.models import *

# Upewnić się, że szukanie działa poprawnie i przycisk powrotu do menu
# Zrobić filtrowanie na razie min po jednej kolumnie
# Poprawić dobre wyświetlanie tabeli

# Create your views here.
def search(request):
    return Task.objects.filter(Q(task_name__icontains=request.GET.get('q')))

class OrderByName(ListView):
    model = Task
    template_name = 'index.html'
    def get_queryset(self):
        current_url = resolve(self.request.path_info).url_name
        print(current_url)
        if "name" in str(current_url):
            print("Haha")
            return Task.objects.order_by('task_name').reverse()
        return Task.objects.order_by('task_name')


class OrderByDays(ListView):
    model = Task
    template_name = 'index.html'

    def get_queryset(self):
        current_url = resolve(self.request.path_info).url_name
        if "days" in str(current_url):
            return Task.objects.order_by('time_interval').reverse()
        return Task.objects.order_by('time_interval')

class OrderByDeadline(ListView):
    model = Task
    template_name = 'index.html'

    def get_queryset(self):
        current_url = resolve(self.request.path_info).url_name
        if "deadline" in str(current_url):
            return Task.objects.order_by('deadline_date').reverse()
        return Task.objects.order_by('deadline_date')


class OrderByCategory(ListView):
    model = Task
    template_name = 'index.html'

    def get_queryset(self):
        current_url = resolve(self.request.path_info).url_name
        if "category" in str(current_url):
            return Task.objects.order_by('category').reverse()
        return Task.objects.order_by('category')



def index(request):
    template_name = 'index.html'
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

    return render(request, "index.html", {"tasks": tasks, "categories": categories})


def company_index(request):
    order_by = request.GET.get('order_by')
    direction = request.GET.get('direction')
    ordering = Lower(order_by)
    if direction == 'desc':
        ordering = '-{}'.format(ordering)
    companies = Task.objects.all().order_by(ordering)

    paginator = Paginator(companies, 10)
    page = request.GET.get('page')
    try:
        all_companies = paginator.page(page)
    except PageNotAnInteger:
        all_companies = paginator.page(1)
    except EmptyPage:
        all_companies = paginator.page(paginator.num_pages)

    return render(request, 'index.html',
                  {'tasks': all_companies,
                   'order_by': order_by, 'direction': direction})


def create_data():
    names = ["Study", "Work", "Family", "Sport", "Personal", "Friends", "Shopping", "General", "Other", "Test"]
    for name in range(len(names)):
        Category.objects.create(category_name=names[name])


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
