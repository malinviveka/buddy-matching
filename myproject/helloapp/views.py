# Create your views here.

# helloapp/views.py

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.utils.timezone import now
from datetime import timedelta
from django.utils.translation import get_language
from .models import BuddyMatchingUser, HomepageText
from .forms import BuddyMatchingUserCreationForm, LoginForm
from ..matching.matching import run_matching



@user_passes_test(lambda u: u.is_staff)
def edit_homepage_text(request):
    homepage_text, created = HomepageText.objects.get_or_create(id=1)  # Standardtext erstellen, falls noch nicht vorhanden

    if request.method == "POST":
        homepage_text.content_de = request.POST.get("content_de")
        homepage_text.content_en = request.POST.get("content_en")
        homepage_text.save()
        return redirect('admin_user_list')  # Zurück zur Admin-Seite

    return render(request, "helloapp/edit_homepage_text.html", {"homepage_text": homepage_text})

