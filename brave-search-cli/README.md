# Brave Search CLI

A token-efficient CLI wrapper for the Brave Search API with 4-level progressive disclosure help system.

## Features

- **Web Search**: Comprehensive web search with rich results
- **Local Search**: Find local businesses and places (Pro plan)
- **Video Search**: Search for videos with metadata
- **Image Search**: Find images with filtering options
- **News Search**: Search current news articles
- **Summarizer**: AI-generated summaries (Pro AI subscription)

## Installation

```bash
# Clone or copy to your preferred location
cd ~/cli-wrappers/brave-search-cli

# Set up environment
cp .env.example .env
# Edit .env with your API key

# Test installation
uv run cli.py --help
```

## Setup

1. Get your API key at [Brave Search API](https://brave.com/search/api/)
2. Export the environment variable:
   ```bash
   export BRAVE_API_KEY="your_api_key_here"
   ```

## 4-Level Help System

This CLI uses progressive disclosure to minimize token usage:

### Level 1: Quick Overview
```bash
uv run cli.py --help
```
Shows main functions and basic usage (~30 tokens)

### Level 2: Function List & Details
```bash
uv run cli.py list                    # All functions
uv run cli.py info web_search         # Detailed docs
```
Shows all parameters and return types (~150 tokens)

### Level 3: Working Examples
```bash
uv run cli.py example web_search
```
Real, copy-paste ready examples (~200 tokens)

### Level 4: Complete Reference
```bash
uv run cli.py web_search --help
```
Full argparse documentation (~500 tokens)

## Quick Start

```bash
# Basic web search
uv run cli.py web_search "python tutorials"

# Search with options
uv run cli.py web_search "AI news" --count 5 --freshness pw

# Image search
uv run cli.py image_search "mountain landscape" --safesearch strict

# News search (last 24 hours)
uv run cli.py news_search "technology" --freshness pd

# Local business search
uv run cli.py local_search "coffee shops near me"

# Video search
uv run cli.py video_search "machine learning tutorial"
```

## Commands

| Command | Alias | Description |
|---------|-------|-------------|
| `web_search` | `search` | Comprehensive web search |
| `local_search` | `local` | Local businesses and places |
| `video_search` | `videos` | Video search with metadata |
| `image_search` | `images` | Image search |
| `news_search` | `news` | News articles |
| `summarizer` | `summary` | AI summaries (Pro) |

## Common Options

| Option | Short | Description |
|--------|-------|-------------|
| `--country` | `-c` | Country code (US, GB, DE, etc.) |
| `--count` | `-n` | Number of results (1-20) |
| `--safesearch` | `-s` | Content filter (off, moderate, strict) |
| `--freshness` | `-f` | Time filter (pd=day, pw=week, pm=month, py=year) |
| `--format` | | Output format (json, text, table) |

## Output Formats

```bash
# JSON (default, for piping)
uv run cli.py web_search "query" --format json

# Text (human readable)
uv run cli.py web_search "query" --format text

# Table (compact view)
uv run cli.py web_search "query" --format table
```

## API Subscription Tiers

| Feature | Free | Basic | Pro |
|---------|------|-------|-----|
| Web Search | Yes | Yes | Yes |
| Image Search | Yes | Yes | Yes |
| Video Search | Yes | Yes | Yes |
| News Search | Yes | Yes | Yes |
| Local Search | Limited | Yes | Yes |
| Summarizer | No | No | Yes |

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `BRAVE_API_KEY` | Yes | Brave Search API key |

## Troubleshooting

### API Key Not Set
```
Error: BRAVE_API_KEY environment variable not set.
```
Solution: Export your API key:
```bash
export BRAVE_API_KEY="your_key_here"
```

### Rate Limiting
If you receive rate limit errors, wait a few seconds between requests or upgrade your API plan.

### No Results
- Check query spelling
- Try broader search terms
- Verify country code is valid

## Development

```bash
# Run tests
pytest tests/

# Format code
ruff format cli.py

# Type check
mypy cli.py
```

## License

MIT License

## Links

- [Brave Search API](https://brave.com/search/api/)
- [API Documentation](https://api.search.brave.com/app/documentation/web-search)
- [MCP Server](https://github.com/brave/brave-search-mcp-server)
