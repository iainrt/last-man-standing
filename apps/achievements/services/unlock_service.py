from dataclasses import dataclass

from django.utils import timezone

from apps.achievements.models import Achievement, UserAchievement


@dataclass
class AchievementProgressResult:
    user_achievement: UserAchievement | None
    achievement_code: str
    progress_changed: bool = False
    unlocked_now: bool = False
    already_unlocked: bool = False
    not_found: bool = False
    not_active: bool = False
    not_started: bool = False

    @property
    def should_notify(self):
        return self.unlocked_now


def update_achievement_progress(
    user,
    achievement_code,
    amount=1,
):
    achievement = Achievement.objects.filter(
        code=achievement_code,
    ).first()

    if achievement is None:
        return AchievementProgressResult(
            user_achievement=None,
            achievement_code=achievement_code,
            not_found=True,
        )

    if not achievement.is_active:
        return AchievementProgressResult(
            user_achievement=None,
            achievement_code=achievement_code,
            not_active=True,
        )

    if (
        achievement.tracking_start
        and timezone.now() < achievement.tracking_start
    ):
        return AchievementProgressResult(
            user_achievement=None,
            achievement_code=achievement_code,
            not_started=True,
        )

    user_achievement, created = UserAchievement.objects.get_or_create(
        user=user,
        achievement=achievement,
        defaults={
            "progress": 0,
            "is_unlocked": False,
        },
    )

    if user_achievement.is_unlocked:
        return AchievementProgressResult(
            user_achievement=user_achievement,
            achievement_code=achievement_code,
            already_unlocked=True,
        )

    old_progress = user_achievement.progress

    user_achievement.progress += amount

    unlocked_now = False

    if user_achievement.progress >= achievement.target:
        user_achievement.progress = achievement.target
        user_achievement.is_unlocked = True
        user_achievement.unlocked_at = timezone.now()
        unlocked_now = True

    progress_changed = user_achievement.progress != old_progress

    user_achievement.save(
        update_fields=[
            "progress",
            "is_unlocked",
            "unlocked_at",
            "updated_at",
        ]
    )

    return AchievementProgressResult(
        user_achievement=user_achievement,
        achievement_code=achievement_code,
        progress_changed=progress_changed,
        unlocked_now=unlocked_now,
    )


def unlock_achievement(user, achievement_code):
    return update_achievement_progress(
        user=user,
        achievement_code=achievement_code,
        amount=10**9,
    )