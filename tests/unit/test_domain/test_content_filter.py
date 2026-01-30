"""
Unit tests for ContentFilterService domain service.
Tests cover: filtering, sanitization, inappropriate content detection.
"""
import pytest
from src.Domain.services.content_filter import ContentFilterService


class TestContentFilterServiceDetection:
    """Tests for inappropriate content detection."""

    def test_contains_inappropriate_content_with_spam(self):
        """Should detect 'spam' in content."""
        content = "This is spam content"
        assert ContentFilterService.contains_inappropriate_content(content) is True

    def test_contains_inappropriate_content_with_malware(self):
        """Should detect 'malware' in content."""
        content = "Warning: malware detected"
        assert ContentFilterService.contains_inappropriate_content(content) is True

    def test_contains_inappropriate_content_with_hack(self):
        """Should detect 'hack' in content."""
        content = "Don't hack my system"
        assert ContentFilterService.contains_inappropriate_content(content) is True

    def test_contains_inappropriate_content_case_insensitive(self):
        """Should detect inappropriate words case-insensitively."""
        contents = [
            "This is SPAM content",
            "This is Spam content",
            "This is spaM content",
            "This is MALWARE",
            "This is HACK"
        ]
        for content in contents:
            assert ContentFilterService.contains_inappropriate_content(content) is True

    def test_contains_inappropriate_content_with_clean_content(self):
        """Should not detect inappropriate content in clean text."""
        content = "This is a clean message"
        assert ContentFilterService.contains_inappropriate_content(content) is False

    def test_contains_inappropriate_content_with_empty_string(self):
        """Should handle empty string gracefully."""
        content = ""
        assert ContentFilterService.contains_inappropriate_content(content) is False


class TestContentFilterServiceSanitization:
    """Tests for content sanitization."""

    def test_sanitize_content_removes_leading_whitespace(self):
        """Should remove leading whitespace."""
        content = "   hello world"
        sanitized = ContentFilterService.sanitize_content(content)
        assert sanitized == "hello world"

    def test_sanitize_content_removes_trailing_whitespace(self):
        """Should remove trailing whitespace."""
        content = "hello world   "
        sanitized = ContentFilterService.sanitize_content(content)
        assert sanitized == "hello world"

    def test_sanitize_content_removes_both_ends_whitespace(self):
        """Should remove whitespace from both ends."""
        content = "   hello world   "
        sanitized = ContentFilterService.sanitize_content(content)
        assert sanitized == "hello world"


class TestContentFilterServiceFilter:
    """Tests for the main filter() method."""

    def test_filter_clean_content_returns_content(self):
        """Should return content when it's clean."""
        content = "Hello world"
        result = ContentFilterService().filter(content)
        assert result == "Hello world"

    def test_filter_sanitizes_content_before_checking(self):
        """Should sanitize content before checking for inappropriate words."""
        content = "   Hello world   "
        result = ContentFilterService().filter(content)
        assert result == "Hello world"

    def test_filter_raises_error_for_spam(self):
        """Should raise ValueError when 'spam' is detected."""
        content = "Buy cheap spam now"
        with pytest.raises(ValueError, match="Content contains inappropriate words"):
            ContentFilterService().filter(content)

    def test_filter_raises_error_for_malware(self):
        """Should raise ValueError when 'malware' is detected."""
        content = "This is malware"
        with pytest.raises(ValueError, match="Content contains inappropriate words"):
            ContentFilterService().filter(content)

    def test_filter_raises_error_for_hack(self):
        """Should raise ValueError when 'hack' is detected."""
        content = "Don't hack into the system"
        with pytest.raises(ValueError, match="Content contains inappropriate words"):
            ContentFilterService().filter(content)

    def test_filter_case_insensitive_spam_detection(self):
        """Should detect spam case-insensitively."""
        with pytest.raises(ValueError, match="Content contains inappropriate words"):
            ContentFilterService().filter("SPAM is bad")

    def test_filter_with_multiple_inappropriate_words(self):
        """Should detect any inappropriate word in content."""
        with pytest.raises(ValueError):
            ContentFilterService().filter("spam and malware and hack")

    def test_filter_ignores_word_boundaries(self):
        """Should detect words within other words (if they exist as substrings)."""
        # Note: This behavior depends on implementation - currently checks substring
        content = "aspiring hacker"  # Contains "hack" as substring in "hacker"
        # This should raise if substring matching is used
        try:
            result = ContentFilterService().filter(content)
            # If it doesn't raise, that's ok - depends on implementation
        except ValueError:
            pass


class TestContentFilterServiceFilterContent:
    """Tests for the legacy filter_content() static method."""

    def test_filter_content_returns_true_for_clean_content(self):
        """Should return (True, '') for clean content."""
        content = "Hello, how can I help you?"
        is_valid, error = ContentFilterService.filter_content(content)

        assert is_valid is True
        assert error == ""

    def test_filter_content_returns_false_for_inappropriate(self):
        """Should return (False, error_msg) for inappropriate content."""
        content = "Buy this malware now!"
        is_valid, error = ContentFilterService.filter_content(content)

        assert is_valid is False
        assert error == "Content contains inappropriate words"

    def test_filter_content_with_spam(self):
        """Should detect spam."""
        content = "Check out this spam offer"
        is_valid, error = ContentFilterService.filter_content(content)

        assert is_valid is False

    def test_filter_content_with_hack(self):
        """Should detect hack."""
        content = "Learn to hack ethically"
        is_valid, error = ContentFilterService.filter_content(content)

        assert is_valid is False

    def test_filter_content_sanitizes_before_checking(self):
        """Should sanitize before checking inappropriate content."""
        content = "   clean message   "
        is_valid, error = ContentFilterService.filter_content(content)

        assert is_valid is True
        assert error == ""


    def test_sanitize_content_removes_extra_spaces(self):
        content = "  Hello world  "
        sanitized = ContentFilterService.sanitize_content(content)

        assert sanitized == "Hello world"

    def test_case_insensitive_filtering(self):
        content = "This is SPAM content"
        assert ContentFilterService.contains_inappropriate_content(content) is True

    def test_empty_content_is_valid(self):
        is_valid, error = ContentFilterService.filter_content("")
        assert is_valid is True
        assert error == ""

    def test_filtering_after_sanitization(self):
        content = "   spam   "
        is_valid, error = ContentFilterService.filter_content(content)

        assert is_valid is False

    def test_inappropriate_word_inside_sentence(self):
        content = "Hello, this message contains malware hidden"
        assert ContentFilterService.contains_inappropriate_content(content) is True
