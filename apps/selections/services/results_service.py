from apps.fixtures.models import Match
from apps.selections.models import Selection


def process_selection(selection):
    match = selection.match

    if match.status != Match.Status.FINISHED:
        return False

    if selection.processed:
        return False

    picked_home = selection.team_id == match.home_team_id
    picked_away = selection.team_id == match.away_team_id

    if not picked_home and not picked_away:
        return False

    if match.winner == Match.Winner.DRAW:
        if selection.is_joker:
            selection.result = Selection.Result.DRAW_SAFE
        else:
            selection.result = Selection.Result.DRAW_ELIMINATED
            selection.competition_member.is_eliminated = True

    elif match.winner == Match.Winner.HOME and picked_home:
        selection.result = Selection.Result.WIN

    elif match.winner == Match.Winner.AWAY and picked_away:
        selection.result = Selection.Result.WIN

    else:
        selection.result = Selection.Result.LOSE
        selection.competition_member.is_eliminated = True

    selection.processed = True
    selection.save(update_fields=["result", "processed"])

    selection.competition_member.save(update_fields=["is_eliminated"])

    return True


def process_pending_selections():
    selections = (
        Selection.objects
        .filter(
            processed=False,
            match__status=Match.Status.FINISHED,
        )
        .select_related(
            "match",
            "team",
            "competition_member",
        )
    )

    processed_count = 0

    for selection in selections:
        if process_selection(selection):
            processed_count += 1

    return processed_count