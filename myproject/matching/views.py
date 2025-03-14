from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, redirect, get_object_or_404
from users.models import BuddyMatchingUser
from .matching import run_matching
# Create your views here.


@login_required
def your_matches(request):
    partners = []

    if request.user.is_authenticated:
        user = request.user
        partners = user.partners.all()
    return render(
        request,
        "matching/your_matches.html",
        {
            "partners": partners,
        },
    )


@user_passes_test(lambda u: u.is_staff)
def delete_partners(request, user_id):
    """
    Entfernt alle Partner des angegebenen Benutzers.
    """
    user = get_object_or_404(BuddyMatchingUser, id=user_id)

    # Alle Partner des Benutzers entfernen
    user.partners.clear()  # Dies entfernt alle Partnerschaften des Benutzers

    return redirect("admin_user_list")  # Nach dem Löschen zurück zur Admin-Seite


@login_required
def start_matching(request):
    try:
        # Matching-Prozess ausführen
        run_matching()
        # Erfolg: Nach dem Matching zurück zur Homepage
        return redirect("admin_user_list")
    except Exception as e:
        # Falls ein Fehler auftritt, Fehlernachricht zurück an den User
        return render(
            request,
            "users/admin_user_site.html",
            {"error": f"Fehler beim Matching: {str(e)}"},
        )


@login_required
def show_partners(request):
    user = request.user
    if user.role == "Buddy":
        partners = user.partners.all()
    elif user.role == "International Student":
        partners = user.partners.all()
    else:
        partners = []

    return render(request, "homepage/homepage.html", {"partners": partners})
