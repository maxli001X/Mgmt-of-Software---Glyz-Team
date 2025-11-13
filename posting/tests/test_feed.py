from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from ..models import Tag


class FeedViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="poster",
            email="poster@yale.edu",
            password="password123",
        )
        self.tag = Tag.objects.create(name="General", slug="general")

    def test_home_page_renders(self):
        response = self.client.get(reverse("posting:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Share Your Thoughts")

