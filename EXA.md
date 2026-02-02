# Exa AI Search CLI Wrapper

Comprehensive CLI wrapper for Exa AI - the first meaning-based web search API powered by embeddings, designed for AI applications.

## Quick Start

```bash
# Set API key
export EXA_API_KEY="your-key-here"

# Level 1: Quick overview
uv run exa.py --help

# Level 2: See all functions
uv run exa.py list

# Level 3: Working examples
uv run exa.py example search

# Execute search
uv run exa.py search "machine learning best practices"
```

## Features

### Search Types

1. **Neural Search** (`search`)
   - Embeddings-based semantic understanding
   - Best for: Natural language queries, concept discovery
   - Search modes: auto, neural, fast

2. **Deep Search** (`deep-search`)
   - Automatic query expansion
   - Comprehensive research coverage
   - Higher cost (~3x), better results

3. **Code Search** (`code-search`)
   - Specialized for programming content
   - Targets: GitHub, Stack Overflow, docs
   - High-accuracy code referencing

4. **Company Research** (`company-research`)
   - Business intelligence gathering
   - News and announcements
   - Financial insights

5. **Find Similar** (`find-similar`)
   - Semantic similarity search
   - Content discovery
   - Competitive analysis

6. **Get Contents** (`get-contents`)
   - Full content extraction
   - Clean text parsing
   - Livecrawl support

## Installation

### Prerequisites

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify installation
uv --version
```

### API Key Setup

Get your API key from [https://exa.ai/](https://exa.ai/)

```bash
# Set environment variable
export EXA_API_KEY="your-key-here"

# Or add to .env file
echo "EXA_API_KEY=your-key-here" >> .env

# Verify
uv run exa.py config
```

## Usage Examples

### Basic Search

```bash
# Simple semantic search
uv run exa.py search "quantum computing applications"

# With result limit
uv run exa.py search "React best practices" --num-results 20

# JSON output for piping
uv run exa.py search "Python async" --format json | jq '.results[].title'
```

### Advanced Search

```bash
# Date-filtered search
uv run exa.py search "AI breakthroughs" \
  --start-published-date 2024-01-01 \
  --num-results 25

# Domain-specific search
uv run exa.py search "Docker tutorials" \
  --include-domains github.com,docker.com \
  --include-text

# Category-filtered search
uv run exa.py search "startup funding" \
  --category company \
  --include-summary

# Exclude domains
uv run exa.py search "machine learning" \
  --exclude-domains medium.com,forbes.com
```

### Deep Search

```bash
# Comprehensive research
uv run exa.py deep-search "blockchain use cases"

# With additional query variations
uv run exa.py deep-search "climate change" \
  --additional-queries "global warming,carbon emissions,renewable energy"

# Include AI summaries
uv run exa.py deep-search "quantum computing" \
  --include-summary \
  --num-results 30
```

### Code Search

```bash
# Find implementation examples
uv run exa.py code-search "async await Python examples"

# GitHub-specific search
uv run exa.py code-search "React hooks patterns" \
  --include-domains github.com \
  --num-results 15

# Multiple documentation sources
uv run exa.py code-search "FastAPI authentication" \
  --include-domains github.com,stackoverflow.com,fastapi.tiangolo.com \
  --include-text
```

### Company Research

```bash
# Company profile and news
uv run exa.py company-research "Anthropic"

# Recent news only
uv run exa.py company-research "OpenAI" \
  --start-date 2024-01-01 \
  --num-results 30

# With AI summaries
uv run exa.py company-research "Tesla" \
  --include-summary \
  --include-news
```

### Find Similar Content

```bash
# Find related articles
uv run exa.py find-similar "https://arxiv.org/abs/2103.03404" \
  --num-results 10

# With full text extraction
uv run exa.py find-similar "https://blog.example.com/post" \
  --include-text \
  --num-results 15
```

### Extract Content

```bash
# Single URL extraction
uv run exa.py get-contents "https://example.com/article"

# Multiple URLs
uv run exa.py get-contents \
  "https://site1.com/page" \
  "https://site2.com/article" \
  --text-verbosity full

# Fresh content with livecrawl
uv run exa.py get-contents "https://news.site.com/latest" \
  --livecrawl \
  --max-characters 5000

# Preserve HTML formatting
uv run exa.py get-contents "https://docs.example.com" \
  --include-html-tags
```

## 4-Level Progressive Disclosure

### Level 1: Quick Help (~30 tokens)

```bash
uv run exa.py --help
```

Shows:
- Available functions
- Quick start commands
- Environment variables
- Basic options

### Level 2: Function Discovery (~150 tokens)

```bash
# List all functions
uv run exa.py list

