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

    for achievement in achievements:
        user_achievement = unlocked.get(achievement.id)

        if user_achievement:
            progress = user_achievement.progress
            percentage = user_achievement.progress_percentage
            is_unlocked = user_achievement.is_unlocked
        else:
            progress = 0
            percentage = 0
            is_unlocked = False

        achievement_cards.append(
            {
                "achievement": achievement,
                "user_achievement": user_achievement,
                "progress": progress,
                "percentage": percentage,
                "is_unlocked": is_unlocked,
            }
        )

    return render(
        request,
        "achievements/list.html",
        {
            "achievement_cards": achievement_cards,
        },
    )