

from django.conf.urls import url
from django.urls import path

from ToDoList import views
from .views import OrderByName, OrderByDays, OrderByDeadline, OrderByCategory

urlpatterns = [
    path('search/', views.search, name='search_results'),
    path('name/', OrderByName.as_view(), name='name'),
    path('days/', OrderByDays.as_view(), name='days'),
    path('deadline/', OrderByDeadline.as_view(), name='deadline'),
    path('category/', OrderByCategory.as_view(), name='category'),


    path('', views.index, name='index'),
]
