from django.urls import path

from . import views

app_name = 'main'
urlpatterns = [
    path('main', views.index),
    path('', views.index, name='index'),
    path('craw', views.craw, name='craw'),
    path('list', views.list, name='list'),
]