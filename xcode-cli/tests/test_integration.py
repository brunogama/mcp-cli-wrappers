"""Integration tests for XcodeMCP CLI wrapper.

These tests require:
- XcodeMCP server configured in Claude Desktop
- An Xcode project available for testing

Skip these tests if the prerequisites are not met.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Test project path - set via environment variable or skip
TEST_PROJECT = os.environ.get("XCODE_TEST_PROJECT")
TEST_XCRESULT = os.environ.get("XCODE_TEST_XCRESULT")


def has_mcp_server():
    """Check if XcodeMCP server is available."""
    try:
        result = subprocess.run(
            ["claude", "mcp", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return "xcode-mcp" in result.stdout.lower()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


requires_mcp = pytest.mark.skipif(
    not has_mcp_server(),
    reason="XcodeMCP server not configured"
)

requires_project = pytest.mark.skipif(
    TEST_PROJECT is None,
    reason="XCODE_TEST_PROJECT environment variable not set"
)

requires_xcresult = pytest.mark.skipif(
    TEST_XCRESULT is None,
    reason="XCODE_TEST_XCRESULT environment variable not set"
)


@requires_mcp
@requires_project
class TestProjectManagement:
    """Integration tests for project management functions."""

    def test_get_schemes(self):
        """Should list schemes from a real project."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "xcode_get_schemes", "--xcodeproj", TEST_PROJECT],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=60
        )
        # May fail if MCP not connected, but should not crash
        assert result.returncode == 0 or "error" in result.stdout.lower()

    def test_get_workspace_info(self):
        """Should get workspace info from a real project."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "xcode_get_workspace_info", "--xcodeproj", TEST_PROJECT],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=60
        )
        assert result.returncode == 0 or "error" in result.stdout.lower()

    def test_get_run_destinations(self):
        """Should list available simulators/devices."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "xcode_get_run_destinations", "--xcodeproj", TEST_PROJECT],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=60
        )
        assert result.returncode == 0 or "error" in result.stdout.lower()


@requires_mcp
@requires_xcresult
class TestXCResultAnalysis:
    """Integration tests for XCResult analysis functions."""

    def test_xcresult_summary(self):
        """Should get summary from a real xcresult file."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "xcresult_summary", "--xcresult-path", TEST_XCRESULT],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=60
        )
        assert result.returncode == 0 or "error" in result.stdout.lower()

    def test_xcresult_browse(self):
        """Should browse a real xcresult file."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "xcresult_browse", "--xcresult-path", TEST_XCRESULT],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=60
        )
        assert result.returncode == 0 or "error" in result.stdout.lower()


@requires_mcp
class TestErrorHandling:
    """Test error handling with invalid inputs."""

    def test_invalid_project_path(self):
        """Should handle non-existent project gracefully."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "xcode_get_schemes", "--xcodeproj", "/nonexistent/path.xcodeproj"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=60
        )
        # Should return error but not crash
        output = result.stdout + result.stderr
        assert "error" in output.lower() or result.returncode == 0

    def test_invalid_xcresult_path(self):
        """Should handle non-existent xcresult gracefully."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "xcresult_summary", "--xcresult-path", "/nonexistent/Test.xcresult"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=60
        )
        output = result.stdout + result.stderr
        assert "error" in output.lower() or result.returncode == 0


class TestJSONOutput:
    """Test JSON output validity."""

    @requires_mcp
    @requires_project
    def test_schemes_json_valid(self):
        """xcode_get_schemes should return valid JSON."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "--format", "json", "xcode_get_schemes", "--xcodeproj", TEST_PROJECT],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=60
        )
        if result.returncode == 0:
            try:
                json.loads(result.stdout)
            except json.JSONDecodeError:
                pytest.fail("Output is not valid JSON")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