# Detailed function info
uv run exa.py info search
uv run exa.py info deep-search
uv run exa.py info code-search
```

Shows:
- Function description
- All parameters with types
- Return format
- Related functions

### Level 3: Working Examples (~200 tokens)

```bash
# See copy-paste ready examples
uv run exa.py example search
uv run exa.py example deep-search
uv run exa.py example code-search
```

Shows:
- Real command examples
- Use case descriptions
- Best practices

### Level 4: Complete Reference (~500 tokens)

```bash
# Full argparse documentation
uv run exa.py search --help
uv run exa.py deep-search --help
uv run exa.py code-search --help
```

Shows:
- Complete parameter reference
- All flags and options
- Default values
- Error handling

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `EXA_API_KEY` | Yes | - | API key for authentication |
| `EXA_API_URL` | No | `https://api.exa.ai` | API endpoint |
| `EXA_TIMEOUT` | No | `60` | Request timeout (seconds) |

### Check Configuration

```bash
# View current settings
uv run exa.py config

# View version info
uv run exa.py version
```

## Output Formats

### Text Format (Default)

```bash
uv run exa.py search "Python async"
```

Shows:
- Rich formatted tables
- Syntax-highlighted output
- Progress indicators
- Color-coded results

### JSON Format

```bash
uv run exa.py search "Python async" --format json
```

Returns:
- Valid JSON output
- Pipeable to `jq`, tools
- Machine-readable
- Complete data structure

### Verbose Mode

```bash
uv run exa.py search "Python async" --verbose
```

Shows:
- Full text content
- Complete metadata
- Error tracebacks
- Debug information

## Search Parameters Reference

### Common Parameters

- `--num-results N`: Number of results (1-100, default: 10)
- `--format json|text`: Output format (default: text)
- `--verbose`: Enable verbose output

### Search Filters

- `--type auto|neural|fast`: Search type (default: auto)
- `--category`: Filter by category (company, news, research_paper, etc.)
- `--include-domains`: Comma-separated domains to include (max 1200)
- `--exclude-domains`: Comma-separated domains to exclude (max 1200)

### Date Filters

- `--start-published-date`: Start date (ISO 8601, e.g., 2024-01-01)
- `--end-published-date`: End date (ISO 8601, e.g., 2024-12-31)

### Content Options

- `--include-text`: Include full page text
- `--include-highlights`: Include relevant snippets (default: true)
- `--include-summary`: Include LLM-generated summaries

## Categories

Available category filters:

- `company`: Company information and business intelligence
- `research_paper`: Academic papers and research
- `news`: News articles and press releases
- `tweet`: Twitter/X posts
- `personal_site`: Personal blogs and sites
- `financial_report`: Financial statements and reports
- `people`: Professional profiles

## Pricing

Exa uses pay-per-use pricing:

- **Neural search (1-25 results)**: $0.005
- **Neural search (26-100 results)**: $0.025
- **Deep search (1-25 results)**: $0.015 (~3x regular search)
- **Deep search (26-100 results)**: $0.075
- **Content text**: $0.001 per page
- **Highlights/summaries**: $0.001 per page

## Integration Examples

### Pipe to jq

```bash
# Extract just titles
uv run exa.py search "AI" --format json | jq '.results[].title'

# Get URLs only
uv run exa.py search "ML" --format json | jq -r '.results[].url'

# Complex filtering
uv run exa.py search "Python" --format json | \
  jq '.results[] | select(.publishedDate > "2024-01-01") | {title, url}'
```

### Save Results

```bash
# Save to file
uv run exa.py search "blockchain" --format json > results.json

# Append to file
uv run exa.py search "crypto" --format json >> all_results.json

# Text output to markdown
uv run exa.py search "DevOps" > devops_research.md
```

### Chaining Commands

```bash
# Extract content from search results
uv run exa.py search "React tutorials" --format json | \
  jq -r '.results[].url' | \
  xargs -I {} uv run exa.py get-contents {}

# Research multiple companies
for company in "Anthropic" "OpenAI" "Google"; do
  uv run exa.py company-research "$company" > "${company}_research.txt"
done
```

### Parallel Execution

```bash
# Use GNU parallel for concurrent searches
parallel -j4 "uv run exa.py search '{}' --format json > {}.json" ::: \
  "Python" "JavaScript" "Rust" "Go"
```

## Troubleshooting

### Missing API Key

```bash
# Error: EXA_API_KEY not set
export EXA_API_KEY="your-key-here"

# Verify
echo $EXA_API_KEY
```

### Timeout Issues

```bash
# Increase timeout for slow queries
export EXA_TIMEOUT=120

# Or use flag (future enhancement)
uv run exa.py search "complex query" --timeout 120
```

### Rate Limiting

If you hit rate limits:
1. Reduce `--num-results`
2. Add delays between requests
3. Use `--type fast` for lower latency
4. Upgrade your Exa plan

