from django.core.management.base import BaseCommand
from django.conf import settings

from apps.fixtures.models import League, Season
from apps.fixtures.services.api_football import api_football_get


class Command(BaseCommand):
    help = "Sync seasons from API-FOOTBALL"

    def handle(self, *args, **options):

        for league in League.objects.all():

            data = api_football_get(
                "leagues",
                params={
                    "id": league.api_id,
                    "season": settings.CURRENT_API_SEASON,
                },
            )

            response = data.get("response", [])

            if not response:
                continue

            season_year = response[0]["seasons"][-1]["year"]

            season_name = f"{season_year}/{str(season_year + 1)[-2:]}"

            season, created = Season.objects.update_or_create(
                league=league,
                api_season=season_year,
                defaults={
                    "name": season_name,
                    "is_active": True,
                },
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f"{season} synced"
                )
            )