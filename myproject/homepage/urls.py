
from django.urls import path
from . import views

urlpatterns = [
    path('cadmin/edit_homepage_text/', views.edit_homepage_text, name='edit_homepage_text'),
]