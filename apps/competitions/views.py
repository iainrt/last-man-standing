from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def competition_list_view(request):
    return render(
        request,
        "competitions/list.html",
    )