from django import forms
from .models import Entry

class AccountCreateForm(forms.ModelForm):
    class Meta: 
        model = Entry
        fields = [
            'surname', 'first_name', 'preferred_language', 
            'email', 'degree_level', 'app_matr_number', 
            'department', 'country', 'preferred_number_of_partners'
        ]
        widgets = {
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'preferred_language': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'degree_level': forms.Select(attrs={'class': 'form-control'}),
            'app_matr_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'preferred_number_of_partners': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
        
    def __init__(self, *args, **kwargs):
        super(AccountCreateForm, self).__init__(*args, **kwargs)
        
        # Hide 'preferred_number_of_partners' if the role is not "Buddy"
        if self.instance and self.instance.role != 'Buddy':
            self.fields.pop('preferred_number_of_partners')

        # Always hide 'partners' field
        if 'partners' in self.fields:
            self.fields.pop('partners')    