from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from apps.fixtures.models import Team

from .models import Profile

from apps.core.forms import apply_form_control_styles


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_form_control_styles(self)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        
        fields = [
            "screen_name",
            "favourite_team",
            "is_public",
        ]

        labels = {
            "is_public": (
                "Allow other players to view my public profile, "
                "achievements and statistics"
            ),
        }
        
        help_texts = {
            "is_public": (
                "If disabled, other players cannot view your profile. "
                "Competition participation and screen name will still be visible."
            ),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["favourite_team"].queryset = Team.objects.order_by("name")
        apply_form_control_styles(self)
