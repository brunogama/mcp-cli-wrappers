#!/usr/bin/env python3
"""Integration tests for Sequential Thinking CLI wrapper.

These tests require the MCP server to be available.
Skip with: pytest -m "not integration"
"""

import json
import subprocess
from pathlib import Path

import pytest


# Mark all tests in this file as integration tests
pytestmark = pytest.mark.integration


class TestMCPDiscovery:
    """Test MCP server discovery."""

    @pytest.mark.skip(reason="Requires MCP server to be running")
    def test_discover_tools(self):
        """--discover should list tools from MCP server."""
        result = subprocess.run(
            ["uv", "run", "cli.py", "--format", "json", "--discover"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=60,
        )
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert "tools" in data
        assert "count" in data


class TestSequentialThinkingExecution:
    """Test actual function execution against MCP server."""

    @pytest.mark.skip(reason="Requires MCP server to be running")
    def test_basic_thought(self):
        """Execute a basic thought step."""
        result = subprocess.run(
            [
                "uv", "run", "cli.py", "--format", "json", "sequentialthinking",
                "--thought", "Test thought for integration testing",
                "--thoughtNumber", "1",
                "--totalThoughts", "1",
                "--nextThoughtNeeded", "false",
            ],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=60,
        )
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert "thoughtNumber" in data or "error" not in data

    @pytest.mark.skip(reason="Requires MCP server to be running")
    def test_thought_chain(self):
        """Execute a multi-step thought chain."""
        # Step 1
        result1 = subprocess.run(
            [
                "uv", "run", "cli.py", "--format", "json", "sequentialthinking",
                "--thought", "First step: identify the problem",
                "--thoughtNumber", "1",
                "--totalThoughts", "3",
                "--nextThoughtNeeded", "true",
            ],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=60,
        )
        assert result1.returncode == 0

        # Step 2
        result2 = subprocess.run(
            [
                "uv", "run", "cli.py", "--format", "json", "sequentialthinking",
                "--thought", "Second step: analyze options",
                "--thoughtNumber", "2",
                "--totalThoughts", "3",
                "--nextThoughtNeeded", "true",
            ],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=60,
        )
        assert result2.returncode == 0

        # Step 3 (final)
        result3 = subprocess.run(
            [
                "uv", "run", "cli.py", "--format", "json", "sequentialthinking",
                "--thought", "Third step: conclusion",
                "--thoughtNumber", "3",
                "--totalThoughts", "3",
                "--nextThoughtNeeded", "false",
            ],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=60,
        )
        assert result3.returncode == 0

    @pytest.mark.skip(reason="Requires MCP server to be running")
    def test_thought_revision(self):
        """Execute a thought revision."""
        result = subprocess.run(
            [
                "uv", "run", "cli.py", "--format", "json", "sequentialthinking",
                "--thought", "Revised understanding",
                "--thoughtNumber", "2",
                "--totalThoughts", "3",
                "--nextThoughtNeeded", "true",
                "--isRevision", "true",
                "--revisesThought", "1",
            ],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=60,
        )
        assert result.returncode == 0

    @pytest.mark.skip(reason="Requires MCP server to be running")
    def test_thought_branch(self):
        """Execute a thought branch."""
        result = subprocess.run(
            [
                "uv", "run", "cli.py", "--format", "json", "sequentialthinking",
                "--thought", "Alternative approach",
                "--thoughtNumber", "2",
                "--totalThoughts", "3",
                "--nextThoughtNeeded", "true",
                "--branchFromThought", "1",
                "--branchId", "alternative-path",
            ],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=60,
        )
        assert result.returncode == 0


class TestErrorHandling:
    """Test error handling with MCP server."""

    @pytest.mark.skip(reason="Requires MCP server to be running")
    def test_invalid_thought_number(self):
        """Invalid thought number should be handled gracefully."""
        result = subprocess.run(
            [
                "uv", "run", "cli.py", "--format", "json", "sequentialthinking",
                "--thought", "Test",
                "--thoughtNumber", "-1",
                "--totalThoughts", "3",
                "--nextThoughtNeeded", "true",
            ],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            timeout=60,
        )
        # Should either succeed with error in response or fail gracefully
        if result.returncode == 0:
            data = json.loads(result.stdout)
            # Check if error is reported in response
            assert "error" in data or "thoughtNumber" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "integration"])
