from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from ..models import Post, Tag


class PostFormTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="poster",
            email="poster@yale.edu",
            password="password123",
        )
        self.tag = Tag.objects.create(name="General", slug="general")

    def test_post_requires_authentication(self):
        response = self.client.post(
            reverse("posting:home"),
            data={
                "title": "Hello",
                "body": "Test body",
                "is_anonymous": True,
                "tags": [self.tag.pk],
            },
        )
        self.assertEqual(response.status_code, 302)
        # Redirects to landing page for unauthenticated users
        self.assertIn("auth", response.url)

    def test_authenticated_post_submission(self):
        self.client.login(username="poster", password="password123")
        response = self.client.post(
            reverse("posting:home"),
            data={
                "title": "Hello",
                "body": "Test body",
                "is_anonymous": True,
                "tags": [self.tag.pk],
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Post.objects.filter(title="Hello").exists())

