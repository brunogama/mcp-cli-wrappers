"""Pytest configuration and fixtures."""

import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture(autouse=True)
def mock_fastmcp():
    """Mock fastmcp module for all tests."""
    mock_client = MagicMock()
    mock_transport = MagicMock()
    
    with patch.dict("sys.modules", {
        "fastmcp": MagicMock(),
        "fastmcp.client": MagicMock(),
        "fastmcp.client.transports": MagicMock(),
    }):
        yield mock_client
