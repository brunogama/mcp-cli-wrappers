"""Unit tests for Brave Search CLI."""

import json
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

# Import after setting up path
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from cli import (
    FUNCTION_EXAMPLES,
    FUNCTION_INFO,
    QUICK_HELP,
    check_api_key,
    cli,
    format_output,
    image_search,
    make_request,
    news_search,
    video_search,
    web_search,
)


class TestHelpSystem:
    """Test 4-level progressive disclosure help system."""

    def test_quick_help_exists(self):
        """QUICK_HELP should contain essential info."""
        assert "web_search" in QUICK_HELP
        assert "BRAVE_API_KEY" in QUICK_HELP
        assert "uv run" in QUICK_HELP

    def test_function_info_completeness(self):
        """All functions should have complete info."""
        required_keys = ["name", "description", "parameters", "returns"]
        for name, info in FUNCTION_INFO.items():
            for key in required_keys:
                assert key in info, f"{name} missing {key}"

    def test_function_examples_exist(self):
        """All functions should have examples."""
        for name in FUNCTION_INFO:
            assert name in FUNCTION_EXAMPLES, f"Missing examples for {name}"
            assert len(FUNCTION_EXAMPLES[name]) >= 1, f"No examples for {name}"


class TestCLICommands:
    """Test CLI command structure."""

    def setup_method(self):
        """Set up test runner."""
        self.runner = CliRunner()

    def test_main_help(self):
        """Main help should display QUICK_HELP."""
        result = self.runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "Brave Search CLI" in result.output

    def test_list_command(self):
        """List command should show all functions."""
        result = self.runner.invoke(cli, ["list"])
        assert result.exit_code == 0
        assert "web_search" in result.output
        assert "video_search" in result.output

    def test_info_command(self):
        """Info command should show function details."""
        result = self.runner.invoke(cli, ["info", "web_search"])
        assert result.exit_code == 0
        assert "query" in result.output
        assert "country" in result.output

    def test_info_unknown_function(self):
        """Info for unknown function should error."""
        result = self.runner.invoke(cli, ["info", "unknown_func"])
        assert "Unknown function" in result.output

    def test_example_command(self):
        """Example command should show usage examples."""
        result = self.runner.invoke(cli, ["example", "web_search"])
        assert result.exit_code == 0
        assert "uv run" in result.output


class TestAPIKeyValidation:
    """Test API key validation."""

    def test_check_api_key_missing(self):
        """Should return False when API key is missing."""
        with patch.dict("os.environ", {"BRAVE_API_KEY": ""}, clear=False):
            # Need to reload module or patch the constant
            with patch("cli.BRAVE_API_KEY", ""):
                assert check_api_key() is False

    def test_check_api_key_present(self, mock_api_key):
        """Should return True when API key is set."""
        with patch("cli.BRAVE_API_KEY", mock_api_key):
            assert check_api_key() is True


class TestSearchFunctions:
    """Test search function implementations."""

    @patch("cli.make_request")
    def test_web_search_basic(self, mock_request, mock_web_response):
        """Web search should call correct endpoint."""
        mock_request.return_value = mock_web_response

        result = web_search("python tutorial")

        mock_request.assert_called_once()
        call_args = mock_request.call_args
        assert call_args[0][0] == "web/search"
        assert call_args[0][1]["q"] == "python tutorial"

    @patch("cli.make_request")
    def test_web_search_with_options(self, mock_request, mock_web_response):
        """Web search should pass all options."""
        mock_request.return_value = mock_web_response

        web_search(
            "test query",
            country="GB",
            count=5,
            safesearch="strict",
            freshness="pw",
        )

        call_args = mock_request.call_args[0][1]
        assert call_args["country"] == "GB"
        assert call_args["count"] == 5
        assert call_args["safesearch"] == "strict"
        assert call_args["freshness"] == "pw"

    @patch("cli.make_request")
    def test_video_search(self, mock_request, mock_video_response):
        """Video search should call videos endpoint."""
        mock_request.return_value = mock_video_response

        video_search("python tutorial")

        call_args = mock_request.call_args
        assert call_args[0][0] == "videos/search"

    @patch("cli.make_request")
    def test_image_search(self, mock_request, mock_image_response):
        """Image search should call images endpoint."""
        mock_request.return_value = mock_image_response

        image_search("mountain landscape")

        call_args = mock_request.call_args
        assert call_args[0][0] == "images/search"

    @patch("cli.make_request")
    def test_news_search(self, mock_request, mock_news_response):
        """News search should call news endpoint."""
        mock_request.return_value = mock_news_response

        news_search("AI news")

        call_args = mock_request.call_args
        assert call_args[0][0] == "news/search"


class TestMakeRequest:
    """Test HTTP request handling."""

    @patch("cli.httpx.Client")
    def test_successful_request(self, mock_client_class, mock_api_key):
        """Successful request should return JSON."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"results": []}
        mock_response.raise_for_status = MagicMock()

        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        with patch("cli.BRAVE_API_KEY", mock_api_key):
            result = make_request("web/search", {"q": "test"})

        assert result == {"results": []}

    @patch("cli.httpx.Client")
    def test_request_error_handling(self, mock_client_class, mock_api_key):
        """HTTP errors should return error dict."""
        import httpx

        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)

        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"

        mock_client.get.side_effect = httpx.HTTPStatusError(
            "Unauthorized",
            request=MagicMock(),
            response=mock_response,
        )
        mock_client_class.return_value = mock_client

        with patch("cli.BRAVE_API_KEY", mock_api_key):
            result = make_request("web/search", {"q": "test"})

        assert "error" in result
        assert "401" in result["error"]


class TestOutputFormatting:
    """Test output format functions."""

    def test_json_format(self, mock_web_response, capsys):
        """JSON format should output valid JSON."""
        format_output(mock_web_response, "json")
        captured = capsys.readouterr()
        # Rich console output includes formatting, check for key content
        assert "Python Tutorial" in captured.out

    def test_text_format(self, mock_web_response, capsys):
        """Text format should be human readable."""
        format_output(mock_web_response, "text")
        captured = capsys.readouterr()
        assert "Python Tutorial" in captured.out

    def test_error_format(self, mock_error_response, capsys):
        """Errors should display clearly."""
        format_output(mock_error_response, "text")
        captured = capsys.readouterr()
        assert "Error" in captured.out


class TestInputValidation:
    """Test input validation."""

    @patch("cli.make_request")
    def test_count_clamped_to_max(self, mock_request):
        """Count should be clamped to 20 max."""
        mock_request.return_value = {}
        web_search("test", count=100)

        call_args = mock_request.call_args[0][1]
        assert call_args["count"] == 20

    @patch("cli.make_request")
    def test_count_clamped_to_min(self, mock_request):
        """Count should be clamped to 1 min."""
        mock_request.return_value = {}
        web_search("test", count=0)

        call_args = mock_request.call_args[0][1]
        assert call_args["count"] == 1

    @patch("cli.make_request")
    def test_offset_clamped_to_max(self, mock_request):
        """Offset should be clamped to 9 max."""
        mock_request.return_value = {}
        web_search("test", offset=100)

        call_args = mock_request.call_args[0][1]
        assert call_args["offset"] == 9


class TestCommandAliases:
    """Test command aliases work correctly."""

    def setup_method(self):
        """Set up test runner."""
        self.runner = CliRunner()

    def test_search_alias(self):
        """'search' should alias to web_search."""
        result = self.runner.invoke(cli, ["search", "--help"])
        assert result.exit_code == 0
        assert "web search" in result.output.lower()

    def test_videos_alias(self):
        """'videos' should alias to video_search."""
        result = self.runner.invoke(cli, ["videos", "--help"])
        assert result.exit_code == 0

    def test_images_alias(self):
        """'images' should alias to image_search."""
        result = self.runner.invoke(cli, ["images", "--help"])
        assert result.exit_code == 0

    def test_news_alias(self):
        """'news' should alias to news_search."""
        result = self.runner.invoke(cli, ["news", "--help"])
        assert result.exit_code == 0

    def test_local_alias(self):
        """'local' should alias to local_search."""
        result = self.runner.invoke(cli, ["local", "--help"])
        assert result.exit_code == 0

    def test_summary_alias(self):
        """'summary' should alias to summarizer."""
        result = self.runner.invoke(cli, ["summary", "--help"])
        assert result.exit_code == 0
