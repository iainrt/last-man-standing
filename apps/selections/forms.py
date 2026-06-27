from django import forms

from apps.selections.models import Selection

from apps.core.forms import apply_form_control_styles


class SelectionForm(forms.Form):
    match_team = forms.ChoiceField(
        choices=[],
        widget=forms.RadioSelect,
        label="Choose your team",
    )

    is_joker = forms.BooleanField(
        required=False,
        label="Play joker",
    )

    def __init__(
        self,
        *args,
        matches=None,
        used_team_ids=None,
        can_use_joker=False,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        used_team_ids = used_team_ids or set()
        choices = []

        for match in matches or []:
            home_disabled = match.home_team_id in used_team_ids
            away_disabled = match.away_team_id in used_team_ids

            if not home_disabled:
                choices.append(
                    (
                        f"{match.id}:{match.home_team_id}",
                        f"{match.home_team.name} vs {match.away_team.name} — pick {match.home_team.name}",
                    )
                )

            if not away_disabled:
                choices.append(
                    (
                        f"{match.id}:{match.away_team_id}",
                        f"{match.home_team.name} vs {match.away_team.name} — pick {match.away_team.name}",
                    )
                )

        self.fields["match_team"].choices = choices

        if not can_use_joker:
            self.fields.pop("is_joker")

        apply_form_control_styles(self)