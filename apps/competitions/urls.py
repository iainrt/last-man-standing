from django.urls import path
from . import views

urlpatterns = [
    path(
        "",
        views.competition_list_view,
        name="competition_list",
    ),
]