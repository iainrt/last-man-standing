from django.urls import path

from . import views

urlpatterns = [
    path(
        "competitions/<int:competition_id>/gameweeks/<int:competition_gameweek_id>/pick/",
        views.make_pick_view,
        name="selection_make_pick",
    ),
]