"""
AI Content Moderation using OpenAI Moderation API.

The Moderation API is FREE and unlimited. It checks content for:
- Hate speech
- Harassment
- Self-harm
- Sexual content
- Violence
- And more categories

Usage:
    moderator = AIContentModerator()
    result = moderator.check_content("Some text to check")
    if result['flagged']:
        # Handle flagged content
"""

import logging
import re
import threading
from typing import Optional

from django.conf import settings

logger = logging.getLogger(__name__)

# Crisis keywords for instant detection (no API call needed)
CRISIS_KEYWORDS = [
    r'\b(suicid|kill\s*(my)?self|end\s*(my)?\s*life|want\s*to\s*die)\b',
    r'\b(self[- ]?harm|cutting\s*myself|hurt\s*myself)\b',
    r'\b(don\'?t\s*want\s*to\s*live|no\s*reason\s*to\s*live)\b',
    r'\b(overdose|take\s*pills|slit\s*wrist)\b',
]
CRISIS_PATTERN = re.compile('|'.join(CRISIS_KEYWORDS), re.IGNORECASE)


def quick_crisis_check(text: str) -> bool:
    """
    Fast keyword-based crisis detection (no API call).

    Returns True if text contains obvious crisis/self-harm indicators.
    This runs synchronously for immediate crisis resource display.
    """
    if not text:
        return False
    return bool(CRISIS_PATTERN.search(text))


class AIContentModerator:
    """
    Wrapper for OpenAI Moderation API.

    Handles content screening for posts and comments.
    Returns flagging decisions, severity scores, and crisis detection.
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
                logger.warning("openai package not installed. AI moderation disabled.")
                return None
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {e}")
                return None
        return self._client

    def check_content(self, text: str) -> dict:
        """
        Check content using OpenAI Moderation API.

        Args:
            text: The content to moderate (post title + body, or comment body)

        Returns:
            dict with keys:
                - flagged: bool - Whether content was flagged
                - categories: dict - Category flags (hate, violence, etc.)
                - category_scores: dict - Confidence scores per category (0-1)
                - severity_score: float - Max score across all categories (0-1)
                - is_crisis: bool - Whether self-harm content was detected
                - error: str (optional) - Error message if API call failed
        """
        # Return safe defaults if no API key or client
        if not self.client:
            return {
                "flagged": False,
                "categories": {},
                "category_scores": {},
                "severity_score": 0.0,
                "is_crisis": False,
                "error": "OpenAI API not configured",
            }

        # Skip very short content
        if not text or len(text.strip()) < 3:
            return {
                "flagged": False,
                "categories": {},
                "category_scores": {},
                "severity_score": 0.0,
                "is_crisis": False,
            }

        try:
            response = self.client.moderations.create(input=text)
            result = response.results[0]

            categories = result.categories.model_dump()
            scores = result.category_scores.model_dump()

            # Calculate severity score (max across all categories)
            severity_score = max(scores.values()) if scores else 0.0

            # Check for crisis content (self-harm or violence indicators)
            is_crisis = (
                # Self-harm indicators
                scores.get("self-harm", 0) > 0.5
                or scores.get("self-harm/intent", 0) > 0.3
                or scores.get("self-harm/instructions", 0) > 0.3
                # Violence indicators
                or scores.get("violence", 0) > 0.5
                or scores.get("violence/graphic", 0) > 0.3
            )

            return {
                "flagged": result.flagged,
                "categories": categories,
                "category_scores": scores,
                "severity_score": severity_score,
                "is_crisis": is_crisis,
            }

        except Exception as e:
            logger.error(f"OpenAI Moderation API error: {e}")
            return {
                "flagged": False,
                "categories": {},
                "category_scores": {},
                "severity_score": 0.0,
                "is_crisis": False,
                "error": str(e),
            }

    def get_top_categories(self, category_scores: dict, threshold: float = 0.3) -> list[str]:
        """
        Get list of categories that exceed the threshold.

        Useful for displaying why content was flagged.
        """
        return [
            category.replace("/", " - ").replace("_", " ").title()
            for category, score in category_scores.items()
            if score >= threshold
        ]


# Singleton instance for reuse
_moderator_instance: Optional[AIContentModerator] = None


def get_moderator() -> AIContentModerator:
    """Get or create singleton moderator instance."""
    global _moderator_instance
    if _moderator_instance is None:
        _moderator_instance = AIContentModerator()
    return _moderator_instance


def run_moderation_async(post_id: int, text: str):
    """
    Run AI moderation in background thread.

    Updates the post's ai_flagged, ai_severity_score, ai_categories,
    and show_crisis_resources fields after moderation completes.
    """
    def _moderate():
        try:
            # Import here to avoid circular imports
            from posting.models import Post

            moderator = get_moderator()
            result = moderator.check_content(text)

            logger.info(f"Async moderation for post {post_id}: flagged={result.get('flagged')}, is_crisis={result.get('is_crisis')}")

            # Update post with moderation results
            Post.objects.filter(pk=post_id).update(
                ai_flagged=result.get("flagged", False),
                ai_severity_score=result.get("severity_score"),
                ai_categories=result.get("category_scores"),
                show_crisis_resources=result.get("is_crisis", False),
                is_flagged=result.get("flagged", False),  # Auto-flag for human review
            )

        except Exception as e:
            logger.error(f"Async moderation failed for post {post_id}: {e}")

    # Run in background thread
    thread = threading.Thread(target=_moderate, daemon=True)
    thread.start()
