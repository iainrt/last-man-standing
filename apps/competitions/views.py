from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseForbidden
from django.db.models import Count

from .forms import CompetitionForm, JoinCompetitionForm, CompetitionGameweekForm
from .models import Competition, CompetitionMember, CompetitionGameweek

from apps.selections.services.selection_service import (
    deadline_has_passed,
    get_competition_gameweek_selections,
    get_current_competition_gameweek,
    get_existing_selection,
    get_matches_for_competition_gameweek,
    get_published_competition_gameweeks,
)


@login_required
def competition_list_view(request):
    memberships = (
        request.user.competition_memberships
        .select_related(
            "competition",
            "competition__season",
            "competition__season__league",
        )
        .annotate(
            member_count=Count("competition__members")
        )
        .order_by("-joined_at")
    )

    return render(
        request,
        "competitions/list.html",
        {
            "memberships": memberships,
        },
    )


@login_required
def create_competition_view(request):
    if not request.user.profile.can_create_competitions:
        messages.error(
            request,
            "You do not currently have permission to create competitions.",
        )
        return redirect("competition_list")

    if request.method == "POST":
        form = CompetitionForm(request.POST)

        if form.is_valid():
            competition = form.save(commit=False)
            competition.created_by = request.user
            competition.save()

            CompetitionMember.objects.create(
                competition=competition,
                user=request.user,
                is_admin=True,
            )

            messages.success(
                request,
                "Competition created successfully.",
            )

            return redirect(
                "competition_detail",
                competition_id=competition.id,
            )

    else:
        form = CompetitionForm()

    return render(
        request,
        "competitions/create.html",
        {
            "form": form,
        },
    )


@login_required
def competition_detail_view(request, competition_id):
    competition = get_object_or_404(
        Competition.objects.select_related(
            "season",
            "season__league",
            "created_by",
        ),
        id=competition_id,
    )

    membership = get_object_or_404(
        CompetitionMember,
        competition=competition,
        user=request.user,
    )

    members = (
        competition.members
        .select_related(
            "user",
            "user__profile",
            "user__profile__favourite_team",
        )
        .order_by("is_eliminated", "joined_at")
    )

    current_competition_gameweek = get_current_competition_gameweek(competition)

    published_gameweeks = get_published_competition_gameweeks(competition)

    selected_competition_gameweek = current_competition_gameweek

    selected_gameweek_id = request.GET.get("week")

    if selected_gameweek_id:
        selected_competition_gameweek = published_gameweeks.filter(
            id=selected_gameweek_id,
        ).first() or current_competition_gameweek

    gameweek_matches = []
    user_selection = None
    all_selections = []
    deadline_passed = False

    if selected_competition_gameweek:
        gameweek_matches = get_matches_for_competition_gameweek(
            selected_competition_gameweek
        )

        user_selection = get_existing_selection(
            membership,
            selected_competition_gameweek,
        )

        deadline_passed = deadline_has_passed(selected_competition_gameweek)

        if deadline_passed:
            all_selections = get_competition_gameweek_selections(
                selected_competition_gameweek
            )

    active_members_count = members.filter(is_eliminated=False).count()

    return render(
        request,
        "competitions/detail.html",
        {
            "competition": competition,
            "membership": membership,
            "members": members,
            "current_competition_gameweek": current_competition_gameweek,
            "published_gameweeks": published_gameweeks,
            "selected_competition_gameweek": selected_competition_gameweek,
            "gameweek_matches": gameweek_matches,
            "user_selection": user_selection,
            "all_selections": all_selections,
            "deadline_passed": deadline_passed,
            "active_members_count": active_members_count,
        },
    )

@login_required
def join_competition_view(request):
    if request.method == "POST":
        form = JoinCompetitionForm(request.POST)

        if form.is_valid():
            invite_code = form.cleaned_data["invite_code"].strip()

            competition = Competition.objects.filter(
                invite_code__iexact=invite_code,
                is_active=True,
                is_locked=False,
            ).first()

            if competition is None:
                messages.error(request, "No joinable competition found with that invite code.")
                return redirect("competition_join")

            membership, created = CompetitionMember.objects.get_or_create(
                competition=competition,
                user=request.user,
                defaults={
                    "is_admin": False,
                },
            )

            if created:
                messages.success(request, "You have joined the competition.")
            else:
                messages.info(request, "You are already a member of this competition.")

            return redirect(
                "competition_detail",
                competition_id=competition.id,
            )

    else:
        form = JoinCompetitionForm()

    return render(
        request,
        "competitions/join.html",
        {
            "form": form,
        },
    )

def user_is_competition_admin(user, competition):
    return CompetitionMember.objects.filter(
        competition=competition,
        user=user,
        is_admin=True,
    ).exists()


@login_required
def lock_competition_view(request, competition_id):
    competition = get_object_or_404(Competition, id=competition_id)

    if not user_is_competition_admin(request.user, competition):
        return HttpResponseForbidden("You are not an admin of this competition.")

    if request.method == "POST":
        competition.is_locked = True
        competition.save(update_fields=["is_locked"])
        messages.success(request, "Competition locked.")

    return redirect("competition_detail", competition_id=competition.id)


@login_required
def unlock_competition_view(request, competition_id):
    competition = get_object_or_404(Competition, id=competition_id)

    if not user_is_competition_admin(request.user, competition):
        return HttpResponseForbidden("You are not an admin of this competition.")

    if request.method == "POST":
        competition.is_locked = False
        competition.save(update_fields=["is_locked"])
        messages.success(request, "Competition unlocked.")

    return redirect("competition_detail", competition_id=competition.id)


@login_required
def regenerate_invite_code_view(request, competition_id):
    competition = get_object_or_404(Competition, id=competition_id)

    if not user_is_competition_admin(request.user, competition):
        return HttpResponseForbidden("You are not an admin of this competition.")

    if request.method == "POST":
        competition.regenerate_invite_code()
        messages.success(request, "Invite code regenerated.")

    return redirect("competition_detail", competition_id=competition.id)


@login_required
def remove_member_view(request, competition_id, member_id):
    competition = get_object_or_404(Competition, id=competition_id)

    if not user_is_competition_admin(request.user, competition):
        return HttpResponseForbidden("You are not an admin of this competition.")

    member = get_object_or_404(
        CompetitionMember,
        id=member_id,
        competition=competition,
    )

    if request.method == "POST":
        if member.user == competition.created_by:
            messages.error(request, "You cannot remove the competition creator.")
        elif member.user == request.user:
            messages.error(request, "You cannot remove yourself.")
        else:
            member.delete()
            messages.success(request, "Member removed.")

    return redirect("competition_detail", competition_id=competition.id)

@login_required
def manage_competition_gameweeks_view(request, competition_id):
    competition = get_object_or_404(
        Competition.objects.select_related("season"),
        id=competition_id,
    )

    if not user_is_competition_admin(request.user, competition):
        return HttpResponseForbidden(
            "You are not an admin of this competition."
        )

    competition_gameweeks = (
        CompetitionGameweek.objects
        .filter(competition=competition)
        .select_related("gameweek")
        .order_by("gameweek__number")
    )

    if request.method == "POST":
        form = CompetitionGameweekForm(
            request.POST,
            competition=competition,
        )

        if form.is_valid():
            gameweek = form.cleaned_data["gameweek"]
            deadline = form.cleaned_data["deadline"]

            CompetitionGameweek.objects.filter(
                competition=competition,
            ).update(is_published=False)

            competition_gameweek, created = (
                CompetitionGameweek.objects.update_or_create(
                    competition=competition,
                    gameweek=gameweek,
                    defaults={
                        "deadline": deadline,
                        "is_published": True,
                    },
                )
            )

            messages.success(
                request,
                f"{competition_gameweek.gameweek} published for this competition.",
            )

            return redirect(
                "competition_gameweeks",
                competition_id=competition.id,
            )

    else:
        published_gameweek_ids = (
            CompetitionGameweek.objects
            .filter(competition=competition)
            .values_list("gameweek_id", flat=True)
        )

        next_gameweek = (
            competition.season.gameweeks
            .exclude(id__in=published_gameweek_ids)
            .order_by("number")
            .first()
        )

        initial = {}

        if next_gameweek:
            initial["gameweek"] = next_gameweek
            initial["deadline"] = next_gameweek.deadline

        form = CompetitionGameweekForm(
            competition=competition,
            initial=initial,
        )

    return render(
        request,
        "competitions/gameweeks.html",
        {
            "competition": competition,
            "form": form,
            "competition_gameweeks": competition_gameweeks,
        },
    )


@login_required
def unpublish_competition_gameweek_view(request, competition_id, competition_gameweek_id):
    competition = get_object_or_404(Competition, id=competition_id)

    if not user_is_competition_admin(request.user, competition):
        return HttpResponseForbidden("You are not an admin of this competition.")

    competition_gameweek = get_object_or_404(
        CompetitionGameweek,
        id=competition_gameweek_id,
        competition=competition,
    )

    if request.method == "POST":
        competition_gameweek.is_published = False
        competition_gameweek.save(update_fields=["is_published"])

        messages.success(
            request,
            f"{competition_gameweek.gameweek} unpublished.",
        )

    return redirect(
        "competition_gameweeks",
        competition_id=competition.id,
    )