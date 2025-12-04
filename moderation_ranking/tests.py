from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from posting.models import Comment, Post

User = get_user_model()


class ModerationDashboardTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="moderator",
            email="moderator@yale.edu",
            password="password123",
        )

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("moderation_ranking:dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("auth_landing:login"), response.url)

    def test_dashboard_authenticated(self):
        self.client.login(username="moderator", password="password123")
        response = self.client.get(reverse("moderation_ranking:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Moderation Dashboard")


class FlaggedQueueTests(TestCase):
    def setUp(self):
        self.regular_user = User.objects.create_user(
            username="regular",
            email="regular@yale.edu",
            password="password123",
        )
        self.staff_user = User.objects.create_user(
            username="staff",
            email="staff@yale.edu",
            password="password123",
            is_staff=True,
        )
        self.post = Post.objects.create(
            title="Test Post",
            body="Test body",
            author=self.regular_user,
            is_flagged=True,
        )
        self.comment = Comment.objects.create(
            post=self.post,
            body="Flagged comment",
            author=self.regular_user,
            is_flagged=True,
        )

    def test_flagged_queue_requires_staff(self):
        """Non-staff users should get 403."""
        self.client.login(username="regular", password="password123")
        response = self.client.get(reverse("moderation_ranking:flagged_queue"))
        self.assertEqual(response.status_code, 403)

    def test_flagged_queue_staff_access(self):
        """Staff users can access the flagged queue."""
        self.client.login(username="staff", password="password123")
        response = self.client.get(reverse("moderation_ranking:flagged_queue"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Moderation Queue")
        self.assertContains(response, "Test Post")
        self.assertContains(response, "Flagged comment")


class PostModerationTests(TestCase):
    def setUp(self):
        self.regular_user = User.objects.create_user(
            username="regular",
            email="regular@yale.edu",
            password="password123",
        )
        self.staff_user = User.objects.create_user(
            username="staff",
            email="staff@yale.edu",
            password="password123",
            is_staff=True,
        )
        self.post = Post.objects.create(
            title="Test Post",
            body="Test body",
            author=self.regular_user,
            is_flagged=True,
        )

    def test_unflag_post_requires_staff(self):
        """Non-staff cannot unflag posts."""
        self.client.login(username="regular", password="password123")
        response = self.client.post(
            reverse("moderation_ranking:unflag_post", args=[self.post.pk])
        )
        self.assertEqual(response.status_code, 403)

    def test_unflag_post_success(self):
        """Staff can unflag posts."""
        self.client.login(username="staff", password="password123")
        response = self.client.post(
            reverse("moderation_ranking:unflag_post", args=[self.post.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertFalse(self.post.is_flagged)

    def test_hide_post_success(self):
        """Staff can hide posts."""
        self.client.login(username="staff", password="password123")
        response = self.client.post(
            reverse("moderation_ranking:hide_post", args=[self.post.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertTrue(self.post.is_hidden)
        self.assertFalse(self.post.is_flagged)  # Auto-unflagged

    def test_unhide_post_success(self):
        """Staff can unhide posts."""
        self.post.is_hidden = True
        self.post.save()
        self.client.login(username="staff", password="password123")
        response = self.client.post(
            reverse("moderation_ranking:unhide_post", args=[self.post.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertFalse(self.post.is_hidden)

    def test_delete_post_success(self):
        """Staff can permanently delete posts."""
        post_pk = self.post.pk
        self.client.login(username="staff", password="password123")
        response = self.client.post(
            reverse("moderation_ranking:delete_post", args=[post_pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(pk=post_pk).exists())

    def test_get_request_redirects(self):
        """GET requests to moderation actions should redirect."""
        self.client.login(username="staff", password="password123")
        response = self.client.get(
            reverse("moderation_ranking:unflag_post", args=[self.post.pk])
        )
        self.assertEqual(response.status_code, 302)
        # Post should still be flagged
        self.post.refresh_from_db()
        self.assertTrue(self.post.is_flagged)


class CommentModerationTests(TestCase):
    def setUp(self):
        self.regular_user = User.objects.create_user(
            username="regular",
            email="regular@yale.edu",
            password="password123",
        )
        self.staff_user = User.objects.create_user(
            username="staff",
            email="staff@yale.edu",
            password="password123",
            is_staff=True,
        )
        self.post = Post.objects.create(
            title="Test Post",
            body="Test body",
            author=self.regular_user,
        )
        self.comment = Comment.objects.create(
            post=self.post,
            body="Flagged comment",
            author=self.regular_user,
            is_flagged=True,
        )

    def test_unflag_comment_requires_staff(self):
        """Non-staff cannot unflag comments."""
        self.client.login(username="regular", password="password123")
        response = self.client.post(
            reverse("moderation_ranking:unflag_comment", args=[self.comment.pk])
        )
        self.assertEqual(response.status_code, 403)

    def test_unflag_comment_success(self):
        """Staff can unflag comments."""
        self.client.login(username="staff", password="password123")
        response = self.client.post(
            reverse("moderation_ranking:unflag_comment", args=[self.comment.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.comment.refresh_from_db()
        self.assertFalse(self.comment.is_flagged)

    def test_hide_comment_success(self):
        """Staff can hide (soft-delete) comments."""
        self.client.login(username="staff", password="password123")
        response = self.client.post(
            reverse("moderation_ranking:hide_comment", args=[self.comment.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.comment.refresh_from_db()
        self.assertTrue(self.comment.is_deleted)
        self.assertFalse(self.comment.is_flagged)  # Auto-unflagged

    def test_unhide_comment_success(self):
        """Staff can unhide (restore) comments."""
        self.comment.is_deleted = True
        self.comment.save()
        self.client.login(username="staff", password="password123")
        response = self.client.post(
            reverse("moderation_ranking:unhide_comment", args=[self.comment.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.comment.refresh_from_db()
        self.assertFalse(self.comment.is_deleted)

    def test_delete_comment_success(self):
        """Staff can permanently delete comments."""
        comment_pk = self.comment.pk
        self.client.login(username="staff", password="password123")
        response = self.client.post(
            reverse("moderation_ranking:delete_comment", args=[comment_pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Comment.objects.filter(pk=comment_pk).exists())


class DeletedCommentActionsTests(TestCase):
    """Test that actions on deleted comments are blocked."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="user",
            email="user@yale.edu",
            password="password123",
        )
        self.other_user = User.objects.create_user(
            username="other",
            email="other@yale.edu",
            password="password123",
        )
        self.post = Post.objects.create(
            title="Test Post",
            body="Test body",
            author=self.user,
        )
        self.deleted_comment = Comment.objects.create(
            post=self.post,
            body="Deleted comment",
            author=self.user,
            is_deleted=True,
        )

    def test_cannot_reply_to_deleted_comment(self):
        """Users cannot reply to deleted comments."""
        self.client.login(username="other", password="password123")
        response = self.client.post(
            reverse("posting:add_reply", args=[self.deleted_comment.pk]),
            {"body": "Reply to deleted", "is_anonymous": True},
        )
        self.assertEqual(response.status_code, 302)
        # No new comments should be created
        self.assertEqual(Comment.objects.filter(parent_comment=self.deleted_comment).count(), 0)

    def test_cannot_vote_on_deleted_comment(self):
        """Users cannot vote on deleted comments."""
        self.client.login(username="other", password="password123")
        response = self.client.post(
            reverse("posting:upvote_comment", args=[self.deleted_comment.pk])
        )
        self.assertEqual(response.status_code, 302)
        # No votes should be created
        self.assertEqual(self.deleted_comment.votes.count(), 0)

    def test_cannot_flag_deleted_comment(self):
        """Users cannot flag deleted comments."""
        self.client.login(username="other", password="password123")
        response = self.client.post(
            reverse("posting:flag_comment", args=[self.deleted_comment.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.deleted_comment.refresh_from_db()
        self.assertFalse(self.deleted_comment.is_flagged)
