from apps.achievements.services.unlock_service import unlock_achievement


def check_selection_achievements(selection):
    """
    Called whenever a player makes or updates a selection.
    """

    results = []

    results.append(
        unlock_achievement(
            selection.competition_member.user,
            "first_pick",
        )
    )

    if selection.is_joker:
        results.append(
            unlock_achievement(
                selection.competition_member.user,
                "joker_played",
            )
        )

    return results