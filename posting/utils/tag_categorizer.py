"""
AI-powered tag categorization using OpenAI.

Groups tags into logical categories dynamically as the tag set grows.
Results are cached to minimize API calls.
"""

import json
import logging
from typing import Optional

from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

# Cache key for tag categories
TAG_CATEGORIES_CACHE_KEY = "ai_tag_categories"
TAG_CATEGORIES_CACHE_TIMEOUT = 60 * 60  # 1 hour


class AITagCategorizer:
    """
    Uses OpenAI to intelligently group tags into categories.

    The AI analyzes tag names and groups them into logical categories
    like "Courses", "Sentiments", "Topics", etc.
    """

    def __init__(self):
        self._client = None

    @property
    def client(self):
        """Lazy initialization of OpenAI client."""
        if self._client is None:
            api_key = getattr(settings, "OPENAI_API_KEY", None)
            if not api_key:
                return None
            try:
                from openai import OpenAI
                self._client = OpenAI(api_key=api_key)
            except ImportError:
                logger.warning("openai package not installed. AI categorization disabled.")
                return None
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {e}")
                return None
        return self._client

    def categorize_tags(self, tag_names: list[str], force_refresh: bool = False) -> dict[str, list[str]]:
        """
        Group tags into AI-suggested categories.

        Args:
            tag_names: List of tag names to categorize
            force_refresh: If True, bypass cache and call API

        Returns:
            Dict mapping category names to lists of tag names
            Example: {"Courses": ["MGT 541", "ECON 101"], "Topics": ["campus-life", "events"]}
        """
        if not tag_names:
            return {}

        # Create a cache key based on sorted tag names (case-insensitive)
        sorted_tags = sorted([t.lower() for t in tag_names])
        cache_key = f"{TAG_CATEGORIES_CACHE_KEY}:{hash(tuple(sorted_tags))}"

        # Check cache first
        if not force_refresh:
            cached = cache.get(cache_key)
            if cached:
                logger.debug("Using cached tag categories")
                return cached

        # Try AI categorization
        if self.client:
            try:
                categories = self._call_ai(tag_names)
                if categories:
                    # Normalize: ensure returned tags match original casing
                    categories = self._normalize_tag_casing(categories, tag_names)
                    cache.set(cache_key, categories, TAG_CATEGORIES_CACHE_TIMEOUT)
                    return categories
            except Exception as e:
                logger.error(f"AI tag categorization failed: {e}")

        # Fallback to simple keyword matching (also cache this)
        fallback = self._fallback_categorize(tag_names)
        cache.set(cache_key, fallback, TAG_CATEGORIES_CACHE_TIMEOUT)
        return fallback

    def _normalize_tag_casing(self, categories: dict[str, list[str]], original_tags: list[str]) -> dict[str, list[str]]:
        """Ensure AI-returned tags match original casing."""
        # Build case-insensitive lookup
        tag_lookup = {t.lower(): t for t in original_tags}

        normalized = {}
        for cat_name, tags in categories.items():
            normalized_tags = []
            for tag in tags:
                # Find original casing
                original = tag_lookup.get(tag.lower())
                if original:
                    normalized_tags.append(original)
            if normalized_tags:
                normalized[cat_name] = normalized_tags

        return normalized

    def _call_ai(self, tag_names: list[str]) -> dict[str, list[str]]:
        """Call OpenAI to categorize tags with timeout."""
        prompt = f"""You are helping organize tags for a university campus forum.
Given these tags, group them into 3-6 logical categories.

Tags: {', '.join(tag_names)}

Rules:
- Create clear, descriptive category names (e.g., "Course Reviews", "Campus Life", "Sentiments")
- Each tag must appear in exactly one category
- Keep categories balanced (avoid having one huge category and many tiny ones)
- Course codes (like "MGT 541", "ECON 101") should be in a "Courses" category
- Sentiment tags (like "Recommended", "Not Recommended", "Mixed") should be in "Sentiments"

Respond with ONLY valid JSON in this exact format:
{{"Category Name": ["tag1", "tag2"], "Another Category": ["tag3", "tag4"]}}"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",  # Fast and cheap
            messages=[
                {"role": "system", "content": "You are a helpful assistant that categorizes tags. Always respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,  # Low temperature for consistent categorization
            max_tokens=1000,  # Enough for ~100 tags
            timeout=10.0  # 10 second timeout
        )

        content = response.choices[0].message.content.strip()

        # Parse JSON response
        # Handle potential markdown code blocks
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
            content = content.strip()

        categories = json.loads(content)

        # Validate structure
        if not isinstance(categories, dict):
            raise ValueError("Response is not a dictionary")

        for cat_name, tags in categories.items():
            if not isinstance(tags, list):
                raise ValueError(f"Category {cat_name} does not contain a list")

        logger.info(f"AI categorized {len(tag_names)} tags into {len(categories)} categories")
        return categories

    def _fallback_categorize(self, tag_names: list[str]) -> dict[str, list[str]]:
        """Fallback keyword-based categorization when AI is unavailable."""
        categories = {
            "Courses": [],
            "Sentiments": [],
            "Reviews": [],
            "Topics": []
        }

        for tag in tag_names:
            name_lower = tag.lower()

            # Check for course-related tags
            if 'mgt' in name_lower or any(char.isdigit() for char in tag):
                categories["Courses"].append(tag)
            # Check for sentiment tags
            elif any(term in name_lower for term in ['recommended', 'not recommended', 'mixed']):
                categories["Sentiments"].append(tag)
            # Check for review tags
            elif 'review' in name_lower or 'class' in name_lower:
                categories["Reviews"].append(tag)
            # Default to Topics
            else:
                categories["Topics"].append(tag)

        # Remove empty categories
        return {k: v for k, v in categories.items() if v}

    def invalidate_cache(self):
        """Clear cached categories (call when tags are added/removed)."""
        # We use a hash-based key, so we can't easily clear all
        # But new tag sets will get new cache keys anyway
        logger.info("Tag category cache will refresh on next request with different tags")


# Singleton instance
_categorizer_instance: Optional[AITagCategorizer] = None


def get_categorizer() -> AITagCategorizer:
    """Get or create singleton categorizer instance."""
    global _categorizer_instance
    if _categorizer_instance is None:
        _categorizer_instance = AITagCategorizer()
    return _categorizer_instance
