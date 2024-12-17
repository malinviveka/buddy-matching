# Create your views here.

# helloapp/views.py

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect
from .forms import BuddyMatchingUserCreationForm, LoginForm
from django.views import View
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .models import BuddyMatchingUser


def homepage(request):
    """
    Render the homepage template.
    """
    return render(request, 'helloapp/homepage.html')  


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
        # redirect to homepage after successful account creation
        return redirect('homepage')
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



# The following is old code from the helloWorld prototype. I leave it here for now, if someone needs to look something up
'''
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
'''

