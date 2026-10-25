from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User

class RegistrationForm(UserCreationForm):
    email=forms.EmailField(required=True)
    role=forms.ChoiceField(
        choices=[(User.Role.EMPLOYER, "Employer"), (User.Role.CANDIDATE, "Candidate")],
        required=True
    )
    class Meta(UserCreationForm.Meta):
        model=User
        fields=("username", "email", "role")