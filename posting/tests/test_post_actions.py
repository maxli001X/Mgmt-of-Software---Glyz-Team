from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from ..models import Post, Tag, Vote

User = get_user_model()


class VoteTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="voter",
            email="voter@yale.edu",
            password="password123",
        )
        self.other_user = User.objects.create_user(
            username="other",
            email="other@yale.edu",
            password="password123",
        )
        self.tag = Tag.objects.create(name="Test", slug="test")
        self.post = Post.objects.create(
            title="Test Post",
            body="Test body",
            author=self.user,
        )
        self.post.tags.add(self.tag)

    def test_upvote_creation(self):
        """Test that upvoting creates a vote."""
        self.client.login(username="other", password="password123")
        response = self.client.post(reverse("posting:upvote", args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Vote.objects.filter(
                post=self.post, voter=self.other_user, vote_type=Vote.UPVOTE
            ).exists()
        )
        self.assertEqual(self.post.get_net_votes(), 1)

    def test_downvote_creation(self):
        """Test that downvoting creates a vote."""
        self.client.login(username="other", password="password123")
        response = self.client.post(reverse("posting:downvote", args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Vote.objects.filter(
                post=self.post, voter=self.other_user, vote_type=Vote.DOWNVOTE
            ).exists()
        )
        self.assertEqual(self.post.get_net_votes(), -1)

    def test_upvote_toggle_off(self):
        """Test that clicking upvote again removes it."""
        Vote.objects.create(
            post=self.post, voter=self.other_user, vote_type=Vote.UPVOTE
        )
        self.client.login(username="other", password="password123")
        response = self.client.post(reverse("posting:upvote", args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Vote.objects.filter(post=self.post, voter=self.other_user).exists()
        )
        self.assertEqual(self.post.get_net_votes(), 0)

    def test_downvote_toggle_off(self):
        """Test that clicking downvote again removes it."""
        Vote.objects.create(
            post=self.post, voter=self.other_user, vote_type=Vote.DOWNVOTE
        )
        self.client.login(username="other", password="password123")
        response = self.client.post(reverse("posting:downvote", args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Vote.objects.filter(post=self.post, voter=self.other_user).exists()
        )
        self.assertEqual(self.post.get_net_votes(), 0)

    def test_switch_downvote_to_upvote(self):
        """Test switching from downvote to upvote."""
        Vote.objects.create(
            post=self.post, voter=self.other_user, vote_type=Vote.DOWNVOTE
        )
        self.client.login(username="other", password="password123")
        response = self.client.post(reverse("posting:upvote", args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)
        vote = Vote.objects.get(post=self.post, voter=self.other_user)
        self.assertEqual(vote.vote_type, Vote.UPVOTE)
        self.assertEqual(self.post.get_net_votes(), 1)

    def test_switch_upvote_to_downvote(self):
        """Test switching from upvote to downvote."""
        Vote.objects.create(
            post=self.post, voter=self.other_user, vote_type=Vote.UPVOTE
        )
        self.client.login(username="other", password="password123")
        response = self.client.post(reverse("posting:downvote", args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)
        vote = Vote.objects.get(post=self.post, voter=self.other_user)
        self.assertEqual(vote.vote_type, Vote.DOWNVOTE)
        self.assertEqual(self.post.get_net_votes(), -1)

    def test_net_votes_calculation(self):
        """Test net votes calculation with multiple votes."""
        # Add upvotes
        Vote.objects.create(
            post=self.post, voter=self.user, vote_type=Vote.UPVOTE
        )
        Vote.objects.create(
            post=self.post, voter=self.other_user, vote_type=Vote.UPVOTE
        )
        # Add downvote
        third_user = User.objects.create_user(
            username="third", email="third@yale.edu", password="password123"
        )
        Vote.objects.create(
            post=self.post, voter=third_user, vote_type=Vote.DOWNVOTE
        )
        self.assertEqual(self.post.get_upvotes_count(), 2)
        self.assertEqual(self.post.get_downvotes_count(), 1)
        self.assertEqual(self.post.get_net_votes(), 1)

    def test_one_vote_per_user_per_post(self):
        """Test that a user can only have one vote per post."""
        Vote.objects.create(
            post=self.post, voter=self.other_user, vote_type=Vote.UPVOTE
        )
        # Try to create another vote - should update existing
        self.client.login(username="other", password="password123")
        response = self.client.post(reverse("posting:downvote", args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)
        # Should only have one vote, but type changed
        self.assertEqual(
            Vote.objects.filter(post=self.post, voter=self.other_user).count(), 1
        )
        vote = Vote.objects.get(post=self.post, voter=self.other_user)
        self.assertEqual(vote.vote_type, Vote.DOWNVOTE)

    def test_vote_requires_authentication(self):
        """Test that voting requires authentication."""
        response = self.client.post(reverse("posting:upvote", args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)  # Redirects to login
        response = self.client.post(reverse("posting:downvote", args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)  # Redirects to login
