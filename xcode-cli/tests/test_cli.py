"""Unit tests for XcodeMCP CLI wrapper."""

import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestQuickHelp:
    """Test Level 1: Quick help output."""

    def test_help_returns_success(self):
        """--help should return exit code 0."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "--help"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=30
        )
        assert result.returncode == 0

    def test_help_contains_usage(self):
        """--help should contain USAGE section."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "--help"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=30
        )
        assert "USAGE" in result.stdout or "usage" in result.stdout.lower()

    def test_help_contains_categories(self):
        """--help should mention categories."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "--help"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=30
        )
        assert "Project Management" in result.stdout or "Build Operations" in result.stdout


class TestListCommand:
    """Test Level 2: List command."""

    def test_list_returns_success(self):
        """list should return exit code 0."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "list"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=30
        )
        assert result.returncode == 0

    def test_list_shows_categories(self):
        """list should show all categories."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "list"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=30
        )
        assert "Project Management" in result.stdout
        assert "Build Operations" in result.stdout
        assert "Configuration" in result.stdout
        assert "XCResult Analysis" in result.stdout

    def test_list_shows_functions(self):
        """list should show key functions."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "list"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=30
        )
        assert "xcode_build" in result.stdout
        assert "xcode_test" in result.stdout
        assert "xcresult_summary" in result.stdout


class TestInfoCommand:
    """Test Level 2: Info command."""

    def test_info_xcode_build(self):
        """info xcode_build should show parameters."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "info", "xcode_build"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=30
        )
        assert result.returncode == 0
        assert "xcodeproj" in result.stdout
        assert "scheme" in result.stdout

    def test_info_unknown_function(self):
        """info with unknown function should error."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "info", "nonexistent_function"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=30
        )
        assert result.returncode != 0
        assert "Unknown function" in result.stdout or "Unknown function" in result.stderr

    def test_info_shows_related(self):
        """info should show related functions."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "info", "xcode_build"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=30
        )
        assert "Related" in result.stdout


class TestExampleCommand:
    """Test Level 3: Example command."""

    def test_example_xcode_build(self):
        """example xcode_build should show examples."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "example", "xcode_build"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=30
        )
        assert result.returncode == 0
        assert "Example" in result.stdout

    def test_example_xcode_test(self):
        """example xcode_test should show test examples."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "example", "xcode_test"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=30
        )
        assert result.returncode == 0
        assert "--xcodeproj" in result.stdout


class TestFunctionHelp:
    """Test Level 4: Function-specific help."""

    def test_xcode_build_help(self):
        """xcode_build --help should show all options."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "xcode_build", "--help"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=30
        )
        assert result.returncode == 0
        assert "--xcodeproj" in result.stdout
        assert "--scheme" in result.stdout
        assert "--destination" in result.stdout

    def test_xcode_test_help(self):
        """xcode_test --help should show all options."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "xcode_test", "--help"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=30
        )
        assert result.returncode == 0
        assert "--xcodeproj" in result.stdout
        assert "--destination" in result.stdout
        assert "--selected-tests" in result.stdout
        assert "--test-plan-path" in result.stdout


class TestRequiredArguments:
    """Test that required arguments are enforced."""

    def test_xcode_build_requires_xcodeproj(self):
        """xcode_build should require --xcodeproj."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "xcode_build", "--scheme", "MyApp"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=30
        )
        assert result.returncode != 0
        assert "xcodeproj" in result.stderr.lower() or "required" in result.stderr.lower()

    def test_xcode_build_requires_scheme(self):
        """xcode_build should require --scheme."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "xcode_build", "--xcodeproj", "/path/to/project"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=30
        )
        assert result.returncode != 0
        assert "scheme" in result.stderr.lower() or "required" in result.stderr.lower()


class TestOutputFormats:
    """Test output format options."""

    def test_format_json_option_accepted(self):
        """--format json should be accepted."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "--format", "json", "list"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=30
        )
        assert result.returncode == 0

    def test_format_text_option_accepted(self):
        """--format text should be accepted."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "--format", "text", "list"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=30
        )
        assert result.returncode == 0

    def test_format_table_option_accepted(self):
        """--format table should be accepted."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "--format", "table", "list"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=30
        )
        assert result.returncode == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
