from django.utils import timezone

from apps.competitions.models import CompetitionGameweek
from apps.fixtures.models import Match
from apps.selections.models import Selection


def get_current_competition_gameweek(competition):
    return (
        CompetitionGameweek.objects
        .filter(
            competition=competition,
            is_published=True,
        )
        .select_related("gameweek")
        .order_by("competition_week_number")
        .first()
    )


def get_published_competition_gameweeks(competition):
    return (
        CompetitionGameweek.objects
        .filter(competition=competition)
        .select_related("gameweek")
        .order_by("competition_week_number")
    )


def get_matches_for_competition_gameweek(competition_gameweek):
    return (
        Match.objects
        .filter(gameweek=competition_gameweek.gameweek)
        .select_related("home_team", "away_team")
        .order_by("kickoff_at")
    )


def get_existing_selection(competition_member, competition_gameweek):
    return (
        Selection.objects
        .filter(
            competition_member=competition_member,
            competition_gameweek=competition_gameweek,
        )
        .select_related("team", "match")
        .first()
    )


def get_competition_gameweek_selections(competition_gameweek):
    return (
        Selection.objects
        .filter(competition_gameweek=competition_gameweek)
        .select_related(
            "competition_member",
            "competition_member__user",
            "competition_member__user__profile",
            "team",
            "match",
        )
        .order_by("competition_member__user__profile__screen_name")
    )


def deadline_has_passed(competition_gameweek):
    return competition_gameweek.deadline <= timezone.now()


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