from django.utils import timezone

from apps.achievements.models import Achievement, UserAchievement


def unlock_achievement(user, achievement_code):
    achievement = Achievement.objects.filter(
        code=achievement_code,
        is_active=True,
    ).first()

    if achievement is None:
        return None, False

    if (
        achievement.tracking_start
        and timezone.now() < achievement.tracking_start
    ):
        return None, False

    user_achievement, created = UserAchievement.objects.get_or_create(
        user=user,
        achievement=achievement,
    )

    return user_achievement, created