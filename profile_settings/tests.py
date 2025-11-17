from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from posting.models import Post, Tag

User = get_user_model()


class ProfileSettingsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="profileuser",
            email="profile@yale.edu",
            password="password123",
        )
        self.other_user = get_user_model().objects.create_user(
            username="otheruser",
            email="other@yale.edu",
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

    def test_my_posts_requires_login(self):
        """Test that my_posts redirects to login when not authenticated."""
        response = self.client.get(reverse("profile_settings:my_posts"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("auth_landing:login"), response.url)

    def test_my_posts_shows_user_posts(self):
        """Test that my_posts shows only the logged-in user's posts."""
        self.client.login(username="profileuser", password="password123")
        
        # Create posts by this user
        post1 = Post.objects.create(
            title="My First Post",
            body="Body of first post",
            author=self.user,
            is_anonymous=False,
        )
        post2 = Post.objects.create(
            title="My Anonymous Post",
            body="Body of anonymous post",
            author=self.user,
            is_anonymous=True,
        )
        
        # Create post by other user (should not appear)
        Post.objects.create(
            title="Other User's Post",
            body="Body",
            author=self.other_user,
        )
        
        response = self.client.get(reverse("profile_settings:my_posts"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "My First Post")
        self.assertContains(response, "My Anonymous Post")
        self.assertNotContains(response, "Other User's Post")
        self.assertContains(response, "Anonymous")

    def test_my_posts_empty_state(self):
        """Test empty state when user has no posts."""
        self.client.login(username="profileuser", password="password123")
        response = self.client.get(reverse("profile_settings:my_posts"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You haven't posted anything yet")
        self.assertContains(response, "Create Your First Post")

    def test_my_posts_shows_anonymous_badge(self):
        """Test that anonymous posts show the anonymous badge."""
        self.client.login(username="profileuser", password="password123")
        Post.objects.create(
            title="Anonymous Post",
            body="Body",
            author=self.user,
            is_anonymous=True,
        )
        response = self.client.get(reverse("profile_settings:my_posts"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Anonymous")

    def test_settings_requires_login(self):
        """Test that settings redirects to login when not authenticated."""
        response = self.client.get(reverse("profile_settings:settings"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("auth_landing:login"), response.url)

    def test_settings_authenticated(self):
        """Test that settings page loads for authenticated users."""
        self.client.login(username="profileuser", password="password123")
        response = self.client.get(reverse("profile_settings:settings"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Settings")
        self.assertContains(response, "Change Password")
        self.assertContains(response, "Email Preferences")
        self.assertContains(response, "Terms of Service")
        self.assertContains(response, "Privacy Policy")
        self.assertContains(response, "Help & Feedback")
        self.assertContains(response, "App Version")

    def test_change_password_requires_login(self):
        """Test that change_password redirects to login when not authenticated."""
        response = self.client.get(reverse("profile_settings:change_password"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("auth_landing:login"), response.url)

    def test_change_password_get(self):
        """Test that change password form displays."""
        self.client.login(username="profileuser", password="password123")
        response = self.client.get(reverse("profile_settings:change_password"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Change Password")
        self.assertContains(response, "Current Password")
        self.assertContains(response, "New Password")

    def test_change_password_success(self):
        """Test successful password change."""
        self.client.login(username="profileuser", password="password123")
        response = self.client.post(
            reverse("profile_settings:change_password"),
            {
                "old_password": "password123",
                "new_password1": "newpassword456",
                "new_password2": "newpassword456",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("profile_settings:settings"))
        
        # Verify password was changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newpassword456"))

    def test_change_password_wrong_old_password(self):
        """Test password change fails with wrong old password."""
        self.client.login(username="profileuser", password="password123")
        response = self.client.post(
            reverse("profile_settings:change_password"),
            {
                "old_password": "wrongpassword",
                "new_password1": "newpassword456",
                "new_password2": "newpassword456",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "error")
        
        # Verify password was not changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("password123"))

    def test_change_password_mismatch(self):
        """Test password change fails when new passwords don't match."""
        self.client.login(username="profileuser", password="password123")
        response = self.client.post(
            reverse("profile_settings:change_password"),
            {
                "old_password": "password123",
                "new_password1": "newpassword456",
                "new_password2": "differentpassword",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "error")
        
        # Verify password was not changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("password123"))
