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

    path(
    "<int:competition_id>/lock/",
    views.lock_competition_view,
    name="competition_lock",
    ),

    path(
        "<int:competition_id>/unlock/",
        views.unlock_competition_view,
        name="competition_unlock",
    ),
    
    path(
        "<int:competition_id>/regenerate-code/",
        views.regenerate_invite_code_view,
        name="competition_regenerate_code",
    ),
    
    path(
        "<int:competition_id>/members/<int:member_id>/remove/",
        views.remove_member_view,
        name="competition_remove_member",
    ),
]