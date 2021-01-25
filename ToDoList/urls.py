

from django.conf.urls import url
from django.urls import path

from ToDoList import views
from .views import SearchResultsView

urlpatterns = [
    path('search/', SearchResultsView.as_view(), name='search_results'),
    url('', views.index, name='index'),
]
