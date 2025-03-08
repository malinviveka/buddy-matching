from django.urls import path
from . import views


urlpatterns = [
    path(
        "cadmin/users/delete_partners/<int:user_id>/",
        views.delete_partners,
        name="delete_partners",
    ),
    path("start-matching/", views.start_matching, name="start_matching"),
    path("show-partners/", views.show_partners, name="show_partners"),
    path("your_matches/", views.your_matches, name="your_matches"),
]
