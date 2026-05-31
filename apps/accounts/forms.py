from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from apps.fixtures.models import Team

from .models import Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    screen_name = forms.CharField(max_length=50)
    favourite_team = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        required=False,
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "screen_name",
            "favourite_team",
            "password1",
            "password2",
        )

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "screen_name",
            "favourite_team",
        ]