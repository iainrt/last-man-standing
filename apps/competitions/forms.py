from django import forms

from .models import Competition


class CompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = [
            "name",
            "season",
        ]

class JoinCompetitionForm(forms.Form):
    invite_code = forms.CharField(
        max_length=12,
        label="Invite code",
    )