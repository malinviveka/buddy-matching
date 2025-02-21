from django.urls import path
from . import views
from feedback.views import FeedbackView

urlpatterns = [
    path('feedback/', FeedbackView.as_view(), name='feedback'),
    path('submit-feedback/', views.submit_feedback, name='submit_feedback'),
    path('cadmin/feedback/', views.admin_feedback_list, name='admin_feedback_list'),
    path('cadmin/feedback/export/', views.export_feedback_csv, name='export_feedback_csv'),
]