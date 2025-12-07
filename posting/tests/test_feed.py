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

    def test_home_page_requires_auth(self):
        """Test that home page redirects unauthenticated users."""
        response = self.client.get(reverse("posting:home"))
        self.assertEqual(response.status_code, 302)

    def test_home_page_renders(self):
        """Test that home page renders for authenticated users."""
        self.client.login(username="poster", password="password123")
        response = self.client.get(reverse("posting:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Share Your Thought")

