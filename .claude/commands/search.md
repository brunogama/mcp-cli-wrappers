# /search - Multi-Tool Documentation & Code Search

Search across documentation, code repositories, and web using progressive disclosure.

## Usage

```bash
/search "your query"
/search "your query" --type docs|code|web
/search "your query" --format text|json|table
```

## What This Command Does

1. Accept search query and optional filters
2. Route to appropriate tool (ref/semly/exa)
3. Execute search operation
4. Format and display results

## Available Search Tools

### Ref.py - Documentation Search (Fastest)
```bash
# Quick search
uv run ref.py search "API authentication"

# See all options
uv run ref.py --help

# Get function info
uv run ref.py info search
```

**Best for**: Official documentation, API references, frameworks

### Semly.py - Code Search & Analysis
```bash
# Find code patterns
uv run semly.py outline /path/to/code

# Explain code
uv run semly.py explain /path/to/function.py

# List indexed projects
uv run semly.py list_indexed_projects

# See all options
uv run semly.py --help
```

**Best for**: Code patterns, implementation examples, repository analysis

### Exa.py - Web Search
```bash
# Search the web
uv run exa.py search "machine learning"

# Search by category
uv run exa.py search "startups" --category company

# Get similar pages
uv run exa.py similar https://example.com

# See all options
uv run exa.py --help
```

**Best for**: Current information, research, diverse sources

## Progressive Disclosure Levels

### Level 1: Quick Help
```bash
uv run ref.py --help
uv run semly.py --help
uv run exa.py --help
```

### Level 2: See All Functions
```bash
uv run ref.py list
uv run semly.py list
uv run exa.py list
```

### Level 2: Detailed Function Info
```bash
uv run ref.py info search
uv run semly.py info outline
uv run exa.py info search
```

### Level 3: Working Examples
```bash
uv run ref.py example search
uv run semly.py example outline
uv run exa.py example search
```

### Level 4: Complete Reference
```bash
uv run ref.py search --help
uv run semly.py outline --help
uv run exa.py search --help
```

## Common Search Workflows

### Search Documentation
```bash
# Quick documentation lookup
uv run ref.py search "Python async"

# See available docs
uv run ref.py --help

# Get detailed info
uv run ref.py info search

# View working examples
uv run ref.py example search
```

### Search Code
```bash
# Outline project structure
uv run semly.py outline ~/my-project

# Explain specific code
uv run semly.py explain ~/my-project/src/main.py

# Locate code anchors
uv run semly.py locate ~/my-project --pattern "class.*Handler"

# Retrieve code chunks
uv run semly.py retrieve ~/my-project --query "authentication logic"
```

### Web Search
```bash
# Basic search
uv run exa.py search "machine learning"

# Search by type
uv run exa.py search "Python" --type neural

# Search by category
uv run exa.py search "AI companies" --category company

# Limit results
uv run exa.py search "startups" --num-results 10

# Get similar pages
uv run exa.py similar https://example.com
```

## Output Formats

### JSON (Machine-Readable)
```bash
# Default format
uv run ref.py search "query"
uv run exa.py search "query"

# Pipe to jq for filtering
uv run exa.py search "Python" | jq '.results[] | {title, url}'
```

### Text (Human-Readable)
```bash
uv run ref.py search "query" --format text
uv run semly.py outline ~/project --format text
uv run exa.py search "query" --format text
```

### Table Format
```bash
# For structured display
uv run exa.py search "query" --format table
```

## Combining Multiple Tools

### Search Everything for a Topic
```bash
echo "=== Docs ===" && uv run ref.py search "machine learning"
echo "" && echo "=== Code Examples ===" && uv run semly.py outline ~/ml-projects
echo "" && echo "=== Web ===" && uv run exa.py search "machine learning"
```

### Save Results to File
```bash
# Save documentation search
uv run ref.py search "async" > docs_results.json

# Save code analysis
uv run semly.py outline ~/project --format text > code_outline.txt

# Save web search
uv run exa.py search "AI trends" > web_results.json
```

### Filter and Combine Results
```bash
# Search multiple tools and extract URLs
uv run exa.py search "Python" | jq '.results[] | .url' > urls.txt

# Count results per tool
echo "Docs:" && uv run ref.py search "query" | jq length
echo "Web:" && uv run exa.py search "query" | jq '.results | length'
```

## API Keys Required

### For Ref.py
```bash
export REF_API_KEY="ref-..."
uv run ref.py search "your query"
```

### For Exa
```bash
export EXA_API_KEY="..."
uv run exa.py search "your query"
```

### For Semly
```bash
export SEMLY_API_KEY="..." # If required
uv run semly.py outline /path/to/code
```

## Advanced Search Examples

### Find Python Async Patterns
```bash
# In documentation
uv run ref.py search "async await Python"

# In code
uv run semly.py retrieve ~/project --query "async def"

# On web
uv run exa.py search "Python async patterns" | jq '.results[] | {title, url}'
```

### Research a Technology
```bash
# Documentation/references
uv run ref.py search "Kubernetes"

# Code examples
uv run semly.py outline ~/k8s-projects

# Latest information
uv run exa.py search "Kubernetes 2025" | jq '.results[] | {title, url, score}'
```

### Code Architecture Review
```bash
# Get project structure
uv run semly.py outline ~/project

# Find specific patterns
uv run semly.py locate ~/project --pattern "class.*Service"

# Get detailed analysis
uv run semly.py explain ~/project/src/core.py
```

## Troubleshooting

### No Results Found
```bash
# Try broader search terms
uv run ref.py search "async" # vs "asyncio implementation details"

# Check with web search
uv run exa.py search "your exact phrase"

# Verify API key
echo $REF_API_KEY
echo $EXA_API_KEY
```

### Connection Issues
```bash
# Test connectivity
timeout 5 ping google.com

# Increase timeout
uv run exa.py search "query" --timeout 60

# Check MCP status
claude mcp list
```

### Invalid JSON Output
```bash
# Validate with jq
uv run exa.py search "query" | jq . > /dev/null && echo "Valid JSON"

# View raw output
uv run exa.py search "query" --format text
```

## See Also

- Documentation search: `uv run ref.py --help`
- Code analysis: `uv run semly.py --help`
- Web search: `uv run exa.py --help`
- Deep dive: `/search "your query" --level 4`
