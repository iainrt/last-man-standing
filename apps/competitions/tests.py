from html.parser import HTMLParser

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.fixtures.models import League, Season

from .models import Competition, CompetitionMember


class ElementTextParser(HTMLParser):
    def __init__(self, element_id):
        super().__init__()
        self.element_id = element_id
        self.depth = 0
        self.target_depth = None
        self.text = []

    def handle_starttag(self, tag, attrs):
        if dict(attrs).get("id") == self.element_id:
            self.target_depth = self.depth
        self.depth += 1

    def handle_endtag(self, tag):
        self.depth -= 1
        if self.target_depth == self.depth:
            self.target_depth = None

    def handle_data(self, data):
        if self.target_depth is not None:
            self.text.append(data)


class CompetitionDetailMetadataTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.creator = User.objects.create_user(
            username="creator-username",
            password="test-password",
        )
        cls.creator.profile.screen_name = "Creator Screen Name"
        cls.creator.profile.save()

        league = League.objects.create(
            api_id=1,
            name="Premier League",
        )
        season = Season.objects.create(
            name="2026/27",
            league=league,
            api_season=2026,
        )
        cls.competition = Competition.objects.create(
            name="Test Competition",
            season=season,
            created_by=cls.creator,
            invite_code="OPEN1234",
        )
        CompetitionMember.objects.create(
            competition=cls.competition,
            user=cls.creator,
            is_admin=True,
        )
        cls.detail_url = reverse(
            "competition_detail",
            args=[cls.competition.pk],
        )

    def setUp(self):
        self.client.force_login(self.creator)

    def get_information_card_text(self, response):
        parser = ElementTextParser("competition-information")
        parser.feed(response.content.decode())
        return " ".join(" ".join(parser.text).split())

    def test_open_competition_displays_metadata_in_main_card(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, 200)
        information = self.get_information_card_text(response)
        self.assertIn("Creator Screen Name", information)
        self.assertNotIn("creator-username", information)
        self.assertIn("Open", information)
        self.assertIn("OPEN1234", information)
        self.assertContains(response, "Created by:", count=1)
        self.assertContains(response, "Invite code:", count=1)

    def test_closed_competition_hides_invite_code(self):
        self.competition.is_locked = True
        self.competition.save(update_fields=["is_locked"])

        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, 200)
        information = self.get_information_card_text(response)
        self.assertIn("Closed", information)
        self.assertNotIn("🔒 Locked", information)
        self.assertNotContains(response, "OPEN1234")
        self.assertNotContains(response, "Invite code:")

    def test_blank_creator_screen_name_falls_back_to_username(self):
        self.creator.profile.screen_name = ""
        self.creator.profile.save()

        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, 200)
        information = self.get_information_card_text(response)
        self.assertIn("creator-username", information)
