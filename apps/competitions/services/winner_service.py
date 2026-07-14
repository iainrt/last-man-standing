from django.utils import timezone

from apps.achievements.services.checkers.competition import (
    check_competition_achievements,
)
from apps.competitions.models import (
    Competition,
    CompetitionMember,
    CompetitionWinner,
)


def evaluate_competition_winner(competition, competition_gameweek):
    """
    Competition completion rules.

    Week 1:
    - If everyone is eliminated, the competition is void.
    - No achievements are awarded.

    Week 2 onwards:
    - If one player remains, that player wins.
    - If all remaining players are eliminated in the same week,
      they are recorded as joint winners.
    """

    if competition.status != Competition.Status.ACTIVE:
        return []

    members = CompetitionMember.objects.filter(
        competition=competition,
    ).select_related("user")

    alive_members = members.filter(
        is_eliminated=False,
    )

    competition_week_number = (
        competition_gameweek.competition_week_number
    )

    #
    # Week 1: everyone eliminated means no winner.
    #
    if competition_week_number == 1:
        if not alive_members.exists():
            competition.status = Competition.Status.VOID
            competition.is_active = False
            competition.has_multiple_winners = False
            competition.completed_at = timezone.now()
            competition.winning_competition_gameweek = competition_gameweek

            competition.save(
                update_fields=[
                    "status",
                    "is_active",
                    "has_multiple_winners",
                    "completed_at",
                    "winning_competition_gameweek",
                ]
            )

        return []

    winners = []

    #
    # Week 2 onwards: one survivor wins.
    #
    if alive_members.count() == 1:
        winners = list(alive_members)

    #
    # Everyone remaining was eliminated in this week:
    # those players are joint winners.
    #
    elif not alive_members.exists():
        winners = list(
            members.filter(
                eliminated_in_competition_gameweek=competition_gameweek,
            )
        )

    if not winners:
        return []

    for member in winners:
        CompetitionWinner.objects.get_or_create(
            competition=competition,
            user=member.user,
            defaults={
                "competition_gameweek": competition_gameweek,
            },
        )

    competition.status = Competition.Status.COMPLETE
    competition.is_active = False
    competition.has_multiple_winners = len(winners) > 1
    competition.completed_at = timezone.now()
    competition.winning_competition_gameweek = competition_gameweek

    competition.save(
        update_fields=[
            "status",
            "is_active",
            "has_multiple_winners",
            "completed_at",
            "winning_competition_gameweek",
        ]
    )

    check_competition_achievements(
        competition=competition,
        winners=winners,
    )

    return winners