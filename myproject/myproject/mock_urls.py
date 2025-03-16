# see: https://docs.djangoproject.com/en/5.1/topics/http/urls/

from django.urls import path, include
from django.http import HttpResponse


def dummy_admin(request):  # faking admin
    return HttpResponse("Mock Admin")


urlpatterns = [
    # urls for mock
    path("", include("helloapp.mock.mock_urls")),
    path("admin/", dummy_admin, name="mock_admin"),
    path("login/", include("django.contrib.auth.urls")),
    # urls from main version
    path("", include("helloapp.urls")),
]
