# Firecrawl MCP CLI

Production-ready CLI wrapper for the Firecrawl MCP server with 4-level progressive disclosure for token-efficient help.

## Quick Start

```bash
# Set API key
export FIRECRAWL_API_KEY="fc-your-key"

# Run directly (PEP 723 - no install needed)
uv run cli.py --help

# Scrape a page
uv run cli.py scrape --url "https://example.com"

# Search the web
uv run cli.py search --query "python tutorials" --limit 5
```

## Installation

No installation required. Uses [PEP 723](https://peps.python.org/pep-0723/) inline script metadata.

Requirements:
- Python 3.10+
- [uv](https://github.com/astral-sh/uv) package manager

```bash
# Copy environment template
cp .env.example .env

# Edit with your API key
nano .env
```

## 4-Level Progressive Disclosure

This CLI uses progressive disclosure to minimize token usage while providing complete documentation when needed.

### Level 1: Quick Overview (~30 tokens)

```bash
uv run cli.py --help
```

Output:
```
Firecrawl MCP - Web scraping and content extraction

Scraping:
  scrape         Single URL extraction
  batch          Multi-URL parallel scraping
  ...
```

### Level 2: Function List & Info (~150 tokens)

```bash
# List all functions
uv run cli.py list

# Get detailed info on a function
uv run cli.py info scrape
```

### Level 3: Working Examples (~200 tokens)

```bash
uv run cli.py example scrape
```

Output:
```
Example 1: Basic scrape
  Extract markdown content from a single page
  $ uv run cli.py scrape --url 'https://example.com'

Example 2: Mobile with main content
  Scrape as mobile device, extract main content only
  $ uv run cli.py scrape --url 'https://example.com' --mobile --only-main-content
```

### Level 4: Complete Reference

```bash
uv run cli.py scrape --help
```

## Functions

### Scraping

| Function | Description |
|----------|-------------|
| `scrape` | Extract content from a single URL |
| `batch` | Scrape multiple URLs in parallel |
| `batch-status` | Check batch operation status |

### Crawling

| Function | Description |
|----------|-------------|
| `crawl` | Async crawl of website sections |
| `crawl-status` | Check crawl job progress |

### Discovery

| Function | Description |
|----------|-------------|
| `map` | Discover all indexed URLs on a site |
| `search` | Web search with optional extraction |

### Extraction

| Function | Description |
|----------|-------------|
| `extract` | LLM-powered structured data extraction |

## Usage Examples

### Basic Scraping

```bash
# Single page
uv run cli.py scrape --url "https://example.com"

# With options
uv run cli.py scrape --url "https://example.com" \
  --only-main-content \
  --mobile \
  --format json
```

### Batch Operations

```bash
# Scrape multiple URLs
uv run cli.py batch --urls '["https://a.com", "https://b.com"]'

# Check status
uv run cli.py batch-status --id "batch_abc123"
```

### Website Crawling

```bash
# Crawl blog section
uv run cli.py crawl --url "https://example.com/blog/*" --max-depth 2

# Check progress
uv run cli.py crawl-status --id "crawl_xyz789"
```

### Web Search

```bash
# Basic search
uv run cli.py search --query "machine learning" --limit 10

# With content extraction
uv run cli.py search --query "python async" --scrape --lang en
```

### Structured Extraction

```bash
# With prompt
uv run cli.py extract \
  --urls '["https://example.com/product"]' \
  --prompt "Extract product name, price, description"

# With JSON schema
uv run cli.py extract \
  --urls '["https://example.com/about"]' \
  --schema '{"type": "object", "properties": {"company": {"type": "string"}}}'
```

## Output Formats

```bash
# Human-readable (default)
uv run cli.py scrape --url "https://example.com"

# JSON
uv run cli.py scrape --url "https://example.com" --format json

# JSON with jq filtering
uv run cli.py scrape --url "https://example.com" --format json | jq '.title'
```

## Detail Levels

Control response verbosity for token optimization:

```bash
# Minimal: URL, title only
uv run cli.py scrape --url "https://example.com" --detail minimal

# Standard: + first 500 chars (default)
uv run cli.py scrape --url "https://example.com" --detail standard

# Full: Complete content
uv run cli.py scrape --url "https://example.com" --detail full
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `FIRECRAWL_API_KEY` | Yes | API key from firecrawl.dev |
| `FIRECRAWL_API_URL` | No | Custom API URL (self-hosted) |
| `FIRECRAWL_RETRY_MAX_ATTEMPTS` | No | Max retry attempts (default: 3) |

## Tool Discovery

Discover available tools directly from the MCP server:

```bash
uv run cli.py --discover --format json
```

## Troubleshooting

### API Key Not Set

```
Error: FIRECRAWL_API_KEY environment variable not set
```

Solution:
```bash
export FIRECRAWL_API_KEY="fc-your-key"
```

### Connection Issues

```bash
# Test with verbose output
uv run cli.py scrape --url "https://example.com" --verbose
```

### Invalid JSON Arguments

For array arguments, use proper JSON:
```bash
# Correct
uv run cli.py batch --urls '["https://a.com", "https://b.com"]'

# Also works (comma-separated)
uv run cli.py batch --urls "https://a.com,https://b.com"
```

## Development

```bash
# Run tests
pytest tests/

# Type checking
mypy cli.py

# Linting
ruff check cli.py
```

## License

MIT
