#!/usr/bin/env python3
"""Unit tests for Ref Tools CLI wrapper."""

import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestCliHelp:
    """Test CLI help and discovery commands."""

    def test_help_returns_success(self):
        """Test that --help returns exit code 0."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "--help"],
            cwd=Path(__file__).parent.parent,
            capture_output=True,
            text=True,
            timeout=30
        )
        assert result.returncode == 0
        assert "Ref Tools MCP CLI" in result.stdout

    def test_list_returns_functions(self):
        """Test that list command shows available functions."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "list"],
            cwd=Path(__file__).parent.parent,
            capture_output=True,
            text=True,
            timeout=30
        )
        assert result.returncode == 0
        assert "search" in result.stdout
        assert "read_url" in result.stdout

    def test_list_json_format(self):
        """Test list command with JSON output."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "--format", "json", "list"],
            cwd=Path(__file__).parent.parent,
            capture_output=True,
            text=True,
            timeout=30
        )
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert "functions" in data
        assert "count" in data

    def test_info_search(self):
        """Test info command for search function."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "info", "search"],
            cwd=Path(__file__).parent.parent,
            capture_output=True,
            text=True,
            timeout=30
        )
        assert result.returncode == 0
        assert "search" in result.stdout.lower()
        assert "query" in result.stdout.lower()

    def test_info_unknown_function(self):
        """Test info command with unknown function."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "info", "nonexistent"],
            cwd=Path(__file__).parent.parent,
            capture_output=True,
            text=True,
            timeout=30
        )
        assert result.returncode == 1
        assert "Unknown function" in result.stderr

    def test_example_search(self):
        """Test example command for search function."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "example", "search"],
            cwd=Path(__file__).parent.parent,
            capture_output=True,
            text=True,
            timeout=30
        )
        assert result.returncode == 0
        assert "Example" in result.stdout
        assert "search" in result.stdout.lower()


class TestCliConfig:
    """Test CLI configuration commands."""

    def test_config_shows_settings(self):
        """Test that config command shows settings."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "config"],
            cwd=Path(__file__).parent.parent,
            capture_output=True,
            text=True,
            timeout=30,
            env={"REF_API_KEY": "test-key-12345678"}
        )
        assert result.returncode == 0
        # Key should be masked
        assert "test" in result.stdout or "..." in result.stdout

    def test_config_json_format(self):
        """Test config with JSON output."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "--format", "json", "config"],
            cwd=Path(__file__).parent.parent,
            capture_output=True,
            text=True,
            timeout=30,
            env={"REF_API_KEY": "test-key-12345678"}
        )
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert "api_key" in data
        assert "api_url" in data


class TestCliValidation:
    """Test CLI argument validation."""

    def test_search_requires_query(self):
        """Test that search command requires --query."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "search"],
            cwd=Path(__file__).parent.parent,
            capture_output=True,
            text=True,
            timeout=30
        )
        assert result.returncode != 0
        assert "required" in result.stderr.lower() or "query" in result.stderr.lower()

    def test_read_url_requires_url(self):
        """Test that read_url command requires --url."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "read_url"],
            cwd=Path(__file__).parent.parent,
            capture_output=True,
            text=True,
            timeout=30
        )
        assert result.returncode != 0
        assert "required" in result.stderr.lower() or "url" in result.stderr.lower()

    def test_check_requires_filepath(self):
        """Test that check command requires --filepath."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "check"],
            cwd=Path(__file__).parent.parent,
            capture_output=True,
            text=True,
            timeout=30
        )
        assert result.returncode != 0

    def test_analyze_requires_path(self):
        """Test that analyze command requires --path."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "analyze"],
            cwd=Path(__file__).parent.parent,
            capture_output=True,
            text=True,
            timeout=30
        )
        assert result.returncode != 0


class TestApiKeyValidation:
    """Test API key validation."""

    def test_search_without_api_key_fails(self):
        """Test that search fails without API key."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "search", "--query", "test"],
            cwd=Path(__file__).parent.parent,
            capture_output=True,
            text=True,
            timeout=30,
            env={"REF_API_KEY": ""}  # Empty key
        )
        assert result.returncode != 0
        assert "API" in result.stdout or "key" in result.stdout.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
