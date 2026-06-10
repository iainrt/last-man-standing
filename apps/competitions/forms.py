from django import forms

from .models import Competition


class CompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = [
            "name",
            "season",
            "allow_joker",
        ]

        labels = {
            "allow_joker": "Allow one joker per player",
        }

class JoinCompetitionForm(forms.Form):
    invite_code = forms.CharField(
        max_length=12,
        label="Invite code",
    )