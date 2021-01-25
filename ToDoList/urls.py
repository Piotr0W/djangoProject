from django.conf.urls import url

from ToDoList import views

urlpatterns = [
    url('', views.index, name='index'),
]
