from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.competitions.models import Competition, CompetitionMember, CompetitionGameweek
from apps.fixtures.models import Match, Team
from apps.selections.forms import SelectionForm
from apps.selections.models import Selection
from apps.selections.services.selection_service import (
    can_use_joker,
    deadline_has_passed,
    get_existing_selection,
    get_matches_for_competition_gameweek,
)

from apps.achievements.services.checkers.selection import (
    check_selection_achievements,
)


@login_required
def make_pick_view(request, competition_id, competition_gameweek_id):
    competition = get_object_or_404(Competition, id=competition_id)

    competition_member = get_object_or_404(
        CompetitionMember,
        competition=competition,
        user=request.user,
    )

    competition_gameweek = get_object_or_404(
        CompetitionGameweek.objects.select_related("gameweek"),
        id=competition_gameweek_id,
        competition=competition,
        is_published=True,
    )

    if competition_member.is_eliminated:
        messages.error(request, "You have been eliminated from this competition.")
        return redirect("competition_detail", competition_id=competition.id)

    if deadline_has_passed(competition_gameweek):
        messages.error(request, "The pick deadline has passed.")
        return redirect("competition_detail", competition_id=competition.id)

    existing_selection = get_existing_selection(
        competition_member,
        competition_gameweek,
    )

    matches = get_matches_for_competition_gameweek(competition_gameweek)

    used_team_ids = set(
        Selection.objects.filter(
            competition_member=competition_member,
        )
        .exclude(
            id=existing_selection.id if existing_selection else None,
        )
        .values_list("team_id", flat=True)
    )

    form = SelectionForm(
        request.POST or None,
        matches=matches,
        used_team_ids=used_team_ids,
        can_use_joker=can_use_joker(competition_member)
        or (existing_selection and existing_selection.is_joker),
    )

    if request.method == "POST" and form.is_valid():
        match_id, team_id = form.cleaned_data["match_team"].split(":")

        match = get_object_or_404(
            Match,
            id=match_id,
            gameweek=competition_gameweek.gameweek,
        )

        team = get_object_or_404(Team, id=team_id)

        if team not in [match.home_team, match.away_team]:
            messages.error(request, "Selected team is not part of that fixture.")
            return redirect(
                "selection_make_pick",
                competition_id=competition.id,
                competition_gameweek_id=competition_gameweek.id,
            )

        is_joker = form.cleaned_data.get("is_joker", False)

        if existing_selection:
            old_joker = existing_selection.is_joker

            existing_selection.match = match
            existing_selection.team = team
            existing_selection.is_joker = is_joker
            existing_selection.save()

            achievement_results = check_selection_achievements(existing_selection)

            for achievement_result in achievement_results:
                if achievement_result.should_notify:
                    messages.success(
                        request,
                        (
                            "Achievement unlocked: "
                            f"{achievement_result.user_achievement.achievement.name}"
                        ),
                    )

                    achievement_result.user_achievement.notification_seen_at = timezone.now()
                    achievement_result.user_achievement.save(
                        update_fields=[
                            "notification_seen_at",
                        ]
                    )

            if old_joker and not is_joker:
                competition_member.joker_used = False

            if is_joker:
                competition_member.joker_used = True

            competition_member.save(update_fields=["joker_used"])

            messages.success(request, f"Your pick has been updated: {team.name}.")

        else:
            selection = Selection.objects.create(
                competition_member=competition_member,
                competition_gameweek=competition_gameweek,
                match=match,
                team=team,
                is_joker=is_joker,
)

            if is_joker:
                competition_member.joker_used = True
                competition_member.save(update_fields=["joker_used"])

            messages.success(request, f"Your pick has been saved: {team.name}.")

            achievement_results = check_selection_achievements(selection)

            for achievement_result in achievement_results:
                if achievement_result.should_notify:
                    messages.success(
                        request,
                        (
                            "Achievement unlocked: "
                            f"{achievement_result.user_achievement.achievement.name}"
                        ),
                    )

                    achievement_result.user_achievement.notification_seen_at = timezone.now()
                    achievement_result.user_achievement.save(
                        update_fields=[
                            "notification_seen_at",
                        ]
                    )

        return redirect("competition_detail", competition_id=competition.id)

    return render(
        request,
        "selections/make_pick.html",
        {
            "competition": competition,
            "competition_gameweek": competition_gameweek,
            "matches": matches,
            "form": form,
            "existing_selection": existing_selection,
        },
    )