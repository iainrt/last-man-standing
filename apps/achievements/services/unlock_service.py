from django.utils import timezone

from apps.achievements.models import Achievement, UserAchievement


def update_achievement_progress(
    user,
    achievement_code,
    amount=1,
):
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
        defaults={
            "progress": 0,
            "is_unlocked": False,
        },
    )

    if user_achievement.is_unlocked:
        return user_achievement, False

    user_achievement.progress += amount

    unlocked_now = False

    if user_achievement.progress >= achievement.target:
        user_achievement.progress = achievement.target
        user_achievement.is_unlocked = True
        user_achievement.unlocked_at = timezone.now()
        unlocked_now = True

    user_achievement.save(
        update_fields=[
            "progress",
            "is_unlocked",
            "unlocked_at",
            "updated_at",
        ]
    )

    return user_achievement, unlocked_now


def unlock_achievement(user, achievement_code):
    return update_achievement_progress(
        user=user,
        achievement_code=achievement_code,
        amount=10**9,
    )