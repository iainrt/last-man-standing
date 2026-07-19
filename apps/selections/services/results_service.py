from django.db import transaction
from django.utils import timezone

from apps.competitions.models import (
    Competition,
    CompetitionGameweek,
)
from apps.competitions.services.winner_service import (
    evaluate_competition_winner,
)
from apps.fixtures.models import Match
from apps.selections.models import Selection
from apps.achievements.services.checkers.result import (
    check_result_achievements,
)


def process_selection(selection):
    match = selection.match

    if match.status != Match.Status.FINISHED:
        return False

    if selection.processed:
        return False

    picked_home = selection.team_id == match.home_team_id
    picked_away = selection.team_id == match.away_team_id

    if not picked_home and not picked_away:
        return False

    member = selection.competition_member

    if match.winner == Match.Winner.DRAW:
        if selection.is_joker:
            selection.result = Selection.Result.DRAW_SAFE
        else:
            selection.result = Selection.Result.DRAW_ELIMINATED
            member.is_eliminated = True
            member.eliminated_in_competition_gameweek = (
                selection.competition_gameweek
            )

    elif match.winner == Match.Winner.HOME and picked_home:
        selection.result = Selection.Result.WIN

    elif match.winner == Match.Winner.AWAY and picked_away:
        selection.result = Selection.Result.WIN

    else:
        selection.result = Selection.Result.LOSE
        member.is_eliminated = True
        member.eliminated_in_competition_gameweek = (
            selection.competition_gameweek
        )

    selection.processed = True
    selection.save(update_fields=["result", "processed"])

    member.save(
        update_fields=[
            "is_eliminated",
            "eliminated_in_competition_gameweek",
        ]
    )

    check_result_achievements(selection)

    return True


def process_pending_selections():
    """
    Process completed selections, eliminate missed picks and evaluate
    competition winners once each competition gameweek has fully finished.
    """

    selections = list(
        Selection.objects
        .filter(
            processed=False,
            match__status=Match.Status.FINISHED,
        )
        .select_related(
            "match",
            "team",
            "competition_member",
            "competition_member__user",
            "competition_gameweek",
            "competition_gameweek__competition",
        )
    )

    processed_count = 0

    for selection in selections:
        if process_selection(selection):
            processed_count += 1

    due_gameweeks = (
        CompetitionGameweek.objects
        .filter(
            is_published=True,
            deadline__lte=timezone.now(),
            results_processed=False,
            competition__status=Competition.Status.ACTIVE,
        )
        .select_related(
            "competition",
            "gameweek",
        )
        .order_by(
            "competition_id",
            "competition_week_number",
        )
    )

    for competition_gameweek in due_gameweeks:
        with transaction.atomic():
            eliminate_missing_selections(
                competition_gameweek
            )

            # Do not decide the competition until every fixture has ended.
            if not all_gameweek_matches_finished(
                competition_gameweek
            ):
                continue

            # Every submitted selection should now have been processed.
            if competition_gameweek.selections.filter(
                processed=False,
            ).exists():
                continue

            evaluate_competition_winner(
                competition=competition_gameweek.competition,
                competition_gameweek=competition_gameweek,
            )

            competition_gameweek.results_processed = True
            competition_gameweek.results_processed_at = timezone.now()

            competition_gameweek.save(
                update_fields=[
                    "results_processed",
                    "results_processed_at",
                ]
            )

    return processed_count

def eliminate_missing_selections(competition_gameweek):
    """
    Eliminate every active member who failed to submit a selection before
    the gameweek deadline.

    This is idempotent because it only updates members who are still alive.
    """

    if competition_gameweek.deadline > timezone.now():
        return 0

    selected_member_ids = (
        competition_gameweek.selections
        .values_list(
            "competition_member_id",
            flat=True,
        )
    )

    missing_members = (
        competition_gameweek.competition.members
        .filter(is_eliminated=False)
        .exclude(id__in=selected_member_ids)
    )

    return missing_members.update(
        is_eliminated=True,
        eliminated_in_competition_gameweek=competition_gameweek,
    )


def all_gameweek_matches_finished(competition_gameweek):
    """
    Return True only when the underlying league gameweek has fixtures and
    every fixture has finished.
    """

    matches = Match.objects.filter(
        gameweek=competition_gameweek.gameweek,
    )

    return (
        matches.exists()
        and not matches.exclude(
            status=Match.Status.FINISHED,
        ).exists()
    )