import re
from collections import defaultdict
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.fixtures.models import Season, Gameweek
from apps.fixtures.services.api_football import api_football_get


def extract_gameweek_number(round_name):
    match = re.search(r"(\d+)$", round_name)

    if match:
        return int(match.group(1))

    return None


class Command(BaseCommand):
    help = "Sync gameweeks from API-FOOTBALL fixture rounds"

    def handle(self, *args, **options):
        api_season = settings.CURRENT_API_SEASON

        seasons = Season.objects.filter(
            api_season=api_season,
            is_active=True,
        ).select_related("league")

        if not seasons.exists():
            self.stdout.write(
                self.style.WARNING(
                    "No active seasons found. Run sync_seasons first."
                )
            )
            return

        for season in seasons:
            self.stdout.write(f"Syncing gameweeks for {season}...")

            data = api_football_get(
                "fixtures",
                params={
                    "league": season.league.api_id,
                    "season": season.api_season,
                },
            )

            rounds = defaultdict(list)

            for item in data.get("response", []):
                fixture = item["fixture"]
                league_data = item["league"]

                round_name = league_data.get("round")

                if not round_name:
                    continue

                rounds[round_name].append(fixture["date"])

            if not rounds:
                self.stdout.write(
                    self.style.WARNING(
                        f"No rounds found for {season}"
                    )
                )
                continue

            for round_name, kickoff_dates in rounds.items():
                number = extract_gameweek_number(round_name)

                if number is None:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Could not extract gameweek number from '{round_name}'"
                        )
                    )
                    continue

                earliest_kickoff = min(kickoff_dates)

                deadline = earliest_kickoff

                gameweek, created = Gameweek.objects.update_or_create(
                    season=season,
                    number=number,
                    defaults={
                        "name": round_name,
                        "deadline": deadline,
                    },
                )

                status = "created" if created else "updated"

                self.stdout.write(
                    self.style.SUCCESS(
                        f"  {gameweek} {status}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS("Gameweek sync complete.")
        )