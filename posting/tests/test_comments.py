from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from ..models import Comment, CommentVote, Post

User = get_user_model()


class CommentModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="commenter",
            email="commenter@yale.edu",
            password="password123",
        )
        self.post = Post.objects.create(
            title="Test Post",
            body="Test body",
            author=self.user,
        )

    def test_create_comment(self):
        """Test creating a top-level comment."""
        comment = Comment.objects.create(
            post=self.post,
            body="Test comment",
            author=self.user,
            is_anonymous=False,
        )
        self.assertEqual(comment.post, self.post)
        self.assertEqual(comment.body, "Test comment")
        self.assertFalse(comment.is_reply())
        self.assertEqual(self.post.comments.count(), 1)

    def test_create_reply(self):
        """Test creating a reply to a comment."""
        parent = Comment.objects.create(
            post=self.post,
            body="Parent comment",
            author=self.user,
        )
        reply = Comment.objects.create(
            post=self.post,
            parent_comment=parent,
            body="Reply comment",
            author=self.user,
        )
        self.assertTrue(reply.is_reply())
        self.assertEqual(reply.parent_comment, parent)
        self.assertEqual(parent.replies.count(), 1)

    def test_soft_delete(self):
        """Test soft delete preserves comment but hides content."""
        comment = Comment.objects.create(
            post=self.post,
            body="To be deleted",
            author=self.user,
        )
        comment.is_deleted = True
        comment.save()

        # Comment still exists in DB
        self.assertTrue(Comment.objects.filter(pk=comment.pk).exists())
        self.assertTrue(comment.is_deleted)

    def test_comment_vote_counts(self):
        """Test vote counting methods."""
        comment = Comment.objects.create(
            post=self.post,
            body="Test",
            author=self.user,
        )
        other_user = User.objects.create_user(
            username="other",
            email="other@yale.edu",
            password="password123",
        )

        CommentVote.objects.create(
            comment=comment, voter=self.user, vote_type=CommentVote.UPVOTE
        )
        CommentVote.objects.create(
            comment=comment, voter=other_user, vote_type=CommentVote.DOWNVOTE
        )

        self.assertEqual(comment.get_upvotes_count(), 1)
        self.assertEqual(comment.get_downvotes_count(), 1)
        self.assertEqual(comment.get_net_votes(), 0)


class CommentViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="commenter",
            email="commenter@yale.edu",
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

    def test_add_comment_requires_login(self):
        """Test that adding a comment requires authentication."""
        response = self.client.post(
            reverse("posting:add_comment", args=[self.post.pk]),
            {"body": "Test comment", "is_anonymous": True},
        )
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_add_comment_success(self):
        """Test adding a comment to a post."""
        self.client.login(username="commenter", password="password123")
        response = self.client.post(
            reverse("posting:add_comment", args=[self.post.pk]),
            {"body": "Test comment", "is_anonymous": True},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.first()
        self.assertEqual(comment.body, "Test comment")
        self.assertEqual(comment.post, self.post)
        self.assertTrue(comment.is_anonymous)

    def test_add_reply_success(self):
        """Test adding a reply to a comment."""
        parent = Comment.objects.create(
            post=self.post,
            body="Parent",
            author=self.user,
        )
        self.client.login(username="other", password="password123")
        response = self.client.post(
            reverse("posting:add_reply", args=[parent.pk]),
            {"body": "Reply", "is_anonymous": False},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 2)
        reply = Comment.objects.get(parent_comment=parent)
        self.assertEqual(reply.body, "Reply")
        self.assertFalse(reply.is_anonymous)

    def test_upvote_comment_toggle(self):
        """Test upvoting a comment with toggle behavior."""
        comment = Comment.objects.create(
            post=self.post,
            body="Test",
            author=self.user,
        )
        self.client.login(username="other", password="password123")

        # First upvote
        response = self.client.post(
            reverse("posting:upvote_comment", args=[comment.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(CommentVote.objects.count(), 1)
        self.assertEqual(comment.get_net_votes(), 1)

        # Toggle off
        response = self.client.post(
            reverse("posting:upvote_comment", args=[comment.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(CommentVote.objects.count(), 0)
        self.assertEqual(comment.get_net_votes(), 0)

    def test_switch_vote_type(self):
        """Test switching from downvote to upvote."""
        comment = Comment.objects.create(
            post=self.post,
            body="Test",
            author=self.user,
        )
        CommentVote.objects.create(
            comment=comment, voter=self.other_user, vote_type=CommentVote.DOWNVOTE
        )
        self.client.login(username="other", password="password123")

        response = self.client.post(
            reverse("posting:upvote_comment", args=[comment.pk])
        )
        self.assertEqual(response.status_code, 302)
        vote = CommentVote.objects.get(comment=comment, voter=self.other_user)
        self.assertEqual(vote.vote_type, CommentVote.UPVOTE)

    def test_flag_comment(self):
        """Test flagging a comment."""
        comment = Comment.objects.create(
            post=self.post,
            body="Test",
            author=self.user,
        )
        self.client.login(username="other", password="password123")

        response = self.client.post(
            reverse("posting:flag_comment", args=[comment.pk])
        )
        self.assertEqual(response.status_code, 302)
        comment.refresh_from_db()
        self.assertTrue(comment.is_flagged)

    def test_delete_own_comment(self):
        """Test user can delete their own comment."""
        comment = Comment.objects.create(
            post=self.post,
            body="My comment",
            author=self.user,
        )
        self.client.login(username="commenter", password="password123")

        response = self.client.post(
            reverse("posting:delete_comment", args=[comment.pk])
        )
        self.assertEqual(response.status_code, 302)
        comment.refresh_from_db()
        self.assertTrue(comment.is_deleted)

    def test_cannot_delete_others_comment(self):
        """Test user cannot delete another user's comment."""
        comment = Comment.objects.create(
            post=self.post,
            body="Other's comment",
            author=self.user,
        )
        self.client.login(username="other", password="password123")

        response = self.client.post(
            reverse("posting:delete_comment", args=[comment.pk])
        )
        comment.refresh_from_db()
        self.assertFalse(comment.is_deleted)  # Should not be deleted

    def test_staff_can_delete_any_comment(self):
        """Test staff users can delete any comment."""
        comment = Comment.objects.create(
            post=self.post,
            body="User comment",
            author=self.user,
        )
        staff_user = User.objects.create_user(
            username="staff",
            email="staff@yale.edu",
            password="password123",
            is_staff=True,
        )
        self.client.login(username="staff", password="password123")

        response = self.client.post(
            reverse("posting:delete_comment", args=[comment.pk])
        )
        comment.refresh_from_db()
        self.assertTrue(comment.is_deleted)
