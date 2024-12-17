from django.urls import path
from . import mock_views
from .mock_views import MockAccountCreationView

urlpatterns = [
    path('', mock_views.mock_homepage, name='mock_homepage'),
    path('login/', mock_views.mock_login_view, name='mock_login'),
    path('logout/', mock_views.mock_logout_view, name='mock_logout'),
    path('create-account/', MockAccountCreationView.as_view(), name='mock_create_account_view'),
    path('submit-account/', mock_views.mock_create_account, name='mock_create_account'),
]
