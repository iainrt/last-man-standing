from django.utils import timezone

from apps.competitions.models import CompetitionGameweek
from apps.selections.models import Selection


def get_current_competition_gameweek(competition):
    """
    Return the next published gameweek whose deadline has not passed.
    """
    return (
        CompetitionGameweek.objects
        .filter(
            competition=competition,
            is_published=True,
            deadline__gt=timezone.now(),
        )
        .select_related("gameweek")
        .order_by("gameweek__number")
        .first()
    )


def has_used_team(competition_member, team):
    return Selection.objects.filter(
        competition_member=competition_member,
        team=team,
    ).exists()


def has_selection_for_competition_gameweek(
    competition_member,
    competition_gameweek,
):
    return Selection.objects.filter(
        competition_member=competition_member,
        competition_gameweek=competition_gameweek,
    ).exists()


def can_use_joker(competition_member):
    return (
        competition_member.competition.allow_joker
        and not competition_member.joker_used
    )