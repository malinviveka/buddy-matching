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

    # Delete all partners of a user 
    user.partners.clear()  

    return redirect("admin_user_list")  # Return to admin page after deletion 


@login_required
def start_matching(request):
    try:
        # run matching process 
        run_matching()
        # If successful: return to homepage 
        return redirect("admin_user_list")
    except Exception as e:
        # If problem occurs, throw error message directly to user 
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
