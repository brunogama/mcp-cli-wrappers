# Testing Patterns

**Analysis Date:** 2026-02-01

## Test Framework

**Runner:**
- Not detected - no test framework configured
- No `pytest.ini`, `conftest.py`, `jest.config.*`, or `vitest.config.*` files present

**Test Files:**
- None detected in the codebase
- No files matching `*.test.*`, `*.spec.*`, `test_*.py`, or `*_test.py` patterns

**Run Commands:**
```bash
# No test commands available
# Tests not implemented
```

## Test File Organization

**Location:**
- No tests directory exists
- No test files co-located with source

**Naming:**
- Not applicable - no tests exist

**Structure:**
```
/Users/bruno/cli-wrappers/
  (no tests directory)
```

## Current Testing Approach

**Manual Testing:**
- Scripts are executed directly with `uv run <script>.py [args]`
- No automated verification

**Configuration checks:**
- `config` command shows current settings: `uv run exa.py config`
- API key validation at runtime: `check_api_key()` function in `exa.py`

## Recommended Test Structure

**For Click-based CLIs (`exa.py`, `ref.py`):**
```python
import pytest
from click.testing import CliRunner
from exa import cli

def test_config_command():
    runner = CliRunner()
    result = runner.invoke(cli, ['config'])
    assert result.exit_code == 0
    assert 'API Key' in result.output
```

**For Argparse-based wrappers:**
```python
import pytest
from firecrawl import main, FUNCTION_INFO

def test_function_info_contains_all_functions():
    assert 'scrape' in FUNCTION_INFO
    assert 'crawl' in FUNCTION_INFO

def test_show_function_info(capsys):
    show_function_info('scrape')
    captured = capsys.readouterr()
    assert 'Scrape webpage' in captured.out
```

## Mocking

**Framework:** Not configured

**Recommended patterns for future testing:**

**Mock external API calls:**
```python
from unittest.mock import patch, MagicMock

@patch('exa.Exa')
def test_search_without_api_call(mock_exa):
    mock_client = MagicMock()
    mock_exa.return_value = mock_client
    mock_client.search.return_value = MagicMock(results=[])

    # Test search functionality
```

**Mock environment variables:**
```python
import os
from unittest.mock import patch

@patch.dict(os.environ, {'EXA_API_KEY': 'test-key'})
def test_client_initialization():
    client = ExaClient()
    assert client.api_key == 'test-key'
```

**What to Mock:**
- External API calls (Exa, ref-tools-mcp)
- Environment variables
- Subprocess calls (for ref.py)
- File system operations

**What NOT to Mock:**
- Argparse argument parsing
- Rich console output formatting
- Dictionary data structures

## Fixtures and Factories

**Test Data:**
- Not implemented

**Recommended fixture pattern:**
```python
@pytest.fixture
def mock_search_response():
    return {
        'results': [
            {'title': 'Test Result', 'url': 'https://example.com', 'score': 0.95}
        ]
    }

@pytest.fixture
def mock_exa_client():
    with patch('exa.ExaClient') as mock:
        yield mock
```

**Location:**
- Fixtures would live in `conftest.py` at project root

## Coverage

**Requirements:** None enforced

**View Coverage:**
```bash
# Not configured
# Recommended setup:
# pip install pytest-cov
# pytest --cov=. --cov-report=html
```

## Test Types

**Unit Tests:**
- Not implemented
- Scope should cover:
  - Individual function behavior (`show_function_info`, `show_quick_help`)
  - Client initialization
  - Response formatting
  - Error handling paths

**Integration Tests:**
- Not implemented
- Scope should cover:
  - CLI command execution
  - Subcommand routing
  - End-to-end wrapper flows

**E2E Tests:**
- Not used
- Would require live API access

## Common Patterns to Implement

**Testing Click commands:**
```python
from click.testing import CliRunner

def test_search_requires_query():
    runner = CliRunner()
    result = runner.invoke(cli, ['search'])
    assert result.exit_code != 0
    assert 'Missing argument' in result.output
```

**Testing argparse commands:**
```python
import sys
from io import StringIO

def test_list_command(monkeypatch, capsys):
    monkeypatch.setattr(sys, 'argv', ['prog', 'list'])
    main()
    captured = capsys.readouterr()
    assert 'Available functions' in captured.out
```

**Error Testing:**
```python
def test_invalid_function_name(capsys):
    show_function_info('nonexistent')
    captured = capsys.readouterr()
    assert 'Unknown function' in captured.out
```

**Environment Variable Testing:**
```python
def test_missing_api_key(monkeypatch):
    monkeypatch.delenv('EXA_API_KEY', raising=False)
    with pytest.raises(ValueError, match='EXA_API_KEY'):
        ExaClient()
```

## Test Gaps Analysis

**Critical untested areas:**
- `exa.py`: All 11 CLI commands (search, contents, similar, answer, etc.)
- `ref.py`: All 7 CLI commands (run, version, info, config, search, check, analyze)
- Auto-generated wrappers: Subcommand routing and display functions
- `generate-all-wrappers.py`: Template generation and file writing

**Risk Assessment:**
- API client initialization paths have no tests
- Error handling logic is untested
- Response formatting correctness unverified
- Command-line argument parsing behavior unvalidated

## Recommended Next Steps

1. **Add pytest configuration:**
   ```toml
   # pyproject.toml
   [tool.pytest.ini_options]
   testpaths = ["tests"]
   python_files = ["test_*.py"]
   ```

2. **Create test directory structure:**
   ```
   tests/
     conftest.py
     test_exa.py
     test_ref.py
     test_wrappers.py
     test_generator.py
   ```

3. **Add test dependencies to scripts:**
   ```python
   # /// script
   # dependencies = [
   #     "pytest>=7.0.0",
   #     "pytest-cov>=4.0.0",
   # ]
   # ///
   ```

---

*Testing analysis: 2026-02-01*
