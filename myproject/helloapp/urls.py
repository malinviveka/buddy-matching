# helloapp/urls.py
from django.urls import path, include
from . import views
from .views import AccountCreationView

urlpatterns = [
    path('create-account/', AccountCreationView.as_view(), name='create_account_view'),
    path('submit-account/', views.create_account, name='create_account'),
    path('login/', views.login_view, name='login'),
    #path('api/save_entry/', views.save_entry, name='save_entry'),
    #path('api/get_entries/', views.get_entries, name='get_entries'),
    path('logout/', views.logout_view, name='logout'),
    path('cadmin/users/', views.admin_user_list, name='admin_user_list'),
    path('cadmin/users/toggle_permission/<int:user_id>/', views.toggle_user_permission, name='toggle_user_permission'),
    path('cadmin/edit_homepage_text/', views.edit_homepage_text, name='edit_homepage_text'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', views.homepage, name='homepage'),
    path('feedback/', views.submit_feedback, name='submit_feedback'),
]