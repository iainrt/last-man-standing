from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, get_user_model
from django.shortcuts import render, redirect, get_object_or_404

from .forms import RegisterForm, ProfileForm

from apps.achievements.models import Achievement, UserAchievement
from apps.accounts.services.player_statistics import (
    get_player_statistics,
)


@login_required
def profile_view(request):
    return render(
        request,
        "accounts/profile.html",
        {
            "profile": request.user.profile,
        },
    )


def register_view(request):
    if request.user.is_authenticated:
        return redirect("profile")

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data["email"]
            user.save()

            user.profile.screen_name = form.cleaned_data["screen_name"]
            user.profile.favourite_team = form.cleaned_data["favourite_team"]
            user.profile.save()

            login(request, user)

            return redirect("profile")
    else:
        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form},
    )

@login_required
def edit_profile_view(request):
    profile = request.user.profile

    if request.method == "POST":
        form = ProfileForm(
            request.POST,
            instance=profile,
        )

        if form.is_valid():
            form.save()
            return redirect("profile")

    else:
        form = ProfileForm(instance=profile)

    return render(
        request,
        "accounts/edit_profile.html",
        {
            "form": form,
        },
    )


def public_profile_view(request, user_id):
    User = get_user_model()

    profile_user = get_object_or_404(
        User.objects.select_related(
            "profile",
            "profile__favourite_team",
        ),
        id=user_id,
    )

    is_own_profile = (
        request.user.is_authenticated
        and request.user == profile_user
    )

    if not profile_user.profile.is_public and not is_own_profile:
        return render(
            request,
            "accounts/public_profile_private.html",
            {
                "profile_user": profile_user,
            },
        )

    profile_achievements = list(
        UserAchievement.objects
        .filter(
            user=profile_user,
            is_unlocked=True,
            achievement__is_active=True,
        )
        .select_related("achievement")
        .order_by(
            "achievement__display_order",
            "-unlocked_at",
        )
    )

    viewer_unlocked_achievement_ids = set()

    if request.user.is_authenticated:
        viewer_unlocked_achievement_ids = set(
            UserAchievement.objects.filter(
                user=request.user,
                is_unlocked=True,
            ).values_list(
                "achievement_id",
                flat=True,
            )
        )

    achievement_cards = []

    for user_achievement in profile_achievements:
        achievement = user_achievement.achievement

        hidden_from_viewer = (
            achievement.discovery == Achievement.Discovery.HIDDEN
            and achievement.id not in viewer_unlocked_achievement_ids
            and not is_own_profile
        )

        achievement_cards.append(
            {
                "achievement": achievement,
                "user_achievement": user_achievement,
                "hidden_from_viewer": hidden_from_viewer,
            }
        )

    total_active_achievements = Achievement.objects.filter(
        is_active=True,
    ).count()

    unlocked_count = len(profile_achievements)

    completion_percentage = 0

    if total_active_achievements:
        completion_percentage = int(
            (unlocked_count / total_active_achievements) * 100
        )

    achievement_xp = sum(
        user_achievement.achievement.xp_reward
        for user_achievement in profile_achievements
    )

    player_statistics = get_player_statistics(profile_user)

    return render(
        request,
        "accounts/public_profile.html",
        {
            "profile_user": profile_user,
            "is_own_profile": is_own_profile,
            "achievement_cards": achievement_cards,
            "unlocked_count": unlocked_count,
            "total_active_achievements": total_active_achievements,
            "completion_percentage": completion_percentage,
            "achievement_xp": achievement_xp,
            "player_statistics": player_statistics,
        },
    )