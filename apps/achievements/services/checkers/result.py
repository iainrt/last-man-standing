from apps.achievements.services.unlock_service import unlock_achievement
from apps.selections.models import Selection


def check_result_achievements(selection):
    """
    Check achievements after a selection result has been processed.

    Returns achievement progress results so they can later be used
    for notifications or logging.
    """

    results = []

    competition_week_number = (
        selection.competition_gameweek.competition_week_number
    )

    survived = selection.result in {
        Selection.Result.WIN,
        Selection.Result.DRAW_SAFE,
    }

    # Awarded only for surviving Competition Week 1.
    if competition_week_number == 1 and survived:
        results.append(
            unlock_achievement(
                selection.competition_member.user,
                "week_one_survivor",
            )
        )

    # Awarded specifically when a joker protects the player from a draw.
    if selection.result == Selection.Result.DRAW_SAFE:
        results.append(
            unlock_achievement(
                selection.competition_member.user,
                "joker_saved_me",
            )
        )

    return results