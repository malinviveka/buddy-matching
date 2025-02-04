# helloapp/urls.py
from django.urls import path, include
from . import views
from .views import AccountCreationView, FeedbackView

urlpatterns = [
    path('create-account/', AccountCreationView.as_view(), name='create_account_view'),
    path('submit-account/', views.create_account, name='create_account'),
    path('login/', views.login_view, name='login'),
    #path('api/save_entry/', views.save_entry, name='save_entry'),
    #path('api/get_entries/', views.get_entries, name='get_entries'),
    path('logout/', views.logout_view, name='logout'),
    path('cadmin/users/', views.admin_user_list, name='admin_user_list'),
    path('cadmin/users/toggle_permission/<int:user_id>/', views.toggle_user_permission, name='toggle_user_permission'),
    path('cadmin/users/delete_partners/<int:user_id>/', views.delete_partners, name='delete_partners'),
    path('cadmin/edit_homepage_text/', views.edit_homepage_text, name='edit_homepage_text'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('reset-deletion-date/', views.reset_deletion_date, name='reset_deletion_date'),
    path('start-matching/', views.start_matching, name='start_matching'),
    path('show-partners/', views.show_partners, name='show_partners'),
    path('your_matches/', views.your_matches, name='your_matches'),
    path('', views.homepage, name='homepage'),
    path('feedback/', FeedbackView.as_view(), name='feedback'),
    path('submit-feedback/', views.submit_feedback, name='submit_feedback'),
    path('cadmin/feedback/', views.admin_feedback_list, name='admin_feedback_list'),
    path('cadmin/feedback/export/', views.export_feedback_csv, name='export_feedback_csv'),
    path('profile/', views.profile_view, name='profile')
]