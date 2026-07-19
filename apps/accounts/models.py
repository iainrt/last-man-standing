from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    screen_name = models.CharField(
        max_length=50,
        unique=True,
    )

    favourite_team = models.ForeignKey(
        "fixtures.Team",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="supporters",
    )

    is_public = models.BooleanField(default=True)

    can_create_competitions = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.screen_name