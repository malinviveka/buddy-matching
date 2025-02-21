from django.urls import path, include
from . import views
from .views import AccountCreationView

urlpatterns = [
    path('create-account/', AccountCreationView.as_view(), name='create_account_view'),
    path('submit-account/', views.create_account, name='create_account'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cadmin/users/', views.admin_user_list, name='admin_user_list'),
    path('cadmin/users/toggle_permission/<int:user_id>/', views.toggle_user_permission, name='toggle_user_permission'),
    path('reset-deletion-date/', views.reset_deletion_date, name='reset_deletion_date'),
    path('profile/', views.profile_view, name='profile'),
    path("user/delete/", views.delete_user_confirm, name="delete_user_confirm"),
    path("user/delete/confirm/", views.delete_user, name="delete_user"),
    path('', views.homepage, name='homepage'),
]