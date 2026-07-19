from django.db.models import Count

from apps.competitions.models import (
    Competition,
    CompetitionMember,
    CompetitionWinner,
)
from apps.selections.models import Selection


SURVIVAL_RESULTS = [
    Selection.Result.WIN,
    Selection.Result.DRAW_SAFE,
]

ELIMINATION_RESULTS = [
    Selection.Result.LOSE,
    Selection.Result.DRAW_ELIMINATED,
]


def get_player_statistics(user):
    """
    Calculate account-wide Last Man Standing statistics for a player.

    Statistics are derived from existing competition and selection data.
    No separate statistics table is maintained at this stage.
    """

    memberships = CompetitionMember.objects.filter(
        user=user,
    )

    selections = Selection.objects.filter(
        competition_member__user=user,
    )

    completed_memberships = memberships.filter(
        competition__status__in=[
            Competition.Status.COMPLETE,
            Competition.Status.VOID,
        ],
    )

    competition_wins = CompetitionWinner.objects.filter(
        user=user,
    )

    competitions_entered = memberships.count()
    competitions_completed = completed_memberships.count()
    competitions_won = competition_wins.count()

    competitions_alive = memberships.filter(
        competition__status=Competition.Status.ACTIVE,
        competition__is_active=True,
        is_eliminated=False,
    ).count()

    successful_picks = selections.filter(
        result__in=SURVIVAL_RESULTS,
    ).count()

    eliminated_picks = selections.filter(
        result__in=ELIMINATION_RESULTS,
    ).count()

    total_processed_picks = successful_picks + eliminated_picks

    pick_success_percentage = 0

    if total_processed_picks:
        pick_success_percentage = round(
            successful_picks
            / total_processed_picks
            * 100
        )

    joker_uses = selections.filter(
        is_joker=True,
    ).count()

    joker_saves = selections.filter(
        result=Selection.Result.DRAW_SAFE,
    ).count()

    best_survival_run = (
        selections
        .filter(result__in=SURVIVAL_RESULTS)
        .values("competition_member_id")
        .annotate(total=Count("id"))
        .order_by("-total")
        .values_list("total", flat=True)
        .first()
        or 0
    )

    single_wins = competition_wins.filter(
        competition__has_multiple_winners=False,
    ).count()

    joint_wins = competition_wins.filter(
        competition__has_multiple_winners=True,
    ).count()

    win_percentage = 0

    if competitions_completed:
        win_percentage = round(
            competitions_won
            / competitions_completed
            * 100
        )

    favourite_team = (
        selections
        .values(
            "team_id",
            "team__name",
        )
        .annotate(
            total_picks=Count("id"),
        )
        .order_by(
            "-total_picks",
            "team__name",
        )
        .first()
    )

    unique_clubs_picked = (
        selections
        .values("team_id")
        .distinct()
        .count()
    )

    return {
        "competitions_entered": competitions_entered,
        "competitions_completed": competitions_completed,
        "competitions_alive": competitions_alive,
        "competitions_won": competitions_won,
        "single_wins": single_wins,
        "joint_wins": joint_wins,
        "win_percentage": win_percentage,
        "successful_picks": successful_picks,
        "eliminated_picks": eliminated_picks,
        "weeks_survived": successful_picks,
        "pick_success_percentage": pick_success_percentage,
        "joker_uses": joker_uses,
        "joker_saves": joker_saves,
        "best_survival_run": best_survival_run,
        "favourite_team": favourite_team,
        "unique_clubs_picked": unique_clubs_picked,
    }