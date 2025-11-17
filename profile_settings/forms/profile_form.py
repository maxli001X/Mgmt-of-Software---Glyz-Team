from django import forms

from ..models import Feedback, UserProfile


class EmailPreferencesForm(forms.ModelForm):
    """Form for managing email notification preferences."""
    
    class Meta:
        model = UserProfile
        fields = [
            "email_notifications_enabled",
            "email_on_replies",
            "email_on_upvotes",
            "email_on_mentions",
        ]
        widgets = {
            "email_notifications_enabled": forms.CheckboxInput(
                attrs={"class": "form-checkbox"}
            ),
            "email_on_replies": forms.CheckboxInput(
                attrs={"class": "form-checkbox"}
            ),
            "email_on_upvotes": forms.CheckboxInput(
                attrs={"class": "form-checkbox"}
            ),
            "email_on_mentions": forms.CheckboxInput(
                attrs={"class": "form-checkbox"}
            ),
        }
        labels = {
            "email_notifications_enabled": "Enable email notifications",
            "email_on_replies": "Email me when someone replies to my posts",
            "email_on_upvotes": "Email me when my posts receive upvotes",
            "email_on_mentions": "Email me when I am mentioned",
        }
        help_texts = {
            "email_notifications_enabled": "Master switch for all email notifications",
            "email_on_replies": "Get notified about replies to your posts",
            "email_on_upvotes": "Get notified when your posts are upvoted",
            "email_on_mentions": "Get notified when someone mentions you",
        }


class FeedbackForm(forms.ModelForm):
    """Form for submitting feedback."""
    
    class Meta:
        model = Feedback
        fields = ["feedback_type", "subject", "message"]
        widgets = {
            "feedback_type": forms.Select(
                attrs={"class": "form-select"}
            ),
            "subject": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Brief description of your feedback"
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-textarea",
                    "rows": 6,
                    "placeholder": "Please provide details about your feedback..."
                }
            ),
        }
        labels = {
            "feedback_type": "Type",
            "subject": "Subject",
            "message": "Message",
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["message"].required = True
        self.fields["subject"].required = True
