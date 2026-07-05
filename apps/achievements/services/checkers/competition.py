from apps.achievements.services.unlock_service import unlock_achievement


def check_competition_achievements(
    competition,
    winners,
):
    """
    Called once a competition has completed.
    """

    if not winners:
        return

    for member in winners:

        unlock_achievement(
            member.user,
            "competition_winner",
        )

        if competition.has_multiple_winners:

            unlock_achievement(
                member.user,
                "joint_winner",
            )