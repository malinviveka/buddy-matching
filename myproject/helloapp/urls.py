# helloapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/save_entry/', views.save_entry, name='save_entry'),
    path('api/get_entries/', views.get_entries, name='get_entries'),
    path('', views.index, name='index'),
]