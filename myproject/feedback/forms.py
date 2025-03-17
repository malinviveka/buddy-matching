from django import forms
from feedback.models import Feedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = [
            "q1",
            "q2",
            "q3",
            "q4",
            "q5",
            "q5_details",
            "q6",
            "q7",
            "q8",
            "q8_details",
            "q9",
            "q9_details",
            "q10",
        ]
        widgets = {
            "q1": forms.Select(attrs={"id": "id_q1"}, choices=Feedback.ROLE_CHOICES),
            "q2": forms.Select(
                attrs={"id": "id_q2"}, choices=[(i, str(i)) for i in range(1, 6)]
            ),
            "q3": forms.Select(
                attrs={"id": "id_q3"}, choices=[(i, str(i)) for i in range(1, 6)]
            ),
            "q4": forms.Select(
                attrs={"id": "id_q4"}, choices=Feedback.DISCOVERY_CHOICES
            ),
            "q5": forms.Select(attrs={"id": "id_q5"}, choices=Feedback.SUPPORT_CHOICES),
            "q5_details": forms.Textarea(
                attrs={"id": "id_q5_details", "rows": 4, "cols": 40}
            ),
            "q6": forms.Select(
                attrs={"id": "id_q6"}, choices=Feedback.FIRST_CONTACT_CHOICES
            ),
            "q7": forms.Select(attrs={"id": "id_q7"}, choices=Feedback.CONTACT_CHOICES),
            "q8": forms.Select(
                attrs={"id": "id_q8"}, choices=Feedback.PROBLEMS_CHOICES
            ),
            "q8_details": forms.Textarea(
                attrs={"id": "id_q8_details", "rows": 4, "cols": 40}
            ),
            "q9": forms.Select(
                attrs={"id": "id_q9"}, choices=Feedback.RECOMMENDATION_CHOICES
            ),
            "q9_details": forms.Textarea(
                attrs={"id": "id_q9_details", "rows": 4, "cols": 40}
            ),
            "q10": forms.Textarea(attrs={"id": "id_q10", "rows": 4, "cols": 40}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hide the details fields by default
        self.fields["q5_details"].widget.attrs["style"] = "display: none;"
        self.fields["q8_details"].widget.attrs["style"] = "display: none;"
        self.fields["q9_details"].widget.attrs["style"] = "display: none;"

    def clean(self):
        cleaned_data = super().clean()

        q5 = cleaned_data.get("q5")
        q5_details = cleaned_data.get("q5_details")

        q8 = cleaned_data.get("q8")
        q8_details = cleaned_data.get("q8_details")

        q9 = cleaned_data.get("q9")
        q9_details = cleaned_data.get("q9_details")

        # If certain options are selected, the corresponding details field must be filled
        if q5 == "No" and not q5_details:
            self.add_error("q5_details", "Please specify the issue you encountered.")

        if q8 == "Yes/Sometimes" and not q8_details:
            self.add_error("q8_details", "Would you like to share the problem with us?")

        if q9 == "No/Maybe" and not q9_details:
            self.add_error(
                "q9_details",
                "Would you like to explain us why you would not recommend us?",
            )

        return cleaned_data
