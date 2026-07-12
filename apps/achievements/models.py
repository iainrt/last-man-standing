from django.conf import settings
from django.db import models


class Achievement(models.Model):
    class Discovery(models.TextChoices):
        VISIBLE = "VISIBLE", "Visible"
        HIDDEN = "HIDDEN", "Hidden"

    class Difficulty(models.TextChoices):
        BRONZE = "BRONZE", "Bronze"
        SILVER = "SILVER", "Silver"
        GOLD = "GOLD", "Gold"
        PLATINUM = "PLATINUM", "Platinum"
        LEGENDARY = "LEGENDARY", "Legendary"

    class Category(models.TextChoices):
        GENERAL = "GENERAL", "General"
        COMPETITION = "COMPETITION", "Competition"
        PICKS = "PICKS", "Picks"
        JOKER = "JOKER", "Joker"
        COLLECTION = "COLLECTION", "Collection"
        EXPLORATION = "EXPLORATION", "Exploration"
        SPECIAL = "SPECIAL", "Special"

    code = models.SlugField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()

    discovery = models.CharField(
        max_length=20,
        choices=Discovery.choices,
        default=Discovery.VISIBLE,
    )

    category = models.CharField(
        max_length=30,
        choices=Category.choices,
        default=Category.GENERAL,
    )

    difficulty = models.CharField(
        max_length=30,
        choices=Difficulty.choices,
        default=Difficulty.BRONZE,
    )

    display_order = models.PositiveIntegerField(default=1000)

    xp_reward = models.PositiveIntegerField(default=0)

    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Emoji or icon name used in the UI.",
    )

    clue = models.TextField(
        blank=True,
        help_text="Optional clue shown for hidden achievements.",
    )

    tracking_start = models.DateTimeField(
        null=True,
        blank=True,
        help_text=(
            "Only activity on or after this date counts "
            "towards this achievement."
        ),
    )

    target = models.PositiveIntegerField(
        default=1,
        help_text="Progress required to unlock this achievement.",
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = [
            "display_order",
            "category",
            "difficulty",
            "name",
        ]

    def __str__(self):
        return self.name


class UserAchievement(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="achievements",
    )

    achievement = models.ForeignKey(
        Achievement,
        on_delete=models.CASCADE,
        related_name="user_achievements",
    )

    progress = models.PositiveIntegerField(default=0)

    is_unlocked = models.BooleanField(default=False)

    unlocked_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    notification_seen_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        unique_together = ("user", "achievement")
        ordering = ["-unlocked_at", "achievement__name"]

    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"

    @property
    def progress_percentage(self):
        if self.achievement.target <= 0:
            return 0

        percentage = (self.progress / self.achievement.target) * 100

        return min(100, int(percentage))