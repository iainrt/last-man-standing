from django.contrib import admin
from .models import League, Season, Team


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "api_id")
    search_fields = ("name", "country")


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ("league", "name", "api_season", "is_active")
    list_filter = ("league", "is_active")


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "short_name", "api_id")
    search_fields = ("name", "short_name")