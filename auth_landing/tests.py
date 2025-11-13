from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AuthLandingTests(TestCase):
    def test_signup_page_renders(self):
        response = self.client.get(reverse("auth_landing:signup"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create your Tree Hole Yale account")

    def test_signup_creates_user(self):
        response = self.client.post(
            reverse("auth_landing:signup"),
            data={
                "username": "newstudent",
                "email": "newstudent@yale.edu",
                "password1": "ComplexPass123!",
                "password2": "ComplexPass123!",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            get_user_model().objects.filter(username="newstudent").exists()
        )
