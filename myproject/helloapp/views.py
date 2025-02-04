# Create your views here.

# helloapp/views.py

import json
from django.http import JsonResponse, HttpResponse
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
from .models import BuddyMatchingUser, HomepageText, Feedback
from .forms import BuddyMatchingUserCreationForm, LoginForm, FeedbackForm
from .matching import run_matching
import csv

def homepage(request):
    """
    Render the homepage template.
    """

    homepage_text = HomepageText.objects.create()

    days_left = None

    # Wählen Sie den Inhalt je nach Sprache
    language_code = get_language()  # Gibt den aktuellen Sprachcode zurück (z.B. 'de' oder 'en')

    if language_code == 'de':
        content = homepage_text.content_de
    else:
        content = homepage_text.content_en
    
    return render(request, 'helloapp/homepage.html')


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

class FeedbackView(View):
    """
    View to render the Feedback form and handle form submissions.
    """
    template_name = 'helloapp/feedback.html'
    
    def get(self, request):
        form = FeedbackForm()
        return render(request, self.template_name, {'form': form})
        
    def post(self, request):
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)  # Create a feedback object without saving it
            if isinstance(request.user, BuddyMatchingUser):
                feedback.student = request.user  # Set the `student` field
            else:
                return JsonResponse({"error": "User is not a valid BuddyMatchingUser"}, status=400)
            feedback.save()  # Save the feedback object with the `student` value
            return JsonResponse({'message': 'Feedback submitted successfully!'}, status=201)
        return JsonResponse({'errors': form.errors}, status=400)


@login_required
def submit_feedback(request):
    """
    Handle feedback form submissions.
    """
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            if isinstance(request.user, BuddyMatchingUser):
                feedback.student = request.user  # `request.user` will be an instance of BuddyMatchingUser
            else:
                return JsonResponse({"error": "User is not a valid BuddyMatchingUser"}, status=400)
            feedback.save()
            return JsonResponse({"message": "Feedback submitter successfully!"}, status=201)
    else:
        form = FeedbackForm()
    return JsonResponse({"errors": form.errors}, status=400)





@user_passes_test(lambda u: u.is_staff)
def admin_feedback_list(request):
    """
    Render the feedback list for the admin.
    """
    feedbacks = Feedback.objects.all()  # get feedback from database
    return render(request, 'helloapp/admin_feedback_list.html', {'feedbacks': feedbacks})


@user_passes_test(lambda u: u.is_staff)
def export_feedback_csv(request):
    """
    Export feedback data as CSV.
    """
    feedbacks = Feedback.objects.all()
    
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="feedback_export.csv"'

    writer = csv.writer(response, delimiter=';')
    writer.writerow(['Student', 'Text Feedback', 'Rating 1', 'Rating 2', 'Datum'])
    
    for feedback in feedbacks:
        writer.writerow([
            feedback.student.email,
            feedback.text_feedback,
            feedback.rating_1,
            feedback.rating_2,
            feedback.submitted_at.strftime('%Y-%m-%d'), # if time should be included: '%Y-%m-%d %H:%M:%S'
        ])
    
    return response

@login_required
def profile_view(request):
    """
    Shows the profile of the currently logged in user.
    """
    profile = request.user

    # Calculate days left for account deletion
    days_left = None
    if profile.is_authenticated:
        days_left = (profile.deletion_date - now().date()).days

    return render(request, 'helloapp/profile.html', {
        'profile': profile,
        'days_left': days_left,  # Now the template can use this variable
    })