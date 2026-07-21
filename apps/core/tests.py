from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AdminNavigationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            username="normal-user",
            password="test-password",
        )
        cls.competition_admin = User.objects.create_user(
            username="competition-admin",
            password="test-password",
        )
        cls.competition_admin.profile.can_create_competitions = True
        cls.competition_admin.profile.save()
        cls.superuser = User.objects.create_superuser(
            username="superuser",
            email="superuser@example.com",
            password="test-password",
        )

    def assert_admin_link_not_visible(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(
            response,
            f'href="{reverse("admin:index")}"',
        )

    def test_anonymous_user_cannot_see_admin_link(self):
        response = self.client.get(reverse("home"))

        self.assert_admin_link_not_visible(response)

    def test_normal_authenticated_user_cannot_see_admin_link(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("home"))

        self.assert_admin_link_not_visible(response)

    def test_competition_admin_cannot_see_admin_link(self):
        self.client.force_login(self.competition_admin)

        response = self.client.get(reverse("home"))

        self.assert_admin_link_not_visible(response)

    def test_superuser_can_see_admin_link(self):
        self.client.force_login(self.superuser)

        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            f'href="{reverse("admin:index")}"',
        )
        self.assertContains(response, "Admin")
