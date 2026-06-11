from django.db import models

from apps.competitions.models import CompetitionMember, CompetitionGameweek
from apps.fixtures.models import Match, Team


class Selection(models.Model):
    class Result(models.TextChoices):
        PENDING = "PENDING", "Pending"
        WIN = "WIN", "Win"
        LOSE = "LOSE", "Lose"
        DRAW_ELIMINATED = "DRAW_ELIMINATED", "Draw - eliminated"
        DRAW_SAFE = "DRAW_SAFE", "Draw - joker safe"

    competition_member = models.ForeignKey(
        CompetitionMember,
        on_delete=models.CASCADE,
        related_name="selections",
    )

    competition_gameweek = models.ForeignKey(
        CompetitionGameweek,
        on_delete=models.CASCADE,
        related_name="selections",
    )

    match = models.ForeignKey(
        Match,
        on_delete=models.PROTECT,
        related_name="selections",
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        related_name="selections",
    )

    is_joker = models.BooleanField(default=False)

    result = models.CharField(
        max_length=30,
        choices=Result.choices,
        default=Result.PENDING,
    )

    processed = models.BooleanField(default=False)

    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "competition_member",
                    "competition_gameweek",
                ],
                name="unique_selection_per_member_competition_gameweek",
            ),
            models.UniqueConstraint(
                fields=[
                    "competition_member",
                    "team",
                ],
                name="unique_team_per_member_competition",
            ),
        ]

    def __str__(self):
        return (
            f"{self.competition_member.user.username} - "
            f"{self.competition_gameweek} - "
            f"{self.team}"
        )