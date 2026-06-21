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

    member = selection.competition_member

    if match.winner == Match.Winner.DRAW:
        if selection.is_joker:
            selection.result = Selection.Result.DRAW_SAFE
        else:
            selection.result = Selection.Result.DRAW_ELIMINATED
            member.is_eliminated = True
            member.eliminated_in_competition_gameweek = (
                selection.competition_gameweek
            )

    elif match.winner == Match.Winner.HOME and picked_home:
        selection.result = Selection.Result.WIN

    elif match.winner == Match.Winner.AWAY and picked_away:
        selection.result = Selection.Result.WIN

    else:
        selection.result = Selection.Result.LOSE
        member.is_eliminated = True
        member.eliminated_in_competition_gameweek = (
            selection.competition_gameweek
        )

    selection.processed = True
    selection.save(update_fields=["result", "processed"])

    member.save(
        update_fields=[
            "is_eliminated",
            "eliminated_in_competition_gameweek",
        ]
    )

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