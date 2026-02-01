"""Tests for GitHub MCP CLI wrapper."""

import json
import os
import sys
from unittest.mock import patch

import pytest
from click.testing import CliRunner

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cli import cli, FUNCTION_INFO, FUNCTION_EXAMPLES, QUICK_HELP


@pytest.fixture
def runner():
    """Create CLI test runner."""
    return CliRunner()


@pytest.fixture
def mock_token():
    """Mock GITHUB_TOKEN environment variable."""
    with patch.dict(os.environ, {"GITHUB_TOKEN": "ghp_test_token"}):
        yield


class TestQuickHelp:
    """Test Level 1: Quick help."""

    def test_help_shows_quick_overview(self, runner):
        """--help shows quick overview."""
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "GitHub MCP CLI" in result.output

    def test_no_args_shows_quick_help(self, runner):
        """No arguments shows QUICK_HELP."""
        result = runner.invoke(cli, [])
        assert result.exit_code == 0
        assert "Namespaces:" in result.output


class TestListCommand:
    """Test Level 2: List all functions."""

    def test_list_shows_all_namespaces(self, runner):
        """List command shows all namespaces."""
        result = runner.invoke(cli, ["list"])
        assert result.exit_code == 0
        assert "repo." in result.output or "issue." in result.output

    def test_list_json_format(self, runner):
        """List command with JSON format."""
        result = runner.invoke(cli, ["--format", "json", "list"])
        assert result.exit_code == 0
        # Should be valid JSON
        data = json.loads(result.output)
        assert isinstance(data, dict)


class TestInfoCommand:
    """Test Level 2: Function info."""

    def test_info_shows_function_details(self, runner):
        """Info command shows function details."""
        result = runner.invoke(cli, ["info", "create_pull_request"])
        assert result.exit_code == 0
        assert "create_pull_request" in result.output
        assert "Parameters:" in result.output

    def test_info_unknown_function(self, runner):
        """Info command handles unknown function."""
        result = runner.invoke(cli, ["info", "nonexistent_function"])
        assert result.exit_code == 1
        assert "Unknown function" in result.output

    def test_info_json_format(self, runner):
        """Info command with JSON format."""
        result = runner.invoke(cli, ["--format", "json", "info", "list_issues"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "description" in data
        assert "parameters" in data


class TestExampleCommand:
    """Test Level 3: Function examples."""

    def test_example_shows_examples(self, runner):
        """Example command shows working examples."""
        result = runner.invoke(cli, ["example", "create_pull_request"])
        assert result.exit_code == 0
        assert "Example" in result.output
        assert "uv run" in result.output

    def test_example_no_examples(self, runner):
        """Example command handles function without examples."""
        result = runner.invoke(cli, ["example", "get_me"])
        assert result.exit_code == 1
        assert "No examples" in result.output


class TestFunctionCommands:
    """Test actual function commands."""

    def test_get_file_contents_requires_token(self, runner):
        """Commands require GITHUB_TOKEN."""
        with patch.dict(os.environ, {}, clear=True):
            os.environ.pop("GITHUB_TOKEN", None)
            result = runner.invoke(cli, [
                "get_file_contents",
                "--owner", "test",
                "--repo", "test",
            ])
            assert "GITHUB_TOKEN" in result.output

    def test_get_file_contents_with_token(self, runner, mock_token):
        """get_file_contents works with token."""
        result = runner.invoke(cli, [
            "get_file_contents",
            "--owner", "anthropics",
            "--repo", "claude-code",
            "--path", "README.md",
        ])
        assert result.exit_code == 0
        assert "stub" in result.output.lower() or "would" in result.output.lower()

    def test_create_pull_request(self, runner, mock_token):
        """create_pull_request parses all arguments."""
        result = runner.invoke(cli, [
            "create_pull_request",
            "--owner", "myorg",
            "--repo", "myrepo",
            "--title", "Test PR",
            "--head", "feature/test",
            "--base", "main",
        ])
        assert result.exit_code == 0

    def test_list_issues_with_filters(self, runner, mock_token):
        """list_issues accepts filter options."""
        result = runner.invoke(cli, [
            "list_issues",
            "--owner", "myorg",
            "--repo", "myrepo",
            "--state", "OPEN",
            "--labels", "bug,priority",
        ])
        assert result.exit_code == 0

    def test_search_issues(self, runner, mock_token):
        """search_issues parses query."""
        result = runner.invoke(cli, [
            "search_issues",
            "--query", "is:open label:bug",
        ])
        assert result.exit_code == 0

    def test_merge_pull_request(self, runner, mock_token):
        """merge_pull_request accepts merge method."""
        result = runner.invoke(cli, [
            "merge_pull_request",
            "--owner", "myorg",
            "--repo", "myrepo",
            "--pull_number", "123",
            "--merge_method", "squash",
        ])
        assert result.exit_code == 0

    def test_run_workflow(self, runner, mock_token):
        """run_workflow accepts inputs JSON."""
        result = runner.invoke(cli, [
            "run_workflow",
            "--owner", "myorg",
            "--repo", "myrepo",
            "--workflow_id", "deploy.yml",
            "--ref", "main",
            "--inputs", '{"env": "staging"}',
        ])
        assert result.exit_code == 0


class TestFunctionInfo:
    """Test FUNCTION_INFO completeness."""

    def test_all_functions_have_description(self):
        """All functions have description."""
        for name, info in FUNCTION_INFO.items():
            assert "description" in info, f"{name} missing description"
            assert len(info["description"]) > 10, f"{name} description too short"

    def test_all_functions_have_namespace(self):
        """All functions have namespace."""
        for name, info in FUNCTION_INFO.items():
            assert "namespace" in info, f"{name} missing namespace"

    def test_all_functions_have_returns(self):
        """All functions have returns."""
        for name, info in FUNCTION_INFO.items():
            assert "returns" in info, f"{name} missing returns"

    def test_parameters_have_required_fields(self):
        """All parameters have required fields."""
        for name, info in FUNCTION_INFO.items():
            for param in info.get("parameters", []):
                assert "name" in param, f"{name} param missing name"
                assert "type" in param, f"{name} param missing type"
                assert "required" in param, f"{name} param missing required"


class TestOutputFormats:
    """Test output format options."""

    def test_json_format(self, runner):
        """JSON format produces valid JSON."""
        result = runner.invoke(cli, ["--format", "json", "list"])
        assert result.exit_code == 0
        json.loads(result.output)  # Should not raise

    def test_text_format_default(self, runner):
        """Text format is default."""
        result = runner.invoke(cli, ["list"])
        assert result.exit_code == 0
        # Should contain human-readable text
        assert "Available Functions" in result.output or "repo" in result.output


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
