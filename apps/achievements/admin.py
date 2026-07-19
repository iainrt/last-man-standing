from django.contrib import admin

from .models import Achievement, UserAchievement


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = (
        "display_order",
        "name",
        "code",
        "category",
        "difficulty",
        "discovery",
        "xp_reward",
        "is_active",
        "tracking_start",
    )

    list_display_links = (
        "name",
    )

    list_editable = (
        "display_order",
    )

    list_filter = (
        "category",
        "difficulty",
        "discovery",
        "is_active",
    )

    search_fields = (
        "name",
        "code",
        "description",
    )


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "achievement",
        "unlocked_at",
    )

    list_filter = (
        "achievement",
        "unlocked_at",
    )

    search_fields = (
        "user__username",
        "user__profile__screen_name",
        "achievement__name",
        "achievement__code",
    )

    date_hierarchy = "unlocked_at"