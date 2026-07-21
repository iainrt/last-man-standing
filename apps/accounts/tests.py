from django.contrib.auth.models import User
from django.test import TestCase

from apps.fixtures.models import Team

from .forms import ProfileForm


class ProfileFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="profile-user",
            password="test-password",
        )
        self.liverpool = Team.objects.create(
            name="Liverpool",
            short_name="Liverpool",
        )
        self.arsenal = Team.objects.create(
            name="Arsenal",
            short_name="Arsenal",
        )
        self.chelsea = Team.objects.create(
            name="Chelsea",
            short_name="Chelsea",
        )

    def test_favourite_team_choices_are_alphabetical_with_blank_option(self):
        form = ProfileForm(instance=self.user.profile)

        choices = list(form.fields["favourite_team"].choices)

        self.assertFalse(form.fields["favourite_team"].required)
        self.assertEqual(choices[0], ("", "---------"))
        self.assertEqual(
            [label for value, label in choices[1:]],
            ["Arsenal", "Chelsea", "Liverpool"],
        )

    def test_existing_favourite_team_can_be_loaded_and_saved(self):
        profile = self.user.profile
        profile.favourite_team = self.chelsea
        profile.save()

        form = ProfileForm(instance=profile)

        self.assertEqual(form["favourite_team"].value(), self.chelsea.pk)

        form = ProfileForm(
            data={
                "screen_name": profile.screen_name,
                "favourite_team": self.chelsea.pk,
                "is_public": "on",
            },
            instance=profile,
        )

        self.assertTrue(form.is_valid(), form.errors)
        form.save()
        profile.refresh_from_db()
        self.assertEqual(profile.favourite_team, self.chelsea)
