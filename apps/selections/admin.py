from django.contrib import admin

from .models import Selection
from .services.results_service import process_selection


@admin.action(description="Process selected results")
def process_selected_results(modeladmin, request, queryset):
    processed_count = 0

    for selection in queryset:
        if process_selection(selection):
            processed_count += 1

    modeladmin.message_user(
        request,
        f"Processed {processed_count} selections.",
    )


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

    actions = [
        process_selected_results,
    ]