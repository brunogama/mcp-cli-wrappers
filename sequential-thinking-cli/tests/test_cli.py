#!/usr/bin/env python3
"""Unit tests for Sequential Thinking CLI wrapper."""

import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestQuickHelp:
    """Test Level 1: --help output."""

    def test_help_shows_quick_overview(self):
        """--help should show quick overview."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "--help"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=30,
        )
        assert result.returncode == 0
        assert "Sequential Thinking" in result.stdout
        assert "sequentialthinking" in result.stdout

    def test_no_args_shows_help(self):
        """No arguments should show help."""
        result = subprocess.run(
            ["uv", "run", "cli.py"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=30,
        )
        assert result.returncode == 0
        assert "Available functions" in result.stdout


class TestFunctionList:
    """Test Level 2: list command."""

    def test_list_shows_functions(self):
        """list should show all available functions."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "list"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=30,
        )
        assert result.returncode == 0
        assert "sequentialthinking" in result.stdout

    def test_list_json_format(self):
        """list --format json should return valid JSON."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "--format", "json", "list"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=30,
        )
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert "functions" in data
        assert "count" in data
        assert data["count"] > 0


class TestFunctionInfo:
    """Test Level 2: info command."""

    def test_info_shows_function_details(self):
        """info FUNCTION should show detailed documentation."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "info", "sequentialthinking"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=30,
        )
        assert result.returncode == 0
        assert "sequentialthinking" in result.stdout
        assert "Parameters" in result.stdout
        assert "thought" in result.stdout

    def test_info_json_format(self):
        """info --format json should return valid JSON."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "--format", "json", "info", "sequentialthinking"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=30,
        )
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert "description" in data
        assert "parameters" in data

    def test_info_unknown_function(self):
        """info with unknown function should error."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "info", "unknown_function"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=30,
        )
        assert result.returncode != 0
        assert "Unknown function" in result.stderr


class TestFunctionExamples:
    """Test Level 3: example command."""

    def test_example_shows_examples(self):
        """example FUNCTION should show working examples."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "example", "sequentialthinking"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=30,
        )
        assert result.returncode == 0
        assert "Example" in result.stdout
        assert "Command" in result.stdout

    def test_example_json_format(self):
        """example --format json should return valid JSON."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "--format", "json", "example", "sequentialthinking"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=30,
        )
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert "function" in data
        assert "examples" in data
        assert "count" in data
        assert len(data["examples"]) > 0

    def test_example_unknown_function(self):
        """example with unknown function should error."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "example", "unknown_function"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=30,
        )
        assert result.returncode != 0


class TestFunctionExecution:
    """Test Level 4: function execution."""

    def test_function_help(self):
        """FUNCTION --help should show complete reference."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "sequentialthinking", "--help"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=30,
        )
        assert result.returncode == 0
        assert "--thought" in result.stdout
        assert "--thoughtNumber" in result.stdout
        assert "--totalThoughts" in result.stdout
        assert "--nextThoughtNeeded" in result.stdout

    def test_missing_required_argument(self):
        """Missing required argument should error."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "sequentialthinking"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=30,
        )
        # Should fail due to missing required arguments
        assert result.returncode != 0


class TestOutputFormats:
    """Test output format options."""

    def test_text_format_default(self):
        """Default format should be text."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "list"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=30,
        )
        assert result.returncode == 0
        # Text format should not be valid JSON
        with pytest.raises(json.JSONDecodeError):
            json.loads(result.stdout)

    def test_json_format_valid(self):
        """--format json should produce valid JSON."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "--format", "json", "list"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=30,
        )
        assert result.returncode == 0
        # Should be valid JSON
        data = json.loads(result.stdout)
        assert isinstance(data, dict)


class TestVerboseMode:
    """Test verbose output."""

    def test_verbose_flag_accepted(self):
        """--verbose flag should be accepted."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "--verbose", "list"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=30,
        )
        assert result.returncode == 0


class TestFunctionInfoContent:
    """Test FUNCTION_INFO content."""

    def test_all_functions_have_description(self):
        """All functions should have descriptions."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "--format", "json", "list"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=30,
        )
        data = json.loads(result.stdout)
        for func in data["functions"]:
            assert "name" in func
            assert "description" in func
            assert len(func["description"]) > 0

    def test_function_parameters_documented(self):
        """Function parameters should be documented."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "--format", "json", "info", "sequentialthinking"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=30,
        )
        data = json.loads(result.stdout)
        assert "parameters" in data
        for param in data["parameters"]:
            assert "name" in param
            assert "type" in param
            assert "description" in param


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
