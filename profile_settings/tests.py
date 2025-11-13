from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class ProfileSettingsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="profileuser",
            email="profile@yale.edu",
            password="password123",
        )

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("profile_settings:dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("auth_landing:login"), response.url)

    def test_dashboard_authenticated(self):
        self.client.login(username="profileuser", password="password123")
        response = self.client.get(reverse("profile_settings:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Profile & Settings")
