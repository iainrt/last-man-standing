from apps.achievements.models import UserAchievement


def achievement_notifications(request):
    if not request.user.is_authenticated:
        return {
            "unseen_achievement_notifications": [],
        }

    unseen = (
        UserAchievement.objects
        .filter(
            user=request.user,
            is_unlocked=True,
            notification_seen_at__isnull=True,
        )
        .select_related("achievement")
        .order_by("unlocked_at")[:5]
    )

    return {
        "unseen_achievement_notifications": unseen,
    }