from apps.achievements.services.unlock_service import unlock_achievement, update_achievement_progress


def check_selection_achievements(selection):
    """
    Called whenever a player makes or updates a selection.
    """

    unlock_achievement(
        selection.competition_member.user,
        "first_pick",
    )

    if selection.is_joker:
        unlock_achievement(
            selection.competition_member.user,
            "joker_played",
        )