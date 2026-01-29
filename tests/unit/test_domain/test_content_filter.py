"""
Unit tests for ContentFilterService domain service.
"""
import pytest
from src.Domain.services.content_filter import ContentFilterService


class TestContentFilterService:
    """Tests for ContentFilterService domain service."""
    
    def test_contains_inappropriate_content_with_spam(self):
        """Test detection of inappropriate content."""
        content = "This is spam content"
        assert ContentFilterService.contains_inappropriate_content(content) is True
    
    def test_contains_inappropriate_content_with_clean_content(self):
        """Test clean content passes the filter."""
        content = "This is a clean message"
        assert ContentFilterService.contains_inappropriate_content(content) is False
    
    def test_filter_content_returns_false_for_inappropriate(self):
        """Test filter_content returns False for inappropriate content."""
        content = "Buy this malware now!"
        is_valid, error = ContentFilterService.filter_content(content)
        
        assert is_valid is False
        assert error == "Content contains inappropriate words"
    
    def test_filter_content_returns_true_for_clean_content(self):
        """Test filter_content returns True for clean content."""
        content = "Hello, how can I help you?"
        is_valid, error = ContentFilterService.filter_content(content)
        
        assert is_valid is True
        assert error == ""
    
    def test_sanitize_content_removes_extra_spaces(self):
        """Test sanitize_content removes leading/trailing spaces."""
        content = "  Hello world  "
        sanitized = ContentFilterService.sanitize_content(content)
        
        assert sanitized == "Hello world"
    
    def test_case_insensitive_filtering(self):
        """Test that filtering is case-insensitive."""
        content = "This is SPAM content"
        assert ContentFilterService.contains_inappropriate_content(content) is True