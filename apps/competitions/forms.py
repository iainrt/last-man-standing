from django import forms

from .models import Competition, CompetitionGameweek

from apps.fixtures.models import Gameweek


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

class CompetitionGameweekForm(forms.ModelForm):
    class Meta:
        model = CompetitionGameweek
        fields = [
            "gameweek",
            "deadline",
        ]

        widgets = {
            "deadline": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                }
            )
        }

    def __init__(self, *args, competition=None, **kwargs):
        super().__init__(*args, **kwargs)

        if competition is not None:
            self.fields["gameweek"].queryset = Gameweek.objects.filter(
                season=competition.season,
            ).order_by("number")