from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class YaleSignUpForm(UserCreationForm):
    email = forms.EmailField(
        label=_("Yale email address"),
        help_text=_("Use your @yale.edu address to register."),
        widget=forms.EmailInput(attrs={'class': 'form-input'}),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-input'})
        self.fields['password2'].widget.attrs.update({'class': 'form-input'})

    def clean_email(self):
        email = self.cleaned_data.get("email", "")
        normalized = email.strip().lower()
        allowed_domains = getattr(settings, "ALLOWED_EMAIL_DOMAINS", [])

        if "@" not in normalized:
            raise ValidationError(_("Enter a valid email address."))

        domain = normalized.split("@")[-1]
        if allowed_domains and domain not in allowed_domains:
            raise ValidationError(
                _("You must use a Yale email address (allowed domains: %(domains)s)."),
                params={"domains": ", ".join(allowed_domains)},
            )

        if User.objects.filter(email__iexact=normalized).exists():
            raise ValidationError(_("An account with this email already exists."))

        return normalized

