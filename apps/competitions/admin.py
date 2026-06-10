from django.contrib import admin

from .models import Competition, CompetitionMember


class CompetitionMemberInline(admin.TabularInline):
    model = CompetitionMember
    extra = 0


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "season",
        "created_by",
        "invite_code",
        "is_active",
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
    ]


@admin.register(CompetitionMember)
class CompetitionMemberAdmin(admin.ModelAdmin):
    list_display = (
        "competition",
        "user",
        "is_admin",
        "allow_joker",
        "is_eliminated",
        "joker_used",
        "joined_at",
    )

    list_filter = (
        "is_admin",
        "is_eliminated",
        "joker_used",
    )