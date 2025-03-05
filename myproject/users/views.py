from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.utils.timezone import now
from django.utils.translation import get_language
from .models import BuddyMatchingUser
from homepage.models import HomepageText
from .forms import BuddyMatchingUserCreationForm, LoginForm


def homepage(request):
    """
    Render the homepage template.
    """

    homepage_text, _ = HomepageText.objects.get_or_create(id=1)

    # Wählen Sie den Inhalt je nach Sprache
    language_code = get_language()  # Gibt den aktuellen Sprachcode zurück (z.B. 'de' oder 'en')
    if language_code == 'de':
        content = homepage_text.content_de
    else:
        content = homepage_text.content_en

    return render(request, 'homepage/homepage.html', {
        "content": content,
    })


@login_required
def reset_deletion_date(request):
    """
    Reset Account Deletion Date by amount specified in "user.reset_deletion_date()".
    """
    user = request.user
    user.reset_deletion_date()
    return redirect('profile')

class AccountCreationView(View):
    """
    View to render the account creation form and handle form submissions.
    """
    template_name = 'users/account_creation.html'
    
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

        messages.success(request, "Account created successfully!")

        form.save()
        return JsonResponse({"message": "Account created successfully!"}, status=201)
    return JsonResponse({"errors": form.errors}, status=400)


def login_view(request):
    """
    Render the login form and handle login form submissions.
    """
    template_name = 'users/login.html'
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=email, password=password)
            if user is not None:
                if user.is_permitted:
                    login(request, user)
                    messages.success(request, "Login was successful!")
                    return redirect('homepage')
                else:
                    messages.error(request, "Your account is not permitted yet. Please wait for approval.")
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
    
    return render(request, 'users/admin_user_site.html', {'users': users})

@user_passes_test(lambda u: u.is_staff)
def toggle_user_permission(request, user_id):
    if request.method == "POST":
        user = get_object_or_404(BuddyMatchingUser, id=user_id)
        user.is_permitted = not user.is_permitted
        user.save()
        return JsonResponse({'is_permitted': user.is_permitted})
    return JsonResponse({'error': 'Invalid request'}, status=400)

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

    return render(request, 'users/profile.html', {
        'profile': profile,
        'days_left': days_left,  # Now the template can use this variable
    })

@login_required
def delete_user_confirm(request):
    """
    Render a confirmation page before deleting the user's account.
    :param request: HTTP request object.
    :return: Rendered confirmation page.
    """
    return render(request, "users/delete_confirm.html")

@login_required
def delete_user(request):
    """
    Delete the authenticated user's account upon confirmation.
    
    Steps:
    1. Ensure the request method is POST to prevent accidental deletions via GET requests.
    2. Retrieve the currently logged-in user.
    3. Log the user out to ensure session cleanup.
    4. Delete the user from the database.
    5. Display a success message and redirect to the homepage.

    :param request: HTTP request object.
    :return: Redirect to the homepage after deletion or back to confirmation page.
    """
    if request.method == "POST":
        user = request.user  # Get the currently logged-in user
        logout(request)  # Log the user out before deleting the account
        user.delete()  # Remove the user from the database
        messages.success(request, "Your account has been successfully deleted.")
        return redirect("homepage")  # Redirect to the homepage or login page

    return redirect("delete_user_confirm")  # If not POST, return to confirmation page
