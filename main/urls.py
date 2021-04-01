from django.urls import path

from . import views

from django.conf import settings
from django.conf.urls.static import static
app_name = 'main'
urlpatterns = [
    path('main', views.index),
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('calendar', views.calendar, name='calendar'),
    path('craw_list_db', views.craw_list_db, name='craw_list_db'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)