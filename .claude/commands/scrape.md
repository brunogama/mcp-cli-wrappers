# /scrape - Web Scraping Workflow

Quick webpage scraping using progressive disclosure.

## Usage

```bash
/scrape https://example.com
/scrape https://example.com --format text
/scrape --help
```

## What This Command Does

1. Identify best scraper for URL (crawl4ai vs firecrawl vs exa)
2. Execute scrape operation
3. Format output based on user preference
4. Show results with preview

## Interactive Workflow

```bash
# Level 1: Quick overview
uv run crawl4ai.py --help
uv run firecrawl.py --help

# Level 2: See available scrape options
uv run crawl4ai.py info scrape
uv run firecrawl.py info scrape

# Level 3: See working examples
uv run crawl4ai.py example scrape
uv run firecrawl.py example scrape

# Level 4: Full reference with all options
uv run crawl4ai.py scrape --help
uv run firecrawl.py scrape --help
```

## Quick Scraping Examples

### Crawl4AI (Fast, Built-in HTML Parser)
```bash
# Scrape single page
uv run crawl4ai.py scrape https://example.com

# View options
uv run crawl4ai.py info scrape
```

### Firecrawl (Advanced, API-Based)
```bash
# Scrape with advanced options
uv run firecrawl.py scrape https://example.com

# See detailed documentation
uv run firecrawl.py info scrape

# View working examples
uv run firecrawl.py example scrape
```

### Exa (Web Search + Content)
```bash
# Search and scrape
uv run exa.py search "machine learning"

# Get specific page content
uv run exa.py contents https://example.com

# See all options
uv run exa.py --help
```

## Output Formats

### JSON (Default)
```bash
uv run crawl4ai.py scrape https://example.com
```
Returns: Machine-readable JSON with full structure

### Text (Human-Readable)
```bash
uv run crawl4ai.py scrape https://example.com --format text
```
Returns: Formatted text output

### Piped to jq
```bash
# Extract specific data
uv run firecrawl.py scrape https://example.com | jq '.content'

# Pretty-print JSON
uv run crawl4ai.py scrape https://example.com | jq .
```

## Common Workflows

### Save Scraped Content
```bash
# Save to file
uv run crawl4ai.py scrape https://example.com > output.json

# Save as formatted text
uv run firecrawl.py scrape https://example.com --format text > output.txt
```

### Extract Specific Content
```bash
# Get just the text content
uv run crawl4ai.py scrape https://example.com | jq '.text'

# Get all links
uv run firecrawl.py scrape https://example.com | jq '.links'

# Get metadata
uv run crawl4ai.py scrape https://example.com | jq '.metadata'
```

### Batch Scraping
```bash
# Scrape multiple URLs
for url in https://example1.com https://example2.com https://example3.com; do
  echo "Scraping $url..."
  uv run crawl4ai.py scrape "$url" > "output_$(echo $url | sed 's/[^a-zA-Z0-9]/_/g').json"
done
```

## API Keys Required

### For Firecrawl
```bash
export FIRECRAWL_API_KEY="fc-..."
uv run firecrawl.py scrape https://example.com
```

### For Crawl4AI (Optional)
```bash
# Works without API key, but may be limited
export CRAWL4AI_API_KEY="..."
uv run crawl4ai.py scrape https://example.com
```

### For Exa
```bash
export EXA_API_KEY="..."
uv run exa.py search "your query"
```

## Troubleshooting

### Connection Timeout
```bash
# Increase timeout (default 30s)
uv run firecrawl.py scrape https://example.com --timeout 60
```

### Invalid JSON Output
```bash
# Validate with jq
uv run crawl4ai.py scrape https://example.com | jq . > /dev/null && echo "Valid"

# Check raw output
uv run crawl4ai.py scrape https://example.com --format text
```

### Missing API Key
```bash
# Check what's set
env | grep -i api_key

# Export missing key
export FIRECRAWL_API_KEY="fc-..."

# Retry
uv run firecrawl.py scrape https://example.com
```

## See Also

- Level 2: `uv run crawl4ai.py info scrape`
- Level 3: `uv run crawl4ai.py example scrape`
- Level 4: `uv run crawl4ai.py scrape --help`
- Advanced: `uv run firecrawl.py --help`
