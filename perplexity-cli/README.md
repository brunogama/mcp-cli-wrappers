# Perplexity CLI

Progressive-disclosure CLI wrapper for the Perplexity AI MCP server, providing AI-powered web search, reasoning, and research capabilities through Sonar models.

## Quick Start

```bash
# Set your API key
export PERPLEXITY_API_KEY="your_key_here"

# Ask a question (uses sonar-pro)
uv run cli.py ask "What is the latest news on AI?"

# Deep research (uses sonar-deep-research)
uv run cli.py research "Compare REST vs GraphQL"

# Advanced reasoning (uses sonar-reasoning-pro)
uv run cli.py reason "Should I use microservices or monolith?"

# Direct web search
uv run cli.py search "Python 3.12 new features"
```

## Installation

No installation required. Uses `uv` for dependency management via PEP 723 inline script metadata.

### Requirements

- Python 3.10+
- `uv` package manager
- Perplexity API key from [Perplexity API Portal](https://www.perplexity.ai/account/api/group)

### Setup

```bash
# Clone or navigate to the cli-wrappers directory
cd ~/cli-wrappers/perplexity-cli

# Copy environment template
cp .env.example .env

# Edit .env with your API key
# PERPLEXITY_API_KEY=pplx-...

# Or export directly
export PERPLEXITY_API_KEY="pplx-your-key-here"

# Verify installation
uv run cli.py --help
```

## 4-Level Progressive Disclosure

This CLI implements a 4-level help system for token efficiency:

### Level 1: Quick Overview (~30 tokens)
```bash
uv run cli.py --help
```
Shows main functions, quick examples, and pointers to next level.

### Level 2: Function Details (~150 tokens)
```bash
uv run cli.py list              # All functions
uv run cli.py info ask          # Detailed docs for 'ask'
uv run cli.py info research     # Detailed docs for 'research'
```
Shows parameters, return types, related functions.

### Level 3: Working Examples (~200 tokens)
```bash
uv run cli.py example ask
uv run cli.py example search
```
Shows 2-3 real, copy-paste ready examples.

### Level 4: Full Reference (~500 tokens)
```bash
uv run cli.py ask --help
uv run cli.py search --help
```
Complete argparse reference with all options.

## Available Functions

| Function | Model | Description |
|----------|-------|-------------|
| `ask` | sonar-pro | General-purpose AI with web search |
| `research` | sonar-deep-research | Deep, comprehensive research |
| `reason` | sonar-reasoning-pro | Advanced reasoning & analysis |
| `search` | Search API | Direct web search results |

### ask

General-purpose conversational AI with real-time web search.

```bash
# Basic question
uv run cli.py ask "What is the current weather in New York?"

# With system prompt
uv run cli.py ask "Explain quantum computing" \
    --system "You are a teacher explaining to a 10-year-old"

# With context
uv run cli.py ask "What are the alternatives?" \
    --context "I'm evaluating PostgreSQL for a new project"

# JSON output
uv run cli.py ask "Latest Python version" --format json | jq '.response'
```

### research

Deep, comprehensive research for thorough analysis.

```bash
# Basic research
uv run cli.py research "Compare REST API vs GraphQL for mobile applications"

# Strip thinking tags (saves tokens)
uv run cli.py research "History of machine learning" --strip-thinking

# Save to file
uv run cli.py research "State of AI in healthcare 2025" --format text > research.md
```

### reason

Advanced reasoning for complex analytical tasks.

```bash
# Problem solving
uv run cli.py reason "Should I use microservices or monolith for a startup MVP?"

# Code analysis
uv run cli.py reason "Why might this function be slow?" \
    --context "def fib(n): return fib(n-1) + fib(n-2) if n > 1 else n"

# Decision making
uv run cli.py reason "PostgreSQL vs MongoDB for e-commerce" \
    --system "Consider scalability, development speed, and team expertise"
```

### search

Direct web search returning ranked results.

```bash
# Basic search
uv run cli.py search "Python 3.12 new features"

# Limit results
uv run cli.py search "Claude AI announcements" --max-results 5

# Regional search
uv run cli.py search "local news" --country US

# Table output
uv run cli.py search "MCP servers" --format table
```

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `PERPLEXITY_API_KEY` | Yes | - | Your Perplexity API key |
| `PERPLEXITY_BASE_URL` | No | `https://api.perplexity.ai` | Custom API endpoint |
| `PERPLEXITY_TIMEOUT_MS` | No | `300000` | Request timeout (5 min) |
| `PERPLEXITY_PROXY` | No | - | Proxy URL for corporate networks |

### Proxy Setup

For corporate networks or firewalls:

```bash
# Direct proxy
export PERPLEXITY_PROXY=https://your-proxy-host:8080

# With authentication
export PERPLEXITY_PROXY=https://username:password@your-proxy-host:8080

# Alternative: standard variables
export HTTPS_PROXY=https://your-proxy-host:8080
```

### Timeout Configuration

For long research queries, increase the timeout:

```bash
# Set 10 minute timeout
export PERPLEXITY_TIMEOUT_MS=600000

# Or per-session
PERPLEXITY_TIMEOUT_MS=600000 uv run cli.py research "comprehensive topic"
```

## Output Formats

All commands support `--format` option:

- `text` (default): Human-readable markdown
- `json`: Machine-readable JSON for piping
- `table`: ASCII table (useful for search results)

```bash
# Pipe JSON to jq
uv run cli.py ask "latest news" --format json | jq '.response'

# Table for search
uv run cli.py search "AI tools" --format table

# Save as markdown
uv run cli.py research "topic" --format text > output.md
```

## Troubleshooting

### API Key Issues
```bash
# Verify key is set
echo $PERPLEXITY_API_KEY

# Test with simple query
uv run cli.py ask "hello" --format json
```

### Timeout Errors
```bash
# Increase timeout for research
export PERPLEXITY_TIMEOUT_MS=600000
uv run cli.py research "complex topic"
```

### Proxy Issues
```bash
# Verify proxy connectivity
curl -x $PERPLEXITY_PROXY https://api.perplexity.ai

# Check proxy format includes https://
export PERPLEXITY_PROXY=https://proxy:8080
```

### EOF / Connection Errors
Ensure your network can reach `api.perplexity.ai` and the API key is valid.

## Related MCP Server

This CLI wraps the official Perplexity MCP server: [@perplexity-ai/mcp-server](https://www.npmjs.com/package/@perplexity-ai/mcp-server)

For direct MCP integration with Claude Code:
```bash
claude mcp add perplexity --env PERPLEXITY_API_KEY="your_key" -- npx -y @perplexity-ai/mcp-server
```

## License

MIT
