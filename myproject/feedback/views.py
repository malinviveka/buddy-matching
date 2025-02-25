import json
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render
from django.views import View
from .models import BuddyMatchingUser, Feedback
from .forms import FeedbackForm
import csv


class FeedbackView(View):
    """
    View to render the Feedback form and handle form submissions.
    """
    template_name = 'feedback/feedback.html'
    
    def get(self, request):
        form = FeedbackForm()
        return render(request, self.template_name, {'form': form})
        
    def post(self, request):
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)  # Create a feedback object without saving it
            if isinstance(request.user, BuddyMatchingUser):
                feedback.student = request.user  # Set the `student` field
            else:
                return JsonResponse({"error": "User is not a valid BuddyMatchingUser"}, status=400)
            feedback.save()  # Save the feedback object with the `student` value
            return JsonResponse({'message': 'Feedback submitted successfully!'}, status=201)
        return JsonResponse({'errors': form.errors}, status=400)


@login_required
def submit_feedback(request):
    """
    Handle feedback form submissions.
    """
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            if isinstance(request.user, BuddyMatchingUser):
                feedback.student = request.user  # `request.user` will be an instance of BuddyMatchingUser
            else:
                return JsonResponse({"error": "User is not a valid BuddyMatchingUser"}, status=400)
            feedback.save()
            return JsonResponse({"message": "Feedback submitted successfully!"}, status=201)
    else:
        form = FeedbackForm()
    return JsonResponse({"errors": form.errors}, status=400)


@user_passes_test(lambda u: u.is_staff)
def admin_feedback_list(request):
    """
    Render the feedback list for the admin.
    """
    feedbacks = Feedback.objects.all()  # get feedback from database
    return render(request, 'feedback/admin_feedback_list.html', {'feedbacks': feedbacks})


@user_passes_test(lambda u: u.is_staff)
def export_feedback_csv(request):
    """
    Export feedback data as CSV.
    """
    feedbacks = Feedback.objects.all()
    
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="feedback_export.csv"'

    writer = csv.writer(response, delimiter=';')
    writer.writerow(['Role', 'Satisfaction', 'Helpfulness', 'Source', 'Helpfulness of ISS', 'Issues with help', 'First contact', 'Overall contact', 'Problems', 'Share problems', 'Recommendation', 'Why not', 'Suggestions', 'Date'])  # add 'Student' in the beginning, if feedback should not be ananomous
    
    for feedback in feedbacks:
        writer.writerow([
            # feedback.student.email, # if student, who submitted feedback, should be displayed
            feedback.q1,
            feedback.q2,
            feedback.q3,
            feedback.q4,
            feedback.q5,
            feedback.q5_details,
            feedback.q6,
            feedback.q7,
            feedback.q8,
            feedback.q8_details,
            feedback.q9,
            feedback.q9_details,
            feedback.q10,
            feedback.submitted_at.strftime('%Y-%m-%d'), # if time should be included: '%Y-%m-%d %H:%M:%S'
        ])
    
    return response

