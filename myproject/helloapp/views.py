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



#def index(request):
#    return render(request, 'helloapp/index.html')  # Render the HTML template
def homepage(request):
    return render(request, 'helloapp/homepage.html')  # Adjust the path to your template if needed


# View to render the account creation form
class AccountCreationView(View):
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
    form = BuddyMatchingUserCreationForm(request.POST)  # Adjusting to parse JSON instead of form POST
    if form.is_valid():
        form.clean()
        email = form.cleaned_data.get("email")
   
        if BuddyMatchingUser.objects.filter(email=email).exists():
            return JsonResponse({"error": "There is already an existing user with this email adress."}, status=400)

        messages.success(request, "Account created successfully!")

        form.save()
        # redirect to loginpage after successful account creation
        return redirect('login') 
    return JsonResponse({"errors": form.errors}, status=400)


def login_view(request):
    template_name = 'helloapp/login.html'
    
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login was successfull!")
                return redirect('homepage')
            else:
                messages.error(request, "Invalid email or password")
    else:
        form = LoginForm()
    return render(request, template_name, {'form': form})    



def logout_view(request):
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

