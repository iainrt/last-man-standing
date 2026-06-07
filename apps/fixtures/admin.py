from django.contrib import admin
from .models import League, Season, Team, SeasonTeam, Gameweek, Match


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "api_id")
    search_fields = ("name", "country")
    ordering = ("country", "name")


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ("league", "name", "api_season", "is_active")
    list_filter = ("league", "is_active")
    search_fields = ("name", "league__name")


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "short_name", "api_id")
    search_fields = ("name", "short_name")
    ordering = ("name",)


@admin.register(SeasonTeam)
class SeasonTeamAdmin(admin.ModelAdmin):
    list_display = (
        "season",
        "team",
    )

    list_filter = (
        "season",
    )

    search_fields = (
        "team__name",
        "season__league__name",
    )


@admin.register(Gameweek)
class GameweekAdmin(admin.ModelAdmin):
    list_display = (
        "season",
        "number",
        "deadline",
        "is_published",
    )

    list_filter = (
        "season",
        "is_published",
    )

    search_fields = (
        "season__league__name",
    )

    ordering = (
        "season",
        "number",
    )


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    date_hierarchy = "kickoff_at"

    list_display = (
        "home_team",
        "away_team",
        "gameweek",
        "kickoff_at",
        "status",
        "winner",
    )

    list_filter = (
        "status",
        "gameweek__season",
    )

    search_fields = (
        "home_team__name",
        "away_team__name",
    )

    ordering = (
        "kickoff_at",
    )