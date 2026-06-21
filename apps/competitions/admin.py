from django.contrib import admin

from .models import Competition, CompetitionMember, CompetitionGameweek


class CompetitionMemberInline(admin.TabularInline):
    model = CompetitionMember
    extra = 0

class CompetitionGameweekInline(admin.TabularInline):
    model = CompetitionGameweek
    extra = 0
    fields = (
        "competition_week_number",
        "gameweek",
        "deadline",
        "is_published",
    )


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "season",
        "created_by",
        "invite_code",
        "is_active",
        "is_locked",
        "allow_joker",
        "created_at",
    )

    search_fields = (
        "name",
        "invite_code",
        "created_by__username",
    )

    list_filter = (
        "season",
        "is_active",
    )

    inlines = [
        CompetitionMemberInline,
        CompetitionGameweekInline,
    ]


@admin.register(CompetitionMember)
class CompetitionMemberAdmin(admin.ModelAdmin):
    list_display = (
        "competition",
        "user",
        "is_admin",
        "is_eliminated",
        "eliminated_in_competition_gameweek",
        "joker_used",
        "joined_at",
    )

    list_filter = (
        "is_admin",
        "is_eliminated",
        "joker_used",
    )

@admin.register(CompetitionGameweek)
class CompetitionGameweekAdmin(admin.ModelAdmin):
    list_display = (
        "competition",
        "competition_week_number",
        "gameweek",
        "deadline",
        "is_published",
    )

    list_filter = (
        "competition",
        "is_published",
    )

    search_fields = (
        "competition__name",
        "gameweek__season__league__name",
    )

    ordering = (
        "competition",
        "competition_week_number",
    )