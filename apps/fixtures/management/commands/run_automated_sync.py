from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Run automated fixture sync and result processing"

    def handle(self, *args, **options):
        self.stdout.write("Starting automated sync...")

        self.stdout.write("Syncing fixtures...")
        call_command("sync_fixtures")

        self.stdout.write("Processing results...")
        call_command("process_results")

        self.stdout.write(
            self.style.SUCCESS(
                "Automated sync complete."
            )
        )