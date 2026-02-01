"""Test fixtures for Brave Search CLI."""

import os
from typing import Any
from unittest.mock import patch

import pytest


@pytest.fixture
def mock_api_key():
    """Set mock API key for testing."""
    with patch.dict(os.environ, {"BRAVE_API_KEY": "test_api_key_12345"}):
        yield "test_api_key_12345"


@pytest.fixture
def mock_web_response() -> dict[str, Any]:
    """Mock web search API response."""
    return {
        "web": {
            "results": [
                {
                    "title": "Python Tutorial",
                    "url": "https://example.com/python",
                    "description": "Learn Python programming",
                },
                {
                    "title": "Python Documentation",
                    "url": "https://docs.python.org",
                    "description": "Official Python docs",
                },
            ]
        },
        "query": {"original": "python tutorial"},
    }


@pytest.fixture
def mock_video_response() -> dict[str, Any]:
    """Mock video search API response."""
    return {
        "results": [
            {
                "title": "Python Crash Course",
                "url": "https://youtube.com/watch?v=123",
                "description": "Complete Python tutorial",
                "duration": "3:45:00",
                "thumbnail": {"src": "https://img.youtube.com/123.jpg"},
            }
        ]
    }


@pytest.fixture
def mock_image_response() -> dict[str, Any]:
    """Mock image search API response."""
    return {
        "results": [
            {
                "title": "Mountain Landscape",
                "url": "https://example.com/image.jpg",
                "properties": {"width": 1920, "height": 1080},
            }
        ]
    }


@pytest.fixture
def mock_news_response() -> dict[str, Any]:
    """Mock news search API response."""
    return {
        "results": [
            {
                "title": "AI Breakthrough",
                "url": "https://news.example.com/ai",
                "description": "New AI development announced",
                "age": "2 hours ago",
                "source": {"name": "Tech News"},
            }
        ]
    }


@pytest.fixture
def mock_error_response() -> dict[str, Any]:
    """Mock API error response."""
    return {"error": "HTTP 401: Invalid API key"}
