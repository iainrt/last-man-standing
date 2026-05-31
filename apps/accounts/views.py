from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.shortcuts import render, redirect

from .forms import RegisterForm, ProfileForm


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