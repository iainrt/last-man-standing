from collections import OrderedDict

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.utils import timezone

from .models import Achievement, UserAchievement


@login_required
def achievement_list_view(request):
    achievements = list(
        Achievement.objects
        .filter(is_active=True)
        .order_by(
            "display_order",
            "category",
            "difficulty",
            "name",
        )
    )

    user_achievements = {
        user_achievement.achievement_id: user_achievement
        for user_achievement in (
            UserAchievement.objects
            .filter(user=request.user)
            .select_related("achievement")
        )
    }

    grouped_cards = OrderedDict()
    hidden_cards = []

    total_achievements = len(achievements)
    completed_count = 0
    hidden_total_count = 0
    hidden_completed_count = 0
    xp_earned = 0

    for achievement in achievements:
        user_achievement = user_achievements.get(achievement.id)

        if user_achievement:
            progress = user_achievement.progress
            percentage = user_achievement.progress_percentage
            is_unlocked = user_achievement.is_unlocked
        else:
            progress = 0
            percentage = 0
            is_unlocked = False

        if achievement.discovery == Achievement.Discovery.HIDDEN:
            hidden_total_count += 1

        if is_unlocked:
            completed_count += 1
            xp_earned += achievement.xp_reward

            if achievement.discovery == Achievement.Discovery.HIDDEN:
                hidden_completed_count += 1

        card = {
            "achievement": achievement,
            "user_achievement": user_achievement,
            "progress": progress,
            "percentage": percentage,
            "is_unlocked": is_unlocked,
        }

        # Locked hidden achievements must not reveal their category.
        if (
            achievement.discovery == Achievement.Discovery.HIDDEN
            and not is_unlocked
        ):
            hidden_cards.append(card)
            continue

        category_name = achievement.get_category_display()

        grouped_cards.setdefault(
            category_name,
            [],
        ).append(card)

    completion_percentage = 0

    if total_achievements:
        completion_percentage = int(
            (completed_count / total_achievements) * 100
        )

    recently_unlocked = (
        UserAchievement.objects
        .filter(
            user=request.user,
            is_unlocked=True,
        )
        .select_related("achievement")
        .order_by("-unlocked_at")[:5]
    )

    return render(
        request,
        "achievements/list.html",
        {
            "grouped_cards": grouped_cards,
            "hidden_cards": hidden_cards,
            "recently_unlocked": recently_unlocked,
            "total_achievements": total_achievements,
            "completed_count": completed_count,
            "hidden_total_count": hidden_total_count,
            "hidden_completed_count": hidden_completed_count,
            "xp_earned": xp_earned,
            "completion_percentage": completion_percentage,
        },
    )


@login_required
def mark_achievement_notifications_seen(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    UserAchievement.objects.filter(
        user=request.user,
        is_unlocked=True,
        notification_seen_at__isnull=True,
    ).update(
        notification_seen_at=timezone.now(),
    )

    next_url = request.POST.get("next") or "achievement_list"

    return redirect(next_url)