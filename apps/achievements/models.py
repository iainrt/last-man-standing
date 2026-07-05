from django.conf import settings
from django.db import models


class Achievement(models.Model):
    class Visibility(models.TextChoices):
        VISIBLE = "VISIBLE", "Visible"
        HIDDEN = "HIDDEN", "Hidden"

    code = models.SlugField(max_length=100, unique=True)

    name = models.CharField(max_length=100)

    description = models.TextField()

    visibility = models.CharField(
        max_length=20,
        choices=Visibility.choices,
        default=Visibility.VISIBLE,
    )

    clue = models.TextField(
        blank=True,
        help_text="Optional clue shown for hidden achievements.",
    )

    start_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Only activity after this date counts.",
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

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

    unlocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "achievement")
        ordering = ["-unlocked_at"]

    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"