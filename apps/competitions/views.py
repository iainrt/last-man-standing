from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CompetitionForm, JoinCompetitionForm
from .models import Competition, CompetitionMember


@login_required
def competition_list_view(request):
    memberships = (
        request.user.competition_memberships
        .select_related(
            "competition",
            "competition__season",
            "competition__season__league",
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

    return render(
        request,
        "competitions/detail.html",
        {
            "competition": competition,
            "membership": membership,
            "members": members,
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
            ).first()

            if competition is None:
                messages.error(request, "No active competition found with that invite code.")
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