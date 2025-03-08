from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from .models import HomepageText


@user_passes_test(lambda u: u.is_staff)
def edit_homepage_text(request):
    homepage_text, created = HomepageText.objects.get_or_create(
        id=1
    )  # Standardtext erstellen, falls noch nicht vorhanden

    if request.method == "POST":
        homepage_text.content_de = request.POST.get("content_de")
        homepage_text.content_en = request.POST.get("content_en")
        homepage_text.save()
        return redirect("admin_user_list")  # Zurück zur Admin-Seite

    return render(
        request, "homepage/edit_homepage_text.html", {"homepage_text": homepage_text}
    )
