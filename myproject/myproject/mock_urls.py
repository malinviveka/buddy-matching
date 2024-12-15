# see: https://docs.djangoproject.com/en/5.1/topics/http/urls/

from django.urls import path, include
from django.http import HttpResponse

def dummy_admin(request): # Admin erstmal fake faken weil eh noch nichts da
   return HttpResponse("Mock Admin")

urlpatterns = [
    # urls for mock
    path('', include('helloapp.mock.mock_urls')),
    path('admin/', dummy_admin, name='mock_admin'),

    # urls from main version
    path('', include('helloapp.urls')),
]
