# Brave Search CLI - Development Guidelines

## Overview

- **Type**: CLI Wrapper for Brave Search API
- **Stack**: Python 3.10+ with `uv` (PEP 723)
- **Pattern**: 4-level progressive disclosure
- **Location**: `~/cli-wrappers/brave-search-cli/`

## MANDATORY: Before Using

```bash
uv run cli.py --help    # Level 1: Quick overview
uv run cli.py list      # Level 2: All functions
```

## Architecture

### API Endpoints

| Function | Endpoint |
|----------|----------|
| web_search | `/res/v1/web/search` |
| local_search | `/res/v1/web/search` (with locations filter) |
| video_search | `/res/v1/videos/search` |
| image_search | `/res/v1/images/search` |
| news_search | `/res/v1/news/search` |
| summarizer | `/res/v1/summarizer/search` |

### File Structure

```
brave-search-cli/
├── cli.py              # Main CLI (PEP 723 script)
├── .env.example        # Environment template
├── README.md           # User documentation
├── CLAUDE.md           # Development guidelines (this file)
├── .gitignore          # Git ignore rules
└── tests/
    ├── test_cli.py     # Unit tests
    └── conftest.py     # Test fixtures
```

## Code Quality Rules

### MUST

- Use PEP 723 headers for uv script execution
- Return valid JSON from all search functions
- Validate query length (max 400 chars, 50 words)
- Check API key exists before requests
- Follow 4-level progressive disclosure pattern
- Handle HTTP errors gracefully

### SHOULD

- Use `rich` for formatted output
- Provide `--format json|text|table` options
- Include timeout limits (30s default)
- Cache responses when reasonable

### MUST NOT

- Store API keys in code
- Execute user input directly
- Suppress errors silently
- Make requests without timeout

## 4-Level Help Pattern

```python
# Level 1: QUICK_HELP (~30 tokens)
QUICK_HELP = """
Functions list, basic usage, setup
"""

# Level 2: FUNCTION_INFO (~150 tokens per function)
FUNCTION_INFO = {
    "function_name": {
        "name": "...",
        "description": "...",
        "parameters": {...},
        "returns": "...",
        "related": [...]
    }
}

# Level 3: FUNCTION_EXAMPLES (~200 tokens per function)
FUNCTION_EXAMPLES = {
    "function_name": [
        {"description": "...", "command": "...", "output": "..."}
    ]
}

# Level 4: Click --help (auto-generated)
```

## Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=cli

# Run specific test
pytest tests/test_cli.py::test_web_search
```

## API Reference

### Authentication

All requests require `X-Subscription-Token` header with API key.

### Rate Limits

| Plan | Requests/Month |
|------|----------------|
| Free | 2,000 |
| Basic | 10,000 |
| Pro | Unlimited |

### Common Parameters

| Parameter | Type | Default | Constraints |
|-----------|------|---------|-------------|
| query | str | required | max 400 chars, 50 words |
| country | str | "US" | ISO country code |
| count | int | 10 | 1-20 |
| offset | int | 0 | 0-9 |
| safesearch | str | "moderate" | off, moderate, strict |
| freshness | str | null | pd, pw, pm, py |

## Adding New Features

1. Add function to `cli.py`
2. Update `FUNCTION_INFO` dictionary
3. Add examples to `FUNCTION_EXAMPLES`
4. Create Click command with proper options
5. Add alias if appropriate
6. Write tests
7. Update README.md

## Git Workflow

```bash
# Before committing
uv run cli.py list  # Verify wrapper works
pytest tests/       # Run tests

# Commit format
git commit -m "feat: add new search parameter"
git commit -m "fix: handle empty results"
git commit -m "docs: update API examples"
```

## Debugging

```bash
# Verbose output
DEBUG=true uv run cli.py web_search "test"

# Check API key
echo $BRAVE_API_KEY

# Test API directly
curl -H "X-Subscription-Token: $BRAVE_API_KEY" \
     "https://api.search.brave.com/res/v1/web/search?q=test"
```

## Security

- Never commit `.env` files
- Use environment variables for credentials
- Validate all user input
- Sanitize output for display

## Links

- [Brave Search API Docs](https://api.search.brave.com/app/documentation)
- [MCP Server Source](https://github.com/brave/brave-search-mcp-server)
- [Parent Project](~/cli-wrappers/CLAUDE.md)
