from django.urls import path

from ToDoList import views
from .views import SearchResultsView, OrderByName, OrderByDeadline, OrderByCategory

urlpatterns = [
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('name/', OrderByName.as_view(), name='name'),
    path('deadline/', OrderByDeadline.as_view(), name='deadline'),
    path('category/', OrderByCategory.as_view(), name='category'),

    path('', views.index, name='index'),
]
