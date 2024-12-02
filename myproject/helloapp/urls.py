# helloapp/urls.py
from django.urls import path
from . import views
from .views import AccountCreationView

urlpatterns = [
    path('create-account/', AccountCreationView.as_view(), name='create_account_view'),
    path('submit-account/', views.create_account, name='create_account'),
    path('api/save_entry/', views.save_entry, name='save_entry'),
    path('api/get_entries/', views.get_entries, name='get_entries'),
    path('', views.index, name='index'),
    #path('', AccountCreationView.as_view(), name='index'),
]