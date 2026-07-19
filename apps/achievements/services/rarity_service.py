from django.contrib.auth import get_user_model
from django.db.models import Count, Q

from apps.achievements.models import UserAchievement
from apps.selections.models import Selection


def get_active_player_count():
    return (
        Selection.objects
        .values("competition_member__user_id")
        .distinct()
        .count()
    )


def get_rarest_unlocked_achievement(user):
    active_player_count = get_active_player_count()

    if active_player_count == 0:
        return None

    user_achievement = (
        UserAchievement.objects
        .filter(
            user=user,
            is_unlocked=True,
            achievement__is_active=True,
        )
        .select_related("achievement")
        .annotate(
            community_unlock_count=Count(
                "achievement__user_achievements",
                filter=Q(
                    achievement__user_achievements__is_unlocked=True,
                ),
                distinct=True,
            )
        )
        .order_by(
            "community_unlock_count",
            "-unlocked_at",
        )
        .first()
    )

    if user_achievement is None:
        return None

    rarity_percentage = round(
        user_achievement.community_unlock_count
        / active_player_count
        * 100
    )

    return {
        "user_achievement": user_achievement,
        "achievement": user_achievement.achievement,
        "unlock_count": user_achievement.community_unlock_count,
        "active_player_count": active_player_count,
        "rarity_percentage": rarity_percentage,
    }