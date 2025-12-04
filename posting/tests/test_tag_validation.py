from django.core.exceptions import ValidationError
from django.test import TestCase

from posting.forms.post_form import PostForm
from posting.models import Tag


class TagValidationTests(TestCase):
    """Tests for tag input and hashtag validation."""

    def test_valid_tags(self):
        """Test that valid tags are accepted."""
        form_data = {
            'title': 'Test Post',
            'body': 'This is a test post.',
            'tags_input': 'valid, tags, are, good',
            'is_anonymous': False
        }
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_short_tag(self):
        """Test that tags shorter than 2 chars are rejected."""
        form_data = {
            'title': 'Test Post',
            'body': 'This is a test post.',
            'tags_input': 'a, valid',
            'is_anonymous': False
        }
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("too short", str(form.errors['tags_input']))

    def test_long_tag(self):
        """Test that tags longer than 50 chars are rejected."""
        long_tag = 'a' * 51
        form_data = {
            'title': 'Test Post',
            'body': 'This is a test post.',
            'tags_input': f'{long_tag}, valid',
            'is_anonymous': False
        }
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("too long", str(form.errors['tags_input']))

    def test_hashtag_extraction_length(self):
        """Test that extracted hashtags respect length limits."""
        form = PostForm()

        # Should extract 'valid' but ignore 'a' and long tag
        long_tag = 'b' * 51
        text = f"This has #valid and #a and #{long_tag} hashtags."

        hashtags = form.extract_hashtags(text)
        self.assertIn('valid', hashtags)
        self.assertNotIn('a', hashtags)
        self.assertNotIn(long_tag, hashtags)


class HashtagExtractionTests(TestCase):
    """Tests for hashtag extraction from post body."""

    def test_hashtag_with_embedded_hash_extracts_first_part(self):
        """Test that #pick#k extracts only 'pick', not 'k'."""
        form = PostForm()
        hashtags = form.extract_hashtags("Testing #pick#k here")
        self.assertIn('pick', hashtags)
        # 'k' alone is too short (< 2 chars) so won't be included anyway
        self.assertNotIn('pick#k', hashtags)

    def test_space_after_hash_not_recognized(self):
        """Test that '# class' is NOT recognized as a hashtag."""
        form = PostForm()
        hashtags = form.extract_hashtags("Testing # class here")
        self.assertNotIn('class', hashtags)
        self.assertEqual(len(hashtags), 0)

    def test_multiple_hashtags_parsed_correctly(self):
        """Test #class #classes extracts both tags."""
        form = PostForm()
        hashtags = form.extract_hashtags("Taking #class and #classes today")
        self.assertIn('class', hashtags)
        self.assertIn('classes', hashtags)
        self.assertEqual(len(hashtags), 2)

    def test_hashtag_with_hyphen(self):
        """Test that #campus-life is valid."""
        form = PostForm()
        hashtags = form.extract_hashtags("Love #campus-life at Yale")
        self.assertIn('campus-life', hashtags)

    def test_hashtag_with_underscore(self):
        """Test that #campus_life is valid."""
        form = PostForm()
        hashtags = form.extract_hashtags("Love #campus_life at Yale")
        self.assertIn('campus_life', hashtags)

    def test_hashtag_stops_at_special_chars(self):
        """Test that hashtags stop at punctuation."""
        form = PostForm()
        hashtags = form.extract_hashtags("Check #academics! Great stuff.")
        self.assertIn('academics', hashtags)
        self.assertNotIn('academics!', hashtags)


class TagInputValidationTests(TestCase):
    """Tests for manual tag input field validation."""

    def test_tag_input_with_embedded_hash_rejected(self):
        """Test that tags with # in manual input are rejected."""
        form_data = {
            'title': 'Test Post',
            'body': 'Test body content here.',
            'tags_input': 'pick#k, valid',
            'is_anonymous': False
        }
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())
        # Check the actual error message (HTML entities may be escaped)
        error_str = str(form.errors['tags_input'])
        self.assertTrue(
            "cannot contain" in error_str and "symbol" in error_str,
            f"Expected hash error message, got: {error_str}"
        )

    def test_tag_input_with_space_rejected(self):
        """Test that tags with spaces are rejected."""
        form_data = {
            'title': 'Test Post',
            'body': 'Test body content here.',
            'tags_input': 'campus life, valid',
            'is_anonymous': False
        }
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("cannot contain spaces", str(form.errors['tags_input']))

    def test_tag_input_strips_leading_hash(self):
        """Test that leading # is stripped from manual input."""
        form_data = {
            'title': 'Test Post',
            'body': 'Test body content here.',
            'tags_input': '#academics, #sports',
            'is_anonymous': False
        }
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())


class TagModelValidationTests(TestCase):
    """Tests for Tag model validation."""

    def test_tag_model_rejects_hash_in_name(self):
        """Test that Tag model rejects names with #."""
        tag = Tag(name="pick#k", slug="pickk")
        with self.assertRaises(ValidationError):
            tag.full_clean()

    def test_tag_model_rejects_space_in_name(self):
        """Test that Tag model rejects names with spaces."""
        tag = Tag(name="campus life", slug="campus-life")
        with self.assertRaises(ValidationError):
            tag.full_clean()

    def test_tag_model_rejects_short_name(self):
        """Test that Tag model rejects names < 2 chars."""
        tag = Tag(name="a", slug="a")
        with self.assertRaises(ValidationError):
            tag.full_clean()

    def test_tag_model_accepts_valid_name(self):
        """Test that Tag model accepts valid names."""
        tag = Tag(name="Academics", slug="academics")
        tag.full_clean()  # Should not raise
        tag.save()
        self.assertEqual(Tag.objects.count(), 1)


class GetOrCreateTagTests(TestCase):
    """Tests for the get_or_create_tag method."""

    def test_get_or_create_strips_hash(self):
        """Test that # symbols are stripped from tag names."""
        form = PostForm()
        tag = form.get_or_create_tag("#academics")
        self.assertIsNotNone(tag)
        self.assertEqual(tag.name, "Academics")
        self.assertNotIn('#', tag.name)

    def test_get_or_create_returns_none_for_spaces(self):
        """Test that tags with spaces return None."""
        form = PostForm()
        tag = form.get_or_create_tag("campus life")
        self.assertIsNone(tag)

    def test_get_or_create_returns_none_for_short(self):
        """Test that tags < 2 chars return None."""
        form = PostForm()
        tag = form.get_or_create_tag("a")
        self.assertIsNone(tag)

    def test_get_or_create_handles_multiple_hashes(self):
        """Test that multiple # symbols are all removed."""
        form = PostForm()
        tag = form.get_or_create_tag("##pick##k")
        self.assertIsNotNone(tag)
        self.assertEqual(tag.name, "Pickk")
        self.assertNotIn('#', tag.name)
