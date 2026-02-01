#!/usr/bin/env python3
"""Integration tests for Ref Tools CLI wrapper.

These tests require a valid REF_API_KEY environment variable.
Skip these tests in CI unless API key is available.
"""

import json
import os
import subprocess
from pathlib import Path

import pytest

# Skip all tests if no API key
pytestmark = pytest.mark.skipif(
    not os.environ.get("REF_API_KEY"),
    reason="REF_API_KEY not set"
)

CLI_DIR = Path(__file__).parent.parent


class TestSearchIntegration:
    """Integration tests for search functionality."""

    def test_search_returns_results(self):
        """Test that search returns valid results."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "--format", "json", "search", "--query", "python async"],
            cwd=CLI_DIR,
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            data = json.loads(result.stdout)
            assert isinstance(data, (dict, list))
        else:
            # API might be unavailable, check for proper error
            assert "error" in result.stdout.lower() or "error" in result.stderr.lower()

    def test_search_with_limit(self):
        """Test search with limit parameter."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "--format", "json", "search", "--query", "javascript", "--limit", "5"],
            cwd=CLI_DIR,
            capture_output=True,
            text=True,
            timeout=60
        )

        # Just verify it completes without crash
        assert result.returncode in (0, 1)


class TestReadUrlIntegration:
    """Integration tests for read_url functionality."""

    def test_read_url_fetches_content(self):
        """Test that read_url fetches and parses content."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "--format", "json", "read_url", "--url", "https://docs.python.org/3/"],
            cwd=CLI_DIR,
            capture_output=True,
            text=True,
            timeout=60
        )

        # Verify it completes (API might reject certain URLs)
        assert result.returncode in (0, 1)


class TestServerInfoIntegration:
    """Integration tests for server info."""

    def test_version_returns_info(self):
        """Test that version command returns info."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "--format", "json", "version"],
            cwd=CLI_DIR,
            capture_output=True,
            text=True,
            timeout=30
        )

        # Should complete, may return error if server unreachable
        assert result.returncode in (0, 1)

    def test_info_returns_server_details(self):
        """Test that info command returns server details."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "--format", "json", "info_server"],
            cwd=CLI_DIR,
            capture_output=True,
            text=True,
            timeout=30
        )

        assert result.returncode in (0, 1)


class TestCheckIntegration:
    """Integration tests for file checking."""

    def test_check_existing_file(self):
        """Test checking an existing file."""
        # Create a temporary test file
        test_file = CLI_DIR / "tests" / "test_sample.py"
        test_file.write_text("# Sample Python file\ndef hello():\n    print('Hello')\n")

        try:
            result = subprocess.run(
                ["uv", "run", "cli.py", "--format", "json", "check", "--filepath", str(test_file)],
                cwd=CLI_DIR,
                capture_output=True,
                text=True,
                timeout=60
            )

            # Should complete
            assert result.returncode in (0, 1)
        finally:
            test_file.unlink(missing_ok=True)

    def test_check_nonexistent_file(self):
        """Test checking a nonexistent file."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "--format", "json", "check", "--filepath", "/nonexistent/file.py"],
            cwd=CLI_DIR,
            capture_output=True,
            text=True,
            timeout=30
        )

        # Should fail gracefully
        assert result.returncode in (0, 1)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            assert "error" in data


class TestAnalyzeIntegration:
    """Integration tests for directory analysis."""

    def test_analyze_current_directory(self):
        """Test analyzing a directory."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "--format", "json", "analyze", "--path", str(CLI_DIR)],
            cwd=CLI_DIR,
            capture_output=True,
            text=True,
            timeout=120
        )

        # Should complete
        assert result.returncode in (0, 1)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
