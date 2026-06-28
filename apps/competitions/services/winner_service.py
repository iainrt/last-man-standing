from django.utils import timezone

from apps.competitions.models import (
    Competition,
    CompetitionMember,
    CompetitionWinner,
)


def evaluate_competition_winner(competition, competition_gameweek):
    """
    Rules

    Week 1
    ------
    Everyone eliminated -> Competition VOID (no winner)

    Week 2 onwards
    --------------
    One survivor -> Winner

    Everyone eliminated in same week -> Joint winners
    """

    if competition.status != Competition.Status.ACTIVE:
        return []

    members = CompetitionMember.objects.filter(
        competition=competition,
    )

    alive_members = members.filter(
        is_eliminated=False,
    )

    winners = []

    #
    # WEEK ONE
    #
    if competition_gameweek.competition_week_number == 1:

        if alive_members.count() == 0:

            competition.status = Competition.Status.VOID
            competition.is_active = False
            competition.winning_competition_gameweek = competition_gameweek
            competition.completed_at = timezone.now()

            competition.save(
                update_fields=[
                    "status",
                    "is_active",
                    "completed_at",
                    "winning_competition_gameweek",
                ]
            )

        return []

    #
    # WEEK TWO+
    #

    if alive_members.count() == 1:
        winners = list(alive_members)

    elif alive_members.count() == 0:

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

    return winners