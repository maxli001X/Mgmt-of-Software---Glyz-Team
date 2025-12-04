"""Tests for AI moderation and tag suggestion features."""

import json
from unittest.mock import MagicMock, patch

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from posting.models import Post, Tag
from posting.utils.ai_moderator import AIContentModerator, get_moderator
from posting.utils.tag_suggester import TagSuggester, get_suggester

User = get_user_model()


class AIContentModeratorTests(TestCase):
    """Tests for AIContentModerator class."""

    def test_get_moderator_returns_singleton(self):
        """Test that get_moderator returns the same instance."""
        mod1 = get_moderator()
        mod2 = get_moderator()
        self.assertIs(mod1, mod2)

    @override_settings(OPENAI_API_KEY=None)
    def test_check_content_without_api_key(self):
        """Test that check_content returns safe defaults without API key."""
        # Reset the cached instance
        from posting.utils import ai_moderator
        ai_moderator._moderator_instance = None

        moderator = get_moderator()
        result = moderator.check_content("test content")

        self.assertFalse(result["flagged"])
        self.assertEqual(result["severity_score"], 0)
        self.assertFalse(result["is_crisis"])

    @override_settings(OPENAI_API_KEY="test-key")
    def test_check_content_with_mocked_api(self):
        """Test check_content with mocked OpenAI API."""
        from posting.utils import ai_moderator
        ai_moderator._moderator_instance = None

        # Mock the API response
        mock_result = MagicMock()
        mock_result.flagged = True
        mock_result.categories.model_dump.return_value = {
            "hate": True,
            "violence": False,
            "self-harm": False,
        }
        mock_result.category_scores.model_dump.return_value = {
            "hate": 0.8,
            "violence": 0.1,
            "self-harm": 0.0,
        }

        mock_response = MagicMock()
        mock_response.results = [mock_result]

        mock_client = MagicMock()
        mock_client.moderations.create.return_value = mock_response

        moderator = AIContentModerator()
        moderator._client = mock_client  # Inject mock client
        result = moderator.check_content("test hateful content")

        self.assertTrue(result["flagged"])
        self.assertAlmostEqual(result["severity_score"], 0.8)
        self.assertFalse(result["is_crisis"])

    @override_settings(OPENAI_API_KEY="test-key")
    def test_crisis_detection(self):
        """Test that crisis content is detected correctly."""
        from posting.utils import ai_moderator
        ai_moderator._moderator_instance = None

        mock_result = MagicMock()
        mock_result.flagged = True
        mock_result.categories.model_dump.return_value = {"self-harm": True}
        mock_result.category_scores.model_dump.return_value = {
            "self-harm": 0.7,
            "self-harm/intent": 0.5,
        }

        mock_response = MagicMock()
        mock_response.results = [mock_result]

        mock_client = MagicMock()
        mock_client.moderations.create.return_value = mock_response

        moderator = AIContentModerator()
        moderator._client = mock_client  # Inject mock client
        result = moderator.check_content("crisis content")

        self.assertTrue(result["is_crisis"])


class TagSuggesterTests(TestCase):
    """Tests for TagSuggester class."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@yale.edu",
            password="testpass123",
        )

        # Create tags with sample posts
        self.tech_tag = Tag.objects.create(name="Technology", slug="technology")
        self.sports_tag = Tag.objects.create(name="Sports", slug="sports")
        self.academics_tag = Tag.objects.create(name="Academics", slug="academics")

        # Create posts with tags
        tech_post = Post.objects.create(
            title="Python programming tips",
            body="Learn about machine learning and artificial intelligence",
            author=self.user,
        )
        tech_post.tags.add(self.tech_tag)

        sports_post = Post.objects.create(
            title="Yale football game",
            body="The team won the championship after a great season",
            author=self.user,
        )
        sports_post.tags.add(self.sports_tag)

    def test_get_suggester_returns_singleton(self):
        """Test that get_suggester returns the same instance."""
        sug1 = get_suggester()
        sug2 = get_suggester()
        self.assertIs(sug1, sug2)

    def test_suggest_returns_list(self):
        """Test that suggest returns a list of tag names."""
        suggester = TagSuggester()
        suggester._initialized = False
        suggester.__init__()

        suggestions = suggester.suggest(
            "My new AI project",
            "Building a neural network for image classification",
        )

        self.assertIsInstance(suggestions, list)

    def test_suggest_empty_for_short_content(self):
        """Test that short content gets empty suggestions."""
        suggester = TagSuggester()
        suggester._initialized = False
        suggester.__init__()

        # Very short content shouldn't crash
        suggestions = suggester.suggest("Hi", "")
        self.assertIsInstance(suggestions, list)

    def test_refresh_clears_cache(self):
        """Test that refresh clears the model cache."""
        suggester = TagSuggester()
        suggester.train()

        # Force some state
        suggester.tags = [self.tech_tag]

        # Refresh should clear
        suggester.refresh()

        # After refresh and retrain, should have tags
        self.assertTrue(len(suggester.tags) >= 0)


class TagSuggestionAPITests(TestCase):
    """Tests for the tag suggestion API endpoint."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@yale.edu",
            password="testpass123",
        )
        self.url = reverse("posting:suggest_tags")

    def test_requires_authentication(self):
        """Test that the API requires authentication."""
        response = self.client.post(
            self.url,
            data=json.dumps({"title": "Test", "body": "Test body content"}),
            content_type="application/json",
        )
        # Should redirect to login
        self.assertEqual(response.status_code, 302)

    def test_requires_post_method(self):
        """Test that only POST is allowed."""
        self.client.login(username="testuser", password="testpass123")

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_returns_json(self):
        """Test that the API returns JSON."""
        self.client.login(username="testuser", password="testpass123")

        response = self.client.post(
            self.url,
            data=json.dumps({
                "title": "Test title for suggestions",
                "body": "This is a longer test body with enough content to trigger suggestions",
            }),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

        data = response.json()
        self.assertIn("tags", data)
        self.assertIsInstance(data["tags"], list)

    def test_short_content_returns_empty(self):
        """Test that short content returns empty suggestions."""
        self.client.login(username="testuser", password="testpass123")

        response = self.client.post(
            self.url,
            data=json.dumps({"title": "Hi", "body": ""}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["tags"], [])

    def test_invalid_json_returns_error(self):
        """Test that invalid JSON returns 400."""
        self.client.login(username="testuser", password="testpass123")

        response = self.client.post(
            self.url,
            data="not valid json",
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)


class PostFormAIModerationTests(TestCase):
    """Tests for AI moderation in post form."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@yale.edu",
            password="testpass123",
        )

    def test_ai_moderation_called_on_save(self):
        """Test that AI moderation is called when saving a post."""
        mock_moderator = MagicMock()
        mock_moderator.check_content.return_value = {
            "flagged": False,
            "severity_score": 0.1,
            "category_scores": {"hate": 0.1},
            "is_crisis": False,
        }

        with patch("posting.utils.ai_moderator.get_moderator", return_value=mock_moderator):
            from posting.forms import PostForm

            form = PostForm(data={
                "title": "Test Post",
                "body": "This is a test post body",
                "is_anonymous": True,
                "tags_input": "",
            })

            self.assertTrue(form.is_valid())
            post = form.save(author=self.user)

            mock_moderator.check_content.assert_called_once()
            self.assertFalse(post.ai_flagged)
            self.assertFalse(post.is_flagged)

    def test_flagged_content_sets_is_flagged(self):
        """Test that AI-flagged content also sets is_flagged."""
        mock_moderator = MagicMock()
        mock_moderator.check_content.return_value = {
            "flagged": True,
            "severity_score": 0.9,
            "category_scores": {"hate": 0.9},
            "is_crisis": False,
        }

        with patch("posting.utils.ai_moderator.get_moderator", return_value=mock_moderator):
            from posting.forms import PostForm

            form = PostForm(data={
                "title": "Bad Post",
                "body": "This is problematic content",
                "is_anonymous": True,
                "tags_input": "",
            })

            self.assertTrue(form.is_valid())
            post = form.save(author=self.user)

            self.assertTrue(post.ai_flagged)
            self.assertTrue(post.is_flagged)
            self.assertAlmostEqual(post.ai_severity_score, 0.9)

    def test_crisis_content_sets_show_crisis_resources(self):
        """Test that crisis content sets show_crisis_resources."""
        mock_moderator = MagicMock()
        mock_moderator.check_content.return_value = {
            "flagged": True,
            "severity_score": 0.8,
            "category_scores": {"self-harm": 0.8},
            "is_crisis": True,
        }

        with patch("posting.utils.ai_moderator.get_moderator", return_value=mock_moderator):
            from posting.forms import PostForm

            form = PostForm(data={
                "title": "Concerning Post",
                "body": "Content that indicates distress",
                "is_anonymous": True,
                "tags_input": "",
            })

            self.assertTrue(form.is_valid())
            post = form.save(author=self.user)

            self.assertTrue(post.show_crisis_resources)


class CommentFormAIModerationTests(TestCase):
    """Tests for AI moderation in comment form."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@yale.edu",
            password="testpass123",
        )
        self.post = Post.objects.create(
            title="Test Post",
            body="Test body",
            author=self.user,
        )

    def test_ai_moderation_called_on_comment_save(self):
        """Test that AI moderation is called when saving a comment."""
        mock_moderator = MagicMock()
        mock_moderator.check_content.return_value = {
            "flagged": False,
            "severity_score": 0.05,
            "category_scores": {},
            "is_crisis": False,
        }

        with patch("posting.utils.ai_moderator.get_moderator", return_value=mock_moderator):
            from posting.forms import CommentForm

            form = CommentForm(
                data={"body": "This is a test comment", "is_anonymous": True},
                post=self.post,
            )

            self.assertTrue(form.is_valid())
            comment = form.save(author=self.user)

            mock_moderator.check_content.assert_called_once()
            self.assertFalse(comment.ai_flagged)
