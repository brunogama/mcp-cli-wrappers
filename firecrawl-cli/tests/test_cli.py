"""Unit tests for Firecrawl CLI wrapper."""

import argparse
import json
import sys
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


# Import after patching to avoid import-time issues
@pytest.fixture
def cli_module():
    """Import CLI module with mocked dependencies."""
    with patch.dict("sys.modules", {"fastmcp": MagicMock(), "fastmcp.client.transports": MagicMock()}):
        # Reset the module if already imported
        if "cli" in sys.modules:
            del sys.modules["cli"]
        
        # Mock the transport before import
        sys.path.insert(0, "/Users/bruno/cli-wrappers/firecrawl-cli")
        import cli
        return cli


class TestQuickHelp:
    """Test Level 1: Quick help."""

    def test_quick_help_contains_functions(self, cli_module):
        """QUICK_HELP should list all available functions."""
        assert "scrape" in cli_module.QUICK_HELP
        assert "crawl" in cli_module.QUICK_HELP
        assert "extract" in cli_module.QUICK_HELP
        assert "map" in cli_module.QUICK_HELP
        assert "search" in cli_module.QUICK_HELP

    def test_quick_help_contains_examples(self, cli_module):
        """QUICK_HELP should have quick start examples."""
        assert "uv run cli.py" in cli_module.QUICK_HELP


class TestFunctionInfo:
    """Test Level 2: Function info."""

    def test_all_functions_have_info(self, cli_module):
        """All functions should have entries in FUNCTION_INFO."""
        expected = ["scrape", "crawl", "extract", "map", "search"]
        for func in expected:
            assert func in cli_module.FUNCTION_INFO, f"Missing function: {func}"

    def test_function_info_has_required_fields(self, cli_module):
        """Each function info should have description, parameters, returns."""
        for name, info in cli_module.FUNCTION_INFO.items():
            assert "description" in info, f"{name} missing description"
            assert "parameters" in info, f"{name} missing parameters"
            assert "returns" in info, f"{name} missing returns"

    def test_scrape_has_url_parameter(self, cli_module):
        """Scrape function should have required url parameter."""
        scrape_info = cli_module.FUNCTION_INFO["scrape"]
        params = {p["name"]: p for p in scrape_info["parameters"]}
        assert "url" in params
        assert params["url"]["required"] is True


class TestFunctionExamples:
    """Test Level 3: Function examples."""

    def test_all_functions_have_examples(self, cli_module):
        """All functions should have examples."""
        for func in cli_module.FUNCTION_INFO.keys():
            assert func in cli_module.FUNCTION_EXAMPLES, f"Missing examples for: {func}"

    def test_examples_have_required_fields(self, cli_module):
        """Each example should have title and command."""
        for name, examples in cli_module.FUNCTION_EXAMPLES.items():
            assert len(examples) > 0, f"No examples for {name}"
            for ex in examples:
                assert "title" in ex, f"Example missing title in {name}"
                assert "command" in ex, f"Example missing command in {name}"


class TestValidateCredentials:
    """Test credential validation."""

    def test_missing_api_key(self, cli_module):
        """Should return False when API key is missing."""
        with patch.dict("os.environ", {}, clear=True):
            assert cli_module.validate_credentials() is False

    def test_valid_api_key(self, cli_module):
        """Should return True when API key is set."""
        with patch.dict("os.environ", {"FIRECRAWL_API_KEY": "fc-test-key"}):
            assert cli_module.validate_credentials() is True


class TestFormatOutput:
    """Test output formatting."""

    def test_json_format(self, cli_module, capsys):
        """JSON format should output valid JSON."""
        data = {"key": "value", "nested": {"a": 1}}
        cli_module.format_output(data, "json")
        captured = capsys.readouterr()
        parsed = json.loads(captured.out)
        assert parsed == data

    def test_text_format_dict(self, cli_module, capsys):
        """Text format should print key-value pairs."""
        data = {"name": "test", "value": 123}
        cli_module.format_output(data, "text")
        captured = capsys.readouterr()
        assert "name: test" in captured.out
        assert "value: 123" in captured.out


class TestShowFunctionInfo:
    """Test show_function_info output."""

    def test_unknown_function_exits(self, cli_module):
        """Should exit with error for unknown function."""
        with pytest.raises(SystemExit) as exc_info:
            cli_module.show_function_info("nonexistent")
        assert exc_info.value.code == 1

    def test_valid_function_shows_info(self, cli_module, capsys):
        """Should show function info for valid function."""
        cli_module.show_function_info("scrape")
        captured = capsys.readouterr()
        assert "scrape" in captured.out
        assert "Description" in captured.out


class TestShowFunctionExample:
    """Test show_function_example output."""

    def test_unknown_function_exits(self, cli_module):
        """Should exit with error for unknown function."""
        with pytest.raises(SystemExit) as exc_info:
            cli_module.show_function_example("nonexistent")
        assert exc_info.value.code == 1

    def test_valid_function_shows_examples(self, cli_module, capsys):
        """Should show examples for valid function."""
        cli_module.show_function_example("scrape")
        captured = capsys.readouterr()
        assert "Example" in captured.out
        assert "scrape" in captured.out
