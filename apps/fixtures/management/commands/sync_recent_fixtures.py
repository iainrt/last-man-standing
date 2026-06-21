from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from apps.fixtures.models import Match, Season, Team
from apps.fixtures.services.api_football import api_football_get


API_STATUS_MAP = {
    "TBD": Match.Status.SCHEDULED,
    "NS": Match.Status.SCHEDULED,
    "1H": Match.Status.IN_PLAY,
    "HT": Match.Status.IN_PLAY,
    "2H": Match.Status.IN_PLAY,
    "ET": Match.Status.IN_PLAY,
    "BT": Match.Status.IN_PLAY,
    "P": Match.Status.IN_PLAY,
    "SUSP": Match.Status.POSTPONED,
    "INT": Match.Status.POSTPONED,
    "FT": Match.Status.FINISHED,
    "AET": Match.Status.FINISHED,
    "PEN": Match.Status.FINISHED,
    "PST": Match.Status.POSTPONED,
    "CANC": Match.Status.CANCELLED,
    "ABD": Match.Status.CANCELLED,
    "AWD": Match.Status.FINISHED,
    "WO": Match.Status.FINISHED,
}


def get_winner(home_goals, away_goals):
    if home_goals is None or away_goals is None:
        return None

    if home_goals > away_goals:
        return Match.Winner.HOME

    if away_goals > home_goals:
        return Match.Winner.AWAY

    return Match.Winner.DRAW


class Command(BaseCommand):
    help = "Sync recent and upcoming fixtures from API-FOOTBALL"

    def handle(self, *args, **options):
        today = timezone.now().date()

        date_from = today - timedelta(days=3)
        date_to = today + timedelta(days=14)

        seasons = Season.objects.filter(
            is_active=True,
        ).select_related("league")

        if not seasons.exists():
            self.stdout.write(
                self.style.WARNING(
                    "No active seasons found. Run sync_seasons first."
                )
            )
            return

        total_created = 0
        total_updated = 0
        total_skipped = 0

        for season in seasons:
            self.stdout.write(
                f"Syncing recent fixtures for {season} "
                f"from {date_from} to {date_to}..."
            )

            data = api_football_get(
                "fixtures",
                params={
                    "league": season.league.api_id,
                    "season": season.api_season,
                    "from": date_from.isoformat(),
                    "to": date_to.isoformat(),
                },
            )

            for item in data.get("response", []):
                fixture_data = item["fixture"]
                league_data = item["league"]
                teams_data = item["teams"]
                goals_data = item["goals"]

                round_name = league_data.get("round", "")

                gameweek = season.gameweeks.filter(
                    name=round_name,
                ).first()

                if gameweek is None:
                    self.stdout.write(
                        self.style.WARNING(
                            f"  Skipping fixture {fixture_data['id']}: "
                            f"no gameweek for '{round_name}'"
                        )
                    )
                    total_skipped += 1
                    continue

                home_team_api_id = teams_data["home"]["id"]
                away_team_api_id = teams_data["away"]["id"]

                try:
                    home_team = Team.objects.get(api_id=home_team_api_id)
                    away_team = Team.objects.get(api_id=away_team_api_id)
                except Team.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(
                            f"  Skipping fixture {fixture_data['id']}: missing team"
                        )
                    )
                    total_skipped += 1
                    continue

                status_short = fixture_data["status"]["short"]
                status = API_STATUS_MAP.get(
                    status_short,
                    Match.Status.SCHEDULED,
                )

                home_score = goals_data.get("home")
                away_score = goals_data.get("away")

                winner = get_winner(home_score, away_score)

                kickoff_at = parse_datetime(fixture_data["date"])

                _, created = Match.objects.update_or_create(
                    api_id=fixture_data["id"],
                    defaults={
                        "gameweek": gameweek,
                        "home_team": home_team,
                        "away_team": away_team,
                        "kickoff_at": kickoff_at,
                        "status": status,
                        "home_score": home_score,
                        "away_score": away_score,
                        "winner": winner,
                    },
                )

                if created:
                    total_created += 1
                else:
                    total_updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Recent fixture sync complete. "
                f"Created: {total_created}, "
                f"Updated: {total_updated}, "
                f"Skipped: {total_skipped}"
            )
        )