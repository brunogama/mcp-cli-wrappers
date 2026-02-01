# Tavily CLI

AI-powered web search and extraction via Tavily MCP server.

## Quick Start

```bash
# Set API key
export TAVILY_API_KEY="tvly-..."

# Get help
uv run cli.py --help

# Search the web
uv run cli.py search --query "Python async best practices"
```

## Functions

| Function | Description |
|----------|-------------|
| search | Real-time web search with AI ranking |
| extract | Extract structured data from web pages |
| map | Create structured sitemap of a website |
| crawl | Systematically crawl and explore websites |

## 4-Level Help System

```bash
uv run cli.py --help              # Level 1: Quick overview
uv run cli.py list                # Level 2: All functions
uv run cli.py info FUNCTION       # Level 2: Detailed docs
uv run cli.py example FUNCTION    # Level 3: Working examples
uv run cli.py FUNCTION --help     # Level 4: Full reference
```

## Examples

### Web Search
```bash
# Basic search
uv run cli.py search --query "machine learning frameworks"

# Advanced search with more results
uv run cli.py search --query "API design patterns" --search-depth advanced --max-results 10

# Search with images
uv run cli.py search --query "data visualization" --include-images
```

### Extract Content
```bash
# Single URL
uv run cli.py extract --urls https://example.com/article

# Multiple URLs
uv run cli.py extract --urls "https://site1.com,https://site2.com"
```

### Map Website
```bash
uv run cli.py map --url https://docs.python.org
```

### Crawl Website
```bash
# Basic crawl
uv run cli.py crawl --url https://blog.example.com

# Deep crawl
uv run cli.py crawl --url https://docs.example.com --max-depth 3 --max-pages 20
```

## Output Formats

```bash
# JSON (for piping to jq)
uv run cli.py search --query "test" --format json | jq '.results[] | {title, url}'

# Text (human-readable)
uv run cli.py search --query "test" --format text
```

## Detail Levels

```bash
# Minimal (URLs only)
uv run cli.py search --query "test" --detail minimal

# Standard (500 char preview)
uv run cli.py search --query "test" --detail standard

# Full (complete content)
uv run cli.py search --query "test" --detail full
```

## Environment Setup

```bash
# Get API key at https://tavily.com
export TAVILY_API_KEY="tvly-your-key"
```

## Requirements

- Python 3.10+
- uv package manager
- Tavily API key