### Invalid JSON Output

```bash
# Validate JSON
uv run exa.py search "test" --format json | jq . > /dev/null

# Pretty print
uv run exa.py search "test" --format json | jq '.'
```

### HTTP Errors

```bash
# 401 Unauthorized: Check API key
uv run exa.py config

# 429 Too Many Requests: Rate limit hit
# Wait and retry, or reduce request frequency

# 500 Server Error: Try again later
# Use --verbose to see full error
```

## Best Practices

### Optimize Costs

```bash
# Use fast search for simple queries
uv run exa.py search "Python docs" --type fast

# Limit results to what you need
uv run exa.py search "tutorials" --num-results 5

# Avoid deep search unless necessary
# (3x cost of regular search)
```

### Improve Results

```bash
# Use semantic queries, not keywords
# Good: "how to implement authentication in React"
# Bad: "React auth tutorial"

# Use domain filters for focused results
uv run exa.py search "API design" \
  --include-domains github.com,docs.microsoft.com

# Use date filters for recent content
uv run exa.py search "AI news" \
  --start-published-date 2024-01-01
```

### Performance Tips

```bash
# Use --type fast for lower latency
uv run exa.py search "quick query" --type fast

# Batch URL extractions
uv run exa.py get-contents url1 url2 url3

# Use --include-highlights instead of --include-text
# (faster, cheaper, often sufficient)
```

## Advanced Usage

### Custom Query Expansion

```bash
# Manual query variations for comprehensive coverage
uv run exa.py deep-search "cloud computing" \
  --additional-queries "AWS,Azure,Google Cloud,serverless"
```

### Multi-Source Code Search

```bash
# Search across multiple code sources
uv run exa.py code-search "authentication patterns" \
  --include-domains github.com,stackoverflow.com,auth0.com,dev.to \
  --num-results 25 \
  --include-text
```

### Competitive Analysis

```bash
# Research multiple competitors
for company in "Company A" "Company B" "Company C"; do
  uv run exa.py company-research "$company" \
    --start-date 2024-01-01 \
    --include-summary \
    --format json > "${company// /_}_analysis.json"
done
```

### Content Archiving

```bash
# Archive webpage content
uv run exa.py get-contents "https://blog.example.com/important-post" \
  --text-verbosity full \
  --livecrawl \
  > archived_content.txt
```

## API Response Format

### Search Results

```json
{
  "requestId": "unique_identifier",
  "searchType": "neural|deep",
  "results": [
    {
      "id": "document_id",
      "title": "Result title",
      "url": "https://example.com",
      "publishedDate": "2024-01-15T10:30:00Z",
      "author": "Author name",
      "image": "https://example.com/image.jpg",
      "favicon": "https://example.com/favicon.ico",
      "text": "Full page content...",
      "highlights": ["Relevant snippet 1", "Snippet 2"],
      "highlightScores": [0.92, 0.85],
      "summary": "AI-generated summary..."
    }
  ],
  "costDollars": {
    "total": 0.005,
    "breakDown": []
  }
}
```

### Content Extraction

```json
{
  "contents": [
    {
      "url": "https://example.com",
      "title": "Page Title",
      "text": "Extracted clean text...",
      "author": "Author Name",
      "publishedDate": "2024-01-15T10:30:00Z"
    }
  ]
}
```

## Related Tools

- **ref.py**: Documentation search (use for official docs)
- **crawl4ai.py**: Web scraping (use for extraction)
- **firecrawl.py**: Advanced scraping (use for JS-heavy sites)
- **gitmcp.py**: GitHub docs (use for repo documentation)
- **semly.py**: Code analysis (use for codebase exploration)

## Resources

- **Exa AI Website**: https://exa.ai/
- **API Documentation**: https://exa.ai/docs
- **Get API Key**: https://exa.ai/
- **GitHub**: https://github.com/exa-labs
- **MCP Server**: https://github.com/exa-labs/exa-mcp-server

## Support

### Quick Questions

```bash
# "How do I search?"
uv run exa.py example search

# "What parameters are available?"
uv run exa.py info search

# "Is my API key set?"
uv run exa.py config
```

### Detailed Help

- **Getting started**: Run `uv run exa.py --help`
- **Function reference**: Run `uv run exa.py list`
- **API docs**: https://exa.ai/docs
- **This file**: `EXA.md`

## Version

- **Exa CLI**: 1.0.0
- **Created**: 2026-02-01
- **Python**: 3.10+
- **Status**: ✅ Production Ready

---

**Start with**: `uv run exa.py --help` (30 seconds)
**Learn more**: `uv run exa.py list` (2 minutes)
**Try it**: `uv run exa.py search "your query"` (instant)
