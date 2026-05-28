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
    

