from django.db import models


class League(models.Model):
    api_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50, default="England")
    logo_url = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ["country", "name"]

    def __str__(self):
        return self.name


class Season(models.Model):
    name = models.CharField(max_length=20)

    league = models.ForeignKey(
        League,
        on_delete=models.CASCADE,
        related_name="seasons",
    )

    api_season = models.IntegerField()
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("league", "api_season")
        ordering = ["-api_season", "league__name"]

    def __str__(self):
        return f"{self.league.name} {self.name}"


class Team(models.Model):
    api_id = models.IntegerField(unique=True, null=True, blank=True)

    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=50)

    crest_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class SeasonTeam(models.Model):
    season = models.ForeignKey(
        Season,
        on_delete=models.CASCADE,
        related_name="season_teams",
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="season_teams",
    )

    class Meta:
        unique_together = ("season", "team")

    def __str__(self):
        return f"{self.team.name} - {self.season}"
    

class Gameweek(models.Model):
    season = models.ForeignKey(
        Season,
        on_delete=models.CASCADE,
        related_name="gameweeks",
    )

    number = models.PositiveIntegerField()

    name = models.CharField(
        max_length=100,
    )

    deadline = models.DateTimeField()

    is_published = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("season", "number")
        ordering = ["season", "number"]

    def __str__(self):
        return f"{self.season} - Gameweek {self.number}"
    

class Match(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = "SCHEDULED", "Scheduled"
        IN_PLAY = "IN_PLAY", "In Play"
        FINISHED = "FINISHED", "Finished"
        POSTPONED = "POSTPONED", "Postponed"
        CANCELLED = "CANCELLED", "Cancelled"

    class Winner(models.TextChoices):
        HOME = "HOME", "Home"
        AWAY = "AWAY", "Away"
        DRAW = "DRAW", "Draw"

    api_id = models.IntegerField(unique=True)

    gameweek = models.ForeignKey(
        Gameweek,
        on_delete=models.CASCADE,
        related_name="matches",
    )

    home_team = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        related_name="home_matches",
    )

    away_team = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        related_name="away_matches",
    )

    kickoff_at = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SCHEDULED,
    )

    home_score = models.IntegerField(null=True, blank=True)
    away_score = models.IntegerField(null=True, blank=True)

    winner = models.CharField(
        max_length=10,
        choices=Winner.choices,
        null=True,
        blank=True,
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["kickoff_at"]

    def __str__(self):
        return f"{self.home_team} vs {self.away_team}"
