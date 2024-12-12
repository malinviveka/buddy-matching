from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from .models import BuddyMatchingUser
from django.contrib.auth.forms import UserCreationForm


class BuddyMatchingUserCreationForm(UserCreationForm):
    #password = forms.CharField(widget=forms.PasswordInput)
    #password_confirmation = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    
    class Meta: 
        model = BuddyMatchingUser
        fields = [
            'role', 'surname', 'first_name', 'preferred_language', 
            'email', 'degree_level', 'app_matr_number', 
            'department', 'country', 'preferred_number_of_partners'
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
        }

    def clean(self):
        cleaned_data = super().clean()
        """
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        """
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if BuddyMatchingUser.objects.filter(email=email).exists():
            raise forms.ValidationError("There is already an existing user with this email adress.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        """
        user.set_password(self.cleaned_data['password1'])  # Passwort verschlüsseln
        if commit:
            user.save()

    
        """
        user.username = self.cleaned_data['email']
        if commit:
            user.save()

        return user



    def __init__(self, *args, **kwargs):
        super(BuddyMatchingUserCreationForm, self).__init__(*args, **kwargs)

        # Always hide 'partners' field
        if 'partners' in self.fields:
            self.fields.pop('partners')    
            
        if 'is_permitted' in self.fields:
            self.fields.pop('is_permitted')     






class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.EmailInput)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        # Authentifizierung über das BuddyMatchingUser-Modell
        try:
            user = BuddyMatchingUser.objects.get(email=email)
            if not user.check_password(password):
                raise forms.ValidationError("Invalid email or password")
        except BuddyMatchingUser.DoesNotExist:
            raise forms.ValidationError("Invalid email or password")
        return cleaned_data         