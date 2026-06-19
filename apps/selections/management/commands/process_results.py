from django.core.management.base import BaseCommand

from apps.selections.services.results_service import process_pending_selections


class Command(BaseCommand):
    help = "Process pending LMS selections against finished match results"

    def handle(self, *args, **options):
        processed_count = process_pending_selections()

        self.stdout.write(
            self.style.SUCCESS(
                f"Processed {processed_count} selections."
            )
        )