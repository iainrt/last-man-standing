from apps.achievements.services.unlock_service import unlock_achievement


def check_competition_achievements(competition, winners):
    """
    Check achievements after a competition has been completed.

    Every winner receives Competition Winner.

    If the competition has multiple winners, every winner also receives
    Joint Winner.

    Void competitions pass an empty winner list and award nothing.
    """

    results = []

    if not winners:
        return results

    for member in winners:
        results.append(
            unlock_achievement(
                member.user,
                "competition_winner",
            )
        )

        if competition.has_multiple_winners:
            results.append(
                unlock_achievement(
                    member.user,
                    "joint_winner",
                )
            )

    return results