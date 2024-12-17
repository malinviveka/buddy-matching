from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.views.decorators.http import require_http_methods
from django.contrib.auth import logout, authenticate, login
from helloapp.forms import BuddyMatchingUserCreationForm, LoginForm
from helloapp.mock.mock_forms import MockBuddyMatchingUserCreationForm, MockLoginForm

def mock_homepage(request):
    context = {'message': 'This is a mocked homepage!'}
    return render(request, 'helloapp/homepage.html', context)
    #return HttpResponse("This is a mocked homepage.")

class MockAccountCreationView(View):
    template_name = 'helloapp/account_creation.html'

    """
    ORIGINAL:
    def get(self, request):
        form = BuddyMatchingUserCreationForm()
        return render(request, self.template_name, {'form': form})
        
    def post(self, request):
        form = BuddyMatchingUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Account created successfully!'}, status=201)
        return JsonResponse({'errors': form.errors}, status=400) 
    """

    def get(self, request):
        # get form:
        # -----------
        # CHANGE BETWEEN REAL AND MOCK FORM
        # -----------
        #form = BuddyMatchingUserCreationForm()
        form = MockBuddyMatchingUserCreationForm()
        return render(request, self.template_name, {'form': form})
        
    def post(self, request):
        # -----------------
        # test how if form.is_valid() can be false:
        # -----------------

        # test form submission:
        email = request.POST.get("email", "")
        #password1 = request.POST.get("password1", "")
        #password2 = request.POST.get("password2", "")

        # test validation:
        #if not email or not password1 or not password2:
            #return JsonResponse({'errors': {"fields": "All fields are required."}}, status=400)
        #if password1 != password2:
            #return JsonResponse({'errors': {"password": "Passwords do not match."}}, status=400)
        if email == "mockuser@example.com":
            return JsonResponse({'errors': {"email": "This email is already taken."}}, status=400)

        # -----------------
        # if form.is_valid() is true:
        # -----------------
        # test successful account creation
        return JsonResponse({'message': 'Mocked account created successfully!'}, status=201)


@require_http_methods(["POST"])
def mock_create_account(request):
    """
    ORIGINAL:
    form = BuddyMatchingUserCreationForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data.get("email")
   
        if BuddyMatchingUser.objects.filter(email=email).exists():
            return JsonResponse({"error": "There is already an existing user with this email address."}, status=400)

        messages.success(request, "Account created successfully!")

        form.save()
        # redirect to loginpage after successful account creation
        return redirect('login')
    return JsonResponse({"errors": form.errors}, status=400)
    """
    # mock form data from POST request:
    email = request.POST.get("email", "")
    password1 = request.POST.get("password1", "")
    password2 = request.POST.get("password2", "")

    # test form.is_valid():
    errors = {}
    if not email:
        errors['email'] = "This field is required."
    if not password1 or not password2:
        errors['password'] = "Both password fields are required."
    elif password1 != password2:
        errors['password'] = "Passwords do not match."
    if email == "mockuser@example.com":
        errors['email'] = "This email is already taken."

    if errors:
        return JsonResponse({"errors": errors}, status=400)

    # test succesful account creation:
    messages.success(request, "Mocked account created successfully!")
    return JsonResponse({"message": "Mocked account created successfully!"}, status=201)


def mock_login_view(request):
    template_name = 'helloapp/login.html'

    """
    #ORIGINAL:
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login was successful!")
                return redirect('homepage')
            else:
                messages.error(request, "Invalid email or password")
    else:
        form = LoginForm()
    return render(request, template_name, {'form': form})    
    """

    if request.method == "POST":
        # -----------
        # CHANGE BETWEEN REAL AND MOCK FORM
        # -----------
        #form = LoginForm(request.POST)
        form = MockLoginForm(request.POST)
        
        # test form.is_valid():
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")

        # hardcoded test form.is_valid():
        if email == "test@example.com" and password == "password123":
            # successful test:
            messages.success(request, "Mocked login successful!")
            #return JsonResponse({"message": "Mocked login successful!"}, status=201)
            return redirect('mock_homepage')  
        else:
            # error test:
            messages.error(request, "Mocked login failed: Invalid email or password")
            return JsonResponse({"message":"Mocked login failed: Invalid email or password"}, status=400)

    else:
        # -----------
        # CHANGE BETWEEN REAL AND MOCK FORM
        # -----------
        #form = LoginForm()
        form = MockLoginForm
    return render(request, template_name, {'form': form})
            

    #if request.method == "POST":
        #return JsonResponse({"message": "Mocked login successful."})
    #return render(request, 'login.html')

def mock_logout_view(request):
    logout(request)
    messages.success(request, "Mocked logout successful!")
    return redirect('homepage')
