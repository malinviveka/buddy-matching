from django import forms
from django.core.exceptions import ValidationError


class MockBuddyMatchingUserCreationForm(forms.Form):
    # structure: forms.<>Field simulates the model; forms.Select simulates forms
    role = forms.ChoiceField(choices=[('International Student', 'International Student'), ('Buddy', 'Buddy')], widget=forms.Select(attrs={'class': 'form-control'}))
    surname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    preferred_language = forms.ChoiceField(choices=[('English', 'English'), ('German', 'German')], widget=forms.Select(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    degree_level = forms.ChoiceField(choices=[('Bachelors', 'Bachelors'), ('Masters', 'Masters')], widget=forms.Select(attrs={'class': 'form-control'}))
    app_matr_number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    # less options for my own convience:
    department = forms.ChoiceField(choices=[('CS', 'Computer Science'), ('His', 'History')], widget=forms.Select(attrs={'class': 'form-control'}))
    country = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    preferred_number_of_partners = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    
  
class MockLoginForm(forms.Form):
    
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control'}), required=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)
