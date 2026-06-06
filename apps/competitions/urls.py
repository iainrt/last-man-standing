from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.competition_list_view,
        name="competition_list",
    ),
    path(
        "create/",
        views.create_competition_view,
        name="competition_create",
    ),

    path(
        "join/",
        views.join_competition_view,
        name="competition_join",
    ),
    
    path(
        "<int:competition_id>/",
        views.competition_detail_view,
        name="competition_detail",
    ),
]