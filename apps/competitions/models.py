# apps/competitions/models.py

import secrets

from django.conf import settings
from django.db import models

from apps.fixtures.models import Season, Gameweek


def generate_invite_code():
    return secrets.token_urlsafe(6)[:8]


class Competition(models.Model):
    name = models.CharField(max_length=100)

    season = models.ForeignKey(
        Season,
        on_delete=models.PROTECT,
        related_name="competitions",
    )

    allow_joker = models.BooleanField(
        default=True,
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_competitions",
    )

    invite_code = models.CharField(
        max_length=12,
        unique=True,
        default=generate_invite_code,
    )

    is_active = models.BooleanField(default=True)
    is_locked = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        COMPLETE = "COMPLETE", "Complete"
        VOID = "VOID", "No Winner"

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    has_multiple_winners = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    winning_competition_gameweek = models.ForeignKey(
        "CompetitionGameweek",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="completed_competitions",
    )

    def regenerate_invite_code(self):
        self.invite_code = generate_invite_code()
        self.save(update_fields=["invite_code"])

    def lock(self):
        self.is_locked = True
        self.save(update_fields=["is_locked"])

    def __str__(self):
        return self.name


class CompetitionMember(models.Model):
    competition = models.ForeignKey(
        Competition,
        on_delete=models.CASCADE,
        related_name="members",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="competition_memberships",
    )

    eliminated_in_competition_gameweek = models.ForeignKey(
        "CompetitionGameweek",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="eliminated_members",
    )

    is_admin = models.BooleanField(default=False)
    is_eliminated = models.BooleanField(default=False)
    joker_used = models.BooleanField(default=False)

    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("competition", "user")

    def __str__(self):
        return f"{self.user.username} - {self.competition.name}"
    
class CompetitionGameweek(models.Model):
    competition = models.ForeignKey(
        Competition,
        on_delete=models.CASCADE,
        related_name="competition_gameweeks",
    )

    gameweek = models.ForeignKey(
        Gameweek,
        on_delete=models.CASCADE,
        related_name="competition_gameweeks",
    )

    competition_week_number = models.PositiveIntegerField()

    is_published = models.BooleanField(default=False)

    deadline = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["competition", "gameweek"],
                name="unique_gameweek_per_competition",
            ),
            models.UniqueConstraint(
                fields=["competition", "competition_week_number"],
                name="unique_week_number_per_competition",
            ),
        ]

        ordering = ["competition_week_number"]

    def __str__(self):
        return (
            f"{self.competition.name} - "
            f"Week {self.competition_week_number} "
            f"({self.gameweek})"
        )
    

class CompetitionWinner(models.Model):
    competition = models.ForeignKey(
        Competition,
        on_delete=models.CASCADE,
        related_name="winners",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="competition_wins",
    )

    competition_gameweek = models.ForeignKey(
        CompetitionGameweek,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="winners",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("competition", "user")

    def __str__(self):
        return f"{self.user.username} - {self.competition.name}"