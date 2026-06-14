from django.core.management.base import BaseCommand
from django.conf import settings

from apps.fixtures.models import League
from apps.fixtures.services.api_football import api_football_get


LEAGUES = [
    {"api_id": 39, "name": "Premier League", "country": "England"},
    {"api_id": 40, "name": "Championship", "country": "England"},
    {"api_id": 41, "name": "League One", "country": "England"},
    {"api_id": 42, "name": "League Two", "country": "England"},
    {"api_id": 357, "name": "Premier Division", "country": "Ireland"},
]


class Command(BaseCommand):
    help = "Sync selected leagues from API-FOOTBALL"

    def handle(self, *args, **options):
        season = settings.CURRENT_API_SEASON

        for league_config in LEAGUES:
            data = api_football_get(
                "leagues",
                params={
                    "id": league_config["api_id"],
                    "season": season,
                },
            )

            response_items = data.get("response", [])

            if not response_items:
                self.stdout.write(
                    self.style.WARNING(
                        f"No API response for league {league_config['name']}"
                    )
                )
                continue

            item = response_items[0]
            league_data = item["league"]
            country_data = item["country"]

            league, created = League.objects.update_or_create(
                api_id=league_data["id"],
                defaults={
                    "name": league_data["name"],
                    "country": country_data["name"],
                    "logo_url": league_data.get("logo"),
                },
            )

            status = "created" if created else "updated"

            self.stdout.write(
                self.style.SUCCESS(
                    f"{league.name} ({league.api_id}) {status}"
                )
            )