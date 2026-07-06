from apps.achievements.services.unlock_service import unlock_achievement, update_achievement_progress
from apps.selections.models import Selection


def check_result_achievements(selection):
    """
    Called after a selection result has been calculated.
    """

    user = selection.competition_member.user

    if selection.result == Selection.Result.WIN:
        unlock_achievement(
            user,
            "week_one_survivor",
        )

    elif selection.result == Selection.Result.DRAW_SAFE:
        unlock_achievement(
            user,
            "week_one_survivor",
        )

        unlock_achievement(
            user,
            "joker_saved_me",
        )