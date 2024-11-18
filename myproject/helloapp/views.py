# Create your views here.

# helloapp/views.py
#from django.http import JsonResponse
#from django.shortcuts import render

#def hello_world(request):
#    return JsonResponse({"message": "Hello World"})  # Returning JSON data

#def index(request):
#    return render(request, 'helloapp/index.html')  # Render the HTML template

# helloapp/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Entry
import json
from django.shortcuts import render

def index(request):
    return render(request, 'helloapp/index.html')  # Adjust the path to your template if needed


@csrf_exempt
def save_entry(request):
    if request.method == "POST":
        data = json.loads(request.body)
        text = data.get("text", "")
        entry = Entry.objects.create(text=text)
        return JsonResponse({"message": "Entry saved!", "entry_id": entry.id})

def get_entries(request):
    entries = Entry.objects.all().values("id", "text")
    return JsonResponse({"entries": list(entries)})


