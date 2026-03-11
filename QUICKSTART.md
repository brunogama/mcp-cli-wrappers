# CLI Wrappers - Quick Start

**Time to complete: 5 minutes**

---

## Prerequisites

```bash
# Python 3.10+
python3 --version

# Install uv (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## Verify Setup

```bash
cd ~/cli-wrappers
uv run crawl4ai.py --help
```

Expected output: Quick help with available functions.

---

## Core Pattern: 4-Level Help

Every wrapper follows this pattern:

```bash
# Level 1: Quick overview (~30 tokens)
uv run crawl4ai.py --help

# Level 2: All functions / detailed docs (~150 tokens)
uv run crawl4ai.py list
uv run crawl4ai.py info scrape

# Level 3: Working examples (~200 tokens)
uv run crawl4ai.py example scrape

# Level 4: Full reference (~500 tokens)
uv run crawl4ai.py scrape --help
```

---

## Try a Wrapper

### Option A: Documentation Search (ref-cli)

```bash
# Set API key
export REF_API_KEY="your-key"

# Test
uv run ref-cli/cli.py --help
uv run ref-cli/cli.py list
uv run ref-cli/cli.py search --query "async python"
```

### Option B: GitHub Operations (github-cli)

```bash
# Set token
export GITHUB_TOKEN="ghp_your_token"

# Test
uv run github-cli/cli.py --help
uv run github-cli/cli.py list
```

### Option C: Web Scraping (crawl4ai)

```bash
# No API key required (uses local MCP server)
uv run crawl4ai.py --help
uv run crawl4ai.py list
uv run crawl4ai.py info scrape
```

### Option D: Exa Neural Search

```bash
# Requires EXA_API_KEY
export EXA_API_KEY="your-key"

uv run exa.py --help
uv run exa.py list

# Semantic search
uv run exa.py search "async Python examples"

# Agentic research (plans, searches, synthesizes with citations)
uv run exa.py research "What are the tradeoffs between gRPC and REST?"

# Code-specific search
uv run exa.py code-search "FastAPI dependency injection"
```

---

## Output Formats

```bash
# Human-readable (default)
uv run ref-cli/cli.py list

# JSON (for scripting)
uv run ref-cli/cli.py --format json list

# Pipe to jq
uv run ref-cli/cli.py --format json list | jq '.functions[].name'
```

---

## Run Tests

```bash
cd ref-cli
pytest tests/ -v
```

---

## Available Tools

| Tool | Purpose | API Key Required |
|------|---------|------------------|
| `crawl4ai.py` | Web scraping | None (local MCP) |
| `firecrawl-cli/cli.py` | Advanced JS scraping | `FIRECRAWL_API_KEY` |
| `ref-cli/cli.py` | Documentation search | `REF_API_KEY` |
| `github-cli/cli.py` | GitHub operations | `GITHUB_TOKEN` |
| `brave-search-cli/cli.py` | Privacy-focused web search | `BRAVE_API_KEY` |
| `tavily-cli/cli.py` | AI-optimized search | `TAVILY_API_KEY` |
| `perplexity-cli/cli.py` | Perplexity AI search | `PERPLEXITY_API_KEY` |
| `sequential-thinking-cli/cli.py` | Multi-step reasoning | None |
| `xcode-cli/cli.py` | Xcode build/test | None |
| `apple-docset-cli/cli.py` | Apple API documentation | None |
| `deepwiki.py` | GitHub repo Q&A | None |
| `repomix.py` | Pack codebases | None |
| `gitmcp.py` | Fetch repo docs | None |
| `exa.py` | Neural search and agentic research | `EXA_API_KEY` |

---

## Key Files to Read

| File | Purpose | Time |
|------|---------|------|
| `CLAUDE.md` | Project rules | 20 min |
| `ONBOARDING.md` | Full onboarding | 30 min |
| `.claude/QUICK_START.md` | Claude Code integration | 10 min |

---

## Common Issues

### "uv: command not found"
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc  # or ~/.zshrc
```

### "Missing API key"
```bash
export REF_API_KEY="your-key"
# Add to ~/.bashrc for persistence
```

### "npx/bunx not found"
```bash
# Install Node.js for npx
# Install Bun for bunx: curl -fsSL https://bun.sh/install | bash
```

### JSON output validation
```bash
uv run cli.py --format json list | jq .
```

---

## Next Steps

1. Read `CLAUDE.md` for full project rules
2. Explore 3 different wrappers using the 4-level pattern
3. Read `ONBOARDING.md` for comprehensive guide
4. Make a small test change on a branch

---

**You're ready!** Start with `uv run crawl4ai.py --help` and explore from there.
