from django.conf import settings
from django.core.management.base import BaseCommand

from apps.fixtures.models import League, Season, Team, SeasonTeam
from apps.fixtures.services.api_football import api_football_get


class Command(BaseCommand):
    help = "Sync teams from API-FOOTBALL for the current season"

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
            self.stdout.write(
                f"Syncing teams for {season}..."
            )

            data = api_football_get(
                "teams",
                params={
                    "league": season.league.api_id,
                    "season": season.api_season,
                },
            )

            for item in data.get("response", []):
                team_data = item["team"]

                team, created = Team.objects.update_or_create(
                    api_id=team_data["id"],
                    defaults={
                        "name": team_data["name"],
                        "short_name": team_data["name"][:50],
                        "crest_url": team_data.get("logo"),
                    },
                )

                SeasonTeam.objects.get_or_create(
                    season=season,
                    team=team,
                )

                status = "created" if created else "updated"

                self.stdout.write(
                    self.style.SUCCESS(
                        f"  {team.name} {status}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS("Team sync complete.")
        )