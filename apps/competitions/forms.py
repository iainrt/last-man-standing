from django import forms

from .models import Competition, CompetitionGameweek

from apps.fixtures.models import Gameweek

from apps.core.forms import apply_form_control_styles


class CompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = [
            "name",
            "season",
            "allow_joker",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_form_control_styles(self)


class JoinCompetitionForm(forms.Form):
    invite_code = forms.CharField(
        max_length=12,
        label="Invite code",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter invite code",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_form_control_styles(self)


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
                },
                format="%Y-%m-%dT%H:%M",
            )
        }

    def __init__(self, *args, competition=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["deadline"].input_formats = [
            "%Y-%m-%dT%H:%M",
        ]

        if competition is not None:
            self.fields["gameweek"].queryset = (
                Gameweek.objects
                .filter(season=competition.season)
                .order_by("number")
            )

            self.fields["gameweek"].label_from_instance = (
                self.gameweek_label_from_instance
            )
        
        apply_form_control_styles(self)

    def gameweek_label_from_instance(self, gameweek):
        return (
            f"Gameweek {gameweek.number} "
            f"— starting {gameweek.deadline:%d %b %Y %H:%M}"
        )