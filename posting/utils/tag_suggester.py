"""
Tag Suggestion using TF-IDF.

100% local processing - no external API calls.
Suggests tags based on content similarity to existing posts with those tags.

Usage:
    suggester = get_suggester()
    tags = suggester.suggest("My title", "My post body", top_k=4)
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


class TagSuggester:
    """
    TF-IDF based tag suggestion system.

    Learns from existing posts and their tags to suggest relevant tags
    for new content. Uses scikit-learn's TfidfVectorizer.
    """

    _instance: Optional["TagSuggester"] = None

    def __new__(cls):
        """Singleton pattern - only one instance needed."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.vectorizer = None
        self.tag_vectors = None
        self.tags = []
        self._initialized = True

    def _ensure_vectorizer(self):
        """Lazy initialization of TfidfVectorizer."""
        if self.vectorizer is None:
            try:
                from sklearn.feature_extraction.text import TfidfVectorizer
                self.vectorizer = TfidfVectorizer(
                    max_features=1000,
                    stop_words="english",
                    ngram_range=(1, 2),  # Include bigrams for better matching
                    min_df=1,
                    max_df=0.95,
                )
            except ImportError:
                logger.warning("scikit-learn not installed. Tag suggestions disabled.")
                return False
        return True

    def train(self):
        """
        Build TF-IDF model from existing posts.

        Should be called on app startup and periodically to update.
        """
        if not self._ensure_vectorizer():
            return

        try:
            # Import here to avoid circular imports
            from posting.models import Tag

            tags = list(Tag.objects.prefetch_related("posts").all())
            if not tags:
                logger.info("No tags found for training tag suggester.")
                return

            self.tags = tags
            tag_texts = []

            for tag in tags:
                # Get sample of posts for this tag
                posts = tag.posts.all()[:50]
                if posts:
                    text = " ".join([f"{p.title} {p.body}" for p in posts])
                else:
                    # Fallback to tag name if no posts
                    text = tag.name
                tag_texts.append(text)

            if tag_texts:
                self.tag_vectors = self.vectorizer.fit_transform(tag_texts)
                logger.info(f"Tag suggester trained on {len(tags)} tags.")

        except Exception as e:
            logger.error(f"Failed to train tag suggester: {e}")

    def suggest(self, title: str, body: str, top_k: int = 4) -> list[str]:
        """
        Suggest tags for new post content.

        Args:
            title: Post title
            body: Post body
            top_k: Maximum number of suggestions to return

        Returns:
            List of tag names (strings), ordered by relevance
        """
        if not self._ensure_vectorizer():
            return []

        # Train if not already trained
        if self.tag_vectors is None or len(self.tags) == 0:
            self.train()

        if self.tag_vectors is None or len(self.tags) == 0:
            return []

        try:
            from sklearn.metrics.pairwise import cosine_similarity

            text = f"{title} {body}"
            text_vector = self.vectorizer.transform([text])
            similarities = cosine_similarity(text_vector, self.tag_vectors)[0]

            # Get indices of top K matches
            top_indices = similarities.argsort()[-top_k:][::-1]

            # Filter by minimum similarity threshold
            suggestions = [
                self.tags[i].name
                for i in top_indices
                if similarities[i] > 0.05
            ]

            return suggestions

        except Exception as e:
            logger.error(f"Failed to suggest tags: {e}")
            return []

    def refresh(self):
        """
        Force refresh of the model.

        Call this when new tags are created or significant content changes.
        """
        self.tag_vectors = None
        self.tags = []
        self.train()


# Singleton accessor
_suggester_instance: Optional[TagSuggester] = None


def get_suggester() -> TagSuggester:
    """Get or create singleton tag suggester instance."""
    global _suggester_instance
    if _suggester_instance is None:
        _suggester_instance = TagSuggester()
    return _suggester_instance
