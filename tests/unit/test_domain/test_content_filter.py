"""
Unit tests for ContentFilterService domain service.
"""
import pytest
from src.Domain.services.content_filter import ContentFilterService


class TestContentFilterService:
    def test_contains_inappropriate_content_with_spam(self):
        content = "This is spam content"
        assert ContentFilterService.contains_inappropriate_content(content) is True

    def test_contains_inappropriate_content_with_clean_content(self):
        content = "This is a clean message"
        assert ContentFilterService.contains_inappropriate_content(content) is False

    def test_filter_content_returns_false_for_inappropriate(self):
        content = "Buy this malware now!"
        is_valid, error = ContentFilterService.filter_content(content)

        assert is_valid is False
        assert error == "Content contains inappropriate words"

    def test_filter_content_returns_true_for_clean_content(self):
        content = "Hello, how can I help you?"
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
