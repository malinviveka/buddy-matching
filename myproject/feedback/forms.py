from django import forms
from feedback.models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['text_feedback', 'rating_1', 'rating_2']
        widgets = {
            'rating_1': forms.Select(attrs={'id': 'id_rating_1'}, choices=Feedback.RATING_CHOICES),
            'rating_2': forms.Select(attrs={'id': 'id_rating_2'}, choices=Feedback.RATING_CHOICES),
            'text_feedback': forms.Textarea(attrs={'id': 'id_text_feedback', 'rows': 4, 'cols': 40}),
        }
