from django.core.management.base import BaseCommand

from apps.achievements.models import Achievement

from django.utils import timezone

V09_TRACKING_START = timezone.datetime(
    2026, 7, 5, 0, 0,
    tzinfo=timezone.get_current_timezone(),
)


ACHIEVEMENTS = [
    {
        "code": "first_pick",
        "name": "First Pick",
        "description": "Make your first Last Man Standing pick.",
        "discovery": Achievement.Discovery.VISIBLE,
        "category": Achievement.Category.PICKS,
        "difficulty": Achievement.Difficulty.BRONZE,
        "xp_reward": 10,
        "icon": "🎯",
        "clue": "",
        "target": 1,
        "tracking_start": V09_TRACKING_START,
    },
    {
        "code": "week_one_survivor",
        "name": "Week One Survivor",
        "description": "Survive your first competition week.",
        "discovery": Achievement.Discovery.VISIBLE,
        "category": Achievement.Category.COMPETITION,
        "difficulty": Achievement.Difficulty.BRONZE,
        "xp_reward": 10,
        "icon": "✅",
        "clue": "",
        "target": 1,
        "tracking_start": V09_TRACKING_START,
    },
    {
        "code": "joker_played",
        "name": "Joker Played",
        "description": "Use a joker in a competition.",
        "discovery": Achievement.Discovery.VISIBLE,
        "category": Achievement.Category.JOKER,
        "difficulty": Achievement.Difficulty.BRONZE,
        "xp_reward": 10,
        "icon": "🃏",
        "clue": "",
        "target": 1,
        "tracking_start": V09_TRACKING_START,
    },
    {
        "code": "joker_saved_me",
        "name": "Joker Saved Me",
        "description": "Survive a draw by using your joker.",
        "discovery": Achievement.Discovery.VISIBLE,
        "category": Achievement.Category.JOKER,
        "difficulty": Achievement.Difficulty.SILVER,
        "xp_reward": 20,
        "icon": "🃏",
        "clue": "",
        "target": 1,
        "tracking_start": V09_TRACKING_START,
    },
    {
        "code": "competition_winner",
        "name": "Competition Winner",
        "description": "Win a Last Man Standing competition.",
        "discovery": Achievement.Discovery.VISIBLE,
        "category": Achievement.Category.COMPETITION,
        "difficulty": Achievement.Difficulty.GOLD,
        "xp_reward": 50,
        "icon": "🏆",
        "clue": "",
        "target": 1,
        "tracking_start": V09_TRACKING_START,
    },
    {
        "code": "joint_winner",
        "name": "Joint Winner",
        "description": "Share victory in a Last Man Standing competition.",
        "discovery": Achievement.Discovery.VISIBLE,
        "category": Achievement.Category.COMPETITION,
        "difficulty": Achievement.Difficulty.SILVER,
        "xp_reward": 30,
        "icon": "🤝",
        "clue": "",
        "target": 1,
        "tracking_start": V09_TRACKING_START,
    },
    {
        "code": "perfect_start",
        "name": "Perfect Start",
        "description": "Survive your first three competition weeks.",
        "discovery": Achievement.Discovery.HIDDEN,
        "category": Achievement.Category.COMPETITION,
        "difficulty": Achievement.Difficulty.SILVER,
        "xp_reward": 25,
        "icon": "🔥",
        "clue": "Start strong.",
        "target": 3,
        "tracking_start": V09_TRACKING_START,
    },
    {
        "code": "popular_choice",
        "name": "Popular Choice",
        "description": "Pick the most popular team in a gameweek and survive.",
        "discovery": Achievement.Discovery.HIDDEN,
        "category": Achievement.Category.PICKS,
        "difficulty": Achievement.Difficulty.SILVER,
        "xp_reward": 25,
        "icon": "👥",
        "clue": "Sometimes the crowd is right.",
        "target": 1,
        "tracking_start": V09_TRACKING_START,
    },
    {
        "code": "against_the_crowd",
        "name": "Against the Crowd",
        "description": "Pick a team nobody else picked and survive.",
        "discovery": Achievement.Discovery.HIDDEN,
        "category": Achievement.Category.PICKS,
        "difficulty": Achievement.Difficulty.SILVER,
        "xp_reward": 25,
        "icon": "🧭",
        "clue": "Stand alone and survive.",
        "target": 1,
        "tracking_start": V09_TRACKING_START,
    },
]


class Command(BaseCommand):
    help = "Seed starter achievements"

    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0

        for achievement_data in ACHIEVEMENTS:
            achievement, created = Achievement.objects.update_or_create(
                code=achievement_data["code"],
                defaults=achievement_data,
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Achievements seeded. Created: {created_count}, Updated: {updated_count}"
            )
        )