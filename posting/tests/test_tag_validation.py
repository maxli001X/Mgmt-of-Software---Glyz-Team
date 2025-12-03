from django.test import TestCase
from posting.forms.post_form import PostForm

class TagValidationTests(TestCase):
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
