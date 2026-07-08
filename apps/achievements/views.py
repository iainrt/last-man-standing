from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Achievement, UserAchievement


@login_required
def achievement_list_view(request):
    achievements = (
        Achievement.objects
        .filter(is_active=True)
        .order_by(
            "display_order",
            "category",
            "difficulty",
            "name",
        )
    )

    unlocked = {
        user_achievement.achievement_id: user_achievement
        for user_achievement in UserAchievement.objects
        .filter(user=request.user)
        .select_related("achievement")
    }

    achievement_cards = []

    total_achievements = achievements.count()
    completed_count = 0
    hidden_total_count = 0
    hidden_completed_count = 0
    xp_earned = 0

    for achievement in achievements:
        user_achievement = unlocked.get(achievement.id)

        if achievement.discovery == Achievement.Discovery.HIDDEN:
            hidden_total_count += 1

        if user_achievement:
            progress = user_achievement.progress
            percentage = user_achievement.progress_percentage
            is_unlocked = user_achievement.is_unlocked
        else:
            progress = 0
            percentage = 0
            is_unlocked = False

        if is_unlocked:
            completed_count += 1
            xp_earned += achievement.xp_reward

            if achievement.discovery == Achievement.Discovery.HIDDEN:
                hidden_completed_count += 1

        achievement_cards.append(
            {
                "achievement": achievement,
                "user_achievement": user_achievement,
                "progress": progress,
                "percentage": percentage,
                "is_unlocked": is_unlocked,
            }
        )

    completion_percentage = 0

    if total_achievements:
        completion_percentage = int(
            (completed_count / total_achievements) * 100
        )

    return render(
        request,
        "achievements/list.html",
        {
            "achievement_cards": achievement_cards,
            "total_achievements": total_achievements,
            "completed_count": completed_count,
            "hidden_total_count": hidden_total_count,
            "hidden_completed_count": hidden_completed_count,
            "xp_earned": xp_earned,
            "completion_percentage": completion_percentage,
        },
    )