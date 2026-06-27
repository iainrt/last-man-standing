from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.competitions.models import Competition, CompetitionGameweek


class Command(BaseCommand):
    help = "Run automated fixture sync and result processing"

    def handle(self, *args, **options):
        self.stdout.write("Starting automated sync...")

        self.stdout.write("Syncing recent fixtures...")
        call_command("sync_recent_fixtures")

        self.stdout.write("Processing results...")
        call_command("process_results")

        self.stdout.write("Locking competitions after week 1 deadline...")
        now = timezone.now()

        week_one_gameweeks = CompetitionGameweek.objects.filter(
            competition_week_number=1,
            is_published=True,
            deadline__lte=now,
            competition__is_locked=False,
        ).select_related("competition")

        locked_count = 0

        for competition_gameweek in week_one_gameweeks:
            competition_gameweek.competition.lock()
            locked_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Locked {locked_count} competitions after week 1 deadline."
            )
        )

        self.stdout.write(
            self.style.SUCCESS("Automated sync complete.")
        )