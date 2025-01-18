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
from .matching import run_matching


def homepage(request):
    """
    Render the homepage template.
    """

    homepage_text = HomepageText.objects.first()
    days_left = None

    # Wählen Sie den Inhalt je nach Sprache
    language_code = get_language()  # Gibt den aktuellen Sprachcode zurück (z.B. 'de' oder 'en')
    if language_code == 'de':
        content = homepage_text.content_de
    else:
        content = homepage_text.content_en

    if request.user.is_authenticated:
        user = request.user
        days_left = (user.deletion_date - now().date()).days

    return render(request, 'helloapp/homepage.html', {
        "content": content,
        "days_left": days_left,
    })

@login_required
def your_matches(request):
    partners = []

    if request.user.is_authenticated:
        user = request.user
        partners = user.partners.all() 
    return render(request, 'helloapp/your_matches.html', {
        "partners": partners,
    })

@login_required
def reset_deletion_date(request):
    """
    Reset Account Deletion Date by amount specified in "user.reset_deletion_date()".
    """
    user = request.user
    user.reset_deletion_date()
    return redirect('homepage')

class AccountCreationView(View):
    """
    View to render the account creation form and handle form submissions.
    """
    template_name = 'helloapp/account_creation.html'
    
    def get(self, request):
        form = BuddyMatchingUserCreationForm()
        return render(request, self.template_name, {'form': form})
        
    def post(self, request):
        form = BuddyMatchingUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Account created successfully!'}, status=201)
        return JsonResponse({'errors': form.errors}, status=400)    


@require_http_methods(["POST"])
def create_account(request):
    """
    Handle account creation form submissions.
    """
    form = BuddyMatchingUserCreationForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data.get("email")
   
        if BuddyMatchingUser.objects.filter(email=email).exists():
            return JsonResponse({"error": "There is already an existing user with this email address."}, status=400)
            #messages.info(request, "There is already an existing user with this email address.")
            #return redirect('login')

        messages.success(request, "Account created successfully!")

        form.save()
        return JsonResponse({"message": "Account created successfully!"}, status=201)
    return JsonResponse({"errors": form.errors}, status=400)


def login_view(request):
    """
    Render the login form and handle login form submissions.
    """
    template_name = 'helloapp/login.html'
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=email, password=password)
            if user is not None:
                # Nach iterationsmeeting auskommentieren!
                #if user.is_permitted:
                    login(request, user)
                    messages.success(request, "Login was successful!")
                    return redirect('homepage')
                #else:
                #    messages.error(request, "Your account is not permitted yet. Please wait for approval.")
            else:
                messages.error(request, "Invalid email or password")
    else:
        form = LoginForm()
    return render(request, template_name, {'form': form})    



def logout_view(request):
    """
    Log the user out and redirect to the homepage.
    """
    logout(request)
    return redirect('homepage')

@user_passes_test(lambda u: u.is_staff)
def admin_user_list(request):
    users = BuddyMatchingUser.objects.all()

    for user in users:
        # Die Partner für den jeweiligen User abrufen
        user.partner_names = [partner.first_name + " " + partner.surname + " " + partner.email for partner in user.partners.all()]
    
    return render(request, 'helloapp/admin_user_site.html', {'users': users})

@user_passes_test(lambda u: u.is_staff)
def toggle_user_permission(request, user_id):
    if request.method == "POST":
        user = get_object_or_404(BuddyMatchingUser, id=user_id)
        user.is_permitted = not user.is_permitted
        user.save()
        return JsonResponse({'is_permitted': user.is_permitted})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@user_passes_test(lambda u: u.is_staff)
def delete_partners(request, user_id):
    """
    Entfernt alle Partner des angegebenen Benutzers.
    """
    user = get_object_or_404(BuddyMatchingUser, id=user_id)
    
    # Alle Partner des Benutzers entfernen
    user.partners.clear()  # Dies entfernt alle Partnerschaften des Benutzers

    return redirect('admin_user_list')  # Nach dem Löschen zurück zur Admin-Seite

@user_passes_test(lambda u: u.is_staff)
def edit_homepage_text(request):
    homepage_text, created = HomepageText.objects.get_or_create(id=1)  # Standardtext erstellen, falls noch nicht vorhanden

    if request.method == "POST":
        homepage_text.content_de = request.POST.get("content_de")
        homepage_text.content_en = request.POST.get("content_en")
        homepage_text.save()
        return redirect('admin_user_list')  # Zurück zur Admin-Seite

    return render(request, "helloapp/edit_homepage_text.html", {"homepage_text": homepage_text})


@login_required
def start_matching(request):
    try:
        # Matching-Prozess ausführen
        run_matching()
        # Erfolg: Nach dem Matching zurück zur Homepage
        return redirect('admin_user_list')
    except Exception as e:
        # Falls ein Fehler auftritt, Fehlernachricht zurück an den User
        return render(request, 'helloapp/admin_user_site.html', {'error': f"Fehler beim Matching: {str(e)}"})

@login_required
def show_partners(request):
    user = request.user
    if user.role == 'Buddy':
        partners = user.partners.all()
    elif user.role == 'International Student':
        partners = user.partners.all()
    else:
        partners = []

    return render(request, 'helloapp/homepage.html', {'partners': partners})

# The following is old code from the helloWorld prototype. I leave it here for now, if someone needs to look something up

@csrf_exempt
def save_entry(request):
    if request.method == "POST":
        data = json.loads(request.body)
        text = data.get("text", "")
        entry = BuddyMatchingUser.objects.create(text=text)
        return JsonResponse({"message": "Entry saved!", "entry_id": entry.id})

def get_entries(request):
    entries = BuddyMatchingUser.objects.all().values("first_name", "surname")
    return JsonResponse({"entries": list(entries)})


