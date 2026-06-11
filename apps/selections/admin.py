from django.contrib import admin

from .models import Selection


@admin.register(Selection)
class SelectionAdmin(admin.ModelAdmin):
    list_display = (
        "competition_member",
        "competition_gameweek",
        "team",
        "match",
        "is_joker",
        "result",
        "processed",
        "submitted_at",
    )

    list_filter = (
        "result",
        "processed",
        "is_joker",
        "competition_gameweek",
    )

    search_fields = (
        "competition_member__user__username",
        "competition_member__user__profile__screen_name",
        "team__name",
        "match__home_team__name",
        "match__away_team__name",
    )

    date_hierarchy = "submitted_at"