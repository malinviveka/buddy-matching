from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from .models import BuddyMatchingUser
from django.contrib.auth.forms import UserCreationForm


class BuddyMatchingUserCreationForm(UserCreationForm):
    """
    Form for creating a new user.
    """
    class Meta: 
        model = BuddyMatchingUser
        fields = [
            'role', 'surname', 'first_name', 'preferred_language', 
            'email', 'degree_level', 'app_matr_number', 
            'department', 'country', 'preferred_number_of_partners', 'interests', 'is_permitted'
        ]
        widgets = {
            'role': forms.Select(attrs={'class': 'form-control', 'id': 'id_role'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'preferred_language': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'degree_level': forms.Select(attrs={'class': 'form-control'}),
            'app_matr_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'preferred_number_of_partners': forms.NumberInput(attrs={'class': 'form-control', 'data-role-field': 'Buddy'}),
            'interests': forms.CheckboxSelectMultiple(attrs={'class': 'form-check'}),
        }


    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if BuddyMatchingUser.objects.filter(email=email).exists():
            raise forms.ValidationError("There is already an existing user with this email address.")
        return email
    

    def save(self, commit=True):
        user = super().save(commit=False)

        user.username = self.cleaned_data['email']
        user.is_permitted = False
        
        if commit:
            user.save()

        return user


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Always hide 'partners' and 'is_permitted' fields
        if 'partners' in self.fields:
            self.fields.pop('partners')    
            
        if 'is_permitted' in self.fields:
            self.fields.pop('is_permitted')     




class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.EmailInput, required=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput, required=True)

    def clean(self):
        """
        Authenticate user/Valdiate form data.
        """
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
   
        # Authenticate user
        user = authenticate(username=email, password=password)
        if not user:
            raise forms.ValidationError("Invalid email or password")

        # Set user if necessary
        self.user = user
        return cleaned_data       