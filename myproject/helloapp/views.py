# Create your views here.

# helloapp/views.py
#from django.http import JsonResponse
#from django.shortcuts import render

# helloapp/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Entry
import json
from django.shortcuts import render, redirect
from .forms import AccountCreateForm
from django.views import View

#def index(request):
#    return render(request, 'helloapp/index.html')  # Render the HTML template
def index(request):
    return render(request, 'helloapp/index.html')  # Adjust the path to your template if needed

# View to render the account creation form
class AccountCreationView(View):
    template_name = 'helloapp/account_creation.html'
    #template_name = 'helloapp/index.html'
    
    def get(self, request):
        form = AccountCreateForm()
        return render(request, self.template_name, {'form': form})
        
    def post(self, request):
        form = AccountCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Account created successfully!'}, status=201)
        return JsonResponse({'errors': form.errors}, status=400)    

@require_http_methods(["POST"])
def create_account(request):
    form = AccountCreateForm(request.POST)  # Adjusting to parse JSON instead of form POST
    if form.is_valid():
        email = form.cleaned_data.get("email")
        
        # Create or prevent duplicate entries
        account, created = Entry.objects.get_or_create(
            email=email,
            defaults=form.cleaned_data
        )
        if created:
            return JsonResponse({"message": "Account created successfully"}, status=201)
        else:
            return JsonResponse({"error": "Account already exists"}, status=400)
    return JsonResponse({"errors": form.errors}, status=400)
    
    

# The following is old code from the helloWorld prototype. I leave it here for now, if someone needs to look something up

@csrf_exempt
def save_entry(request):
    if request.method == "POST":
        data = json.loads(request.body)
        text = data.get("text", "")
        entry = Entry.objects.create(text=text)
        return JsonResponse({"message": "Entry saved!", "entry_id": entry.id})

def get_entries(request):
    entries = Entry.objects.all().values("first_name", "surname")
    return JsonResponse({"entries": list(entries)})


