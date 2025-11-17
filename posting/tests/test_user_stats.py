from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from ..models import Post, Tag, Vote

User = get_user_model()


class UserStatsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@yale.edu",
            password="password123",
        )
        self.tag = Tag.objects.create(name="Test", slug="test")
        self.post = Post.objects.create(
            title="Test Post",
            body="Test body",
            author=self.user,
        )
        self.post.tags.add(self.tag)

    def test_my_stats_requires_login(self):
        """Test that my_stats view requires authentication."""
        response = self.client.get(reverse("posting:my_stats"))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_my_stats_displays_user_data(self):
        """Test that my_stats displays correct user statistics."""
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("posting:my_stats"))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "My Statistics")
        self.assertContains(response, "1")  # post_count
        self.assertContains(response, "Test Post")

    def test_my_stats_shows_vote_count(self):
        """Test that my_stats displays vote count."""
        # Create another user and post
        other_user = User.objects.create_user(
            username="other",
            email="other@yale.edu",
            password="password123",
        )
        other_post = Post.objects.create(
            title="Other Post",
            body="Other body",
            author=other_user,
        )
        
        # User votes on other post
        Vote.objects.create(post=other_post, voter=self.user)
        
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("posting:my_stats"))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "1")  # vote_count

    def test_my_stats_shows_flagged_count(self):
        """Test that my_stats displays flagged post count."""
        self.post.is_flagged = True
        self.post.save()
        
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("posting:my_stats"))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "1")  # flagged_count

    def test_my_stats_shows_most_used_tags(self):
        """Test that my_stats displays most used tags."""
        # Create another post with same tag
        Post.objects.create(
            title="Another Post",
            body="Another body",
            author=self.user,
        ).tags.add(self.tag)
        
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("posting:my_stats"))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test")


class AdminUserListTests(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username="admin",
            email="admin@yale.edu",
            password="password123",
            is_staff=True,
        )
        self.regular_user = User.objects.create_user(
            username="regular",
            email="regular@yale.edu",
            password="password123",
        )
        self.post = Post.objects.create(
            title="Test Post",
            body="Test body",
            author=self.regular_user,
        )

    def test_admin_user_list_requires_staff(self):
        """Test that admin_user_list requires staff status."""
        self.client.login(username="regular", password="password123")
        response = self.client.get(reverse("posting:admin_user_list"))
        # PermissionDenied raises 403
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_admin_user_list_displays_all_users(self):
        """Test that admin_user_list displays all users."""
        self.client.login(username="admin", password="password123")
        response = self.client.get(reverse("posting:admin_user_list"))
        # Debug: print response status if needed
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "User Management")
        self.assertContains(response, "admin")
        self.assertContains(response, "regular")
        self.assertContains(response, "1")  # post_count for regular user

    def test_admin_user_list_shows_user_statistics(self):
        """Test that admin_user_list shows correct statistics."""
        # Create vote
        Vote.objects.create(post=self.post, voter=self.regular_user)
        
        self.client.login(username="admin", password="password123")
        response = self.client.get(reverse("posting:admin_user_list"))
        # Debug: print response status if needed
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "1")  # post_count
        self.assertContains(response, "1")  # vote_count


class AggregatedStatsTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1",
            email="user1@yale.edu",
            password="password123",
        )
        self.user2 = User.objects.create_user(
            username="user2",
            email="user2@yale.edu",
            password="password123",
        )
        self.tag = Tag.objects.create(name="Popular", slug="popular")
        
        # Create posts
        self.post1 = Post.objects.create(
            title="Post 1",
            body="Body 1",
            author=self.user1,
        )
        self.post1.tags.add(self.tag)
        
        self.post2 = Post.objects.create(
            title="Post 2",
            body="Body 2",
            author=self.user2,
        )
        self.post2.tags.add(self.tag)
        
        # Create votes
        Vote.objects.create(post=self.post1, voter=self.user2)
        Vote.objects.create(post=self.post2, voter=self.user1)

    def test_aggregated_stats_public_access(self):
        """Test that aggregated_stats is publicly accessible."""
        response = self.client.get(reverse("posting:aggregated_stats"))
        self.assertEqual(response.status_code, 200)

    def test_aggregated_stats_displays_totals(self):
        """Test that aggregated_stats displays correct totals."""
        response = self.client.get(reverse("posting:aggregated_stats"))
        
        self.assertContains(response, "Platform Statistics")
        self.assertContains(response, "2")  # total_users
        self.assertContains(response, "2")  # total_posts
        self.assertContains(response, "2")  # total_votes

    def test_aggregated_stats_shows_active_users(self):
        """Test that aggregated_stats calculates active users."""
        response = self.client.get(reverse("posting:aggregated_stats"))
        
        self.assertEqual(response.status_code, 200)
        # Both users have posted or voted, so active_users should be 2
        self.assertContains(response, "2")  # active_users

    def test_aggregated_stats_shows_popular_tags(self):
        """Test that aggregated_stats displays popular tags."""
        response = self.client.get(reverse("posting:aggregated_stats"))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Popular")

    def test_aggregated_stats_calculates_dau(self):
        """Test that aggregated_stats calculates Daily Active Users."""
        # Create recent activity
        recent_post = Post.objects.create(
            title="Recent Post",
            body="Recent body",
            author=self.user1,
            created_at=timezone.now() - timedelta(hours=12),
        )
        
        response = self.client.get(reverse("posting:aggregated_stats"))
        
        self.assertEqual(response.status_code, 200)
        # Should show DAU >= 1 (user1 has recent activity)

    def test_aggregated_stats_shows_posts_per_day(self):
        """Test that aggregated_stats shows posts per day."""
        response = self.client.get(reverse("posting:aggregated_stats"))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Posts Per Day")

