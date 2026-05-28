from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "screen_name",
        "user",
        "favourite_team",
        "created_at",
    )

    search_fields = (
        "screen_name",
        "user__username",
    )

    list_filter = (
        "favourite_team",
    )