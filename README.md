# CLI Wrappers

**Token-efficient CLI wrappers for Model Context Protocol (MCP) servers**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Wrappers](https://img.shields.io/badge/wrappers-15+-green.svg)](#available-tools)
[![Status](https://img.shields.io/badge/status-production-brightgreen.svg)](#)
[![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)](#)

A collection of **15+ self-contained Python CLI tools** that wrap MCP servers with a consistent 4-level progressive disclosure pattern. Reduces token usage by 60-70% compared to monolithic help systems.

---

## Quick Install

```bash
# Install uv (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and test
cd ~/cli-wrappers
uv run crawl4ai.py --help
```

No installation required - dependencies are resolved automatically via PEP 723.

---

## The 4-Level Help Pattern

Every wrapper follows this progressive disclosure pattern:

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

**Token savings**: Start with Level 1 (30 tokens) and only go deeper when needed, vs 500+ tokens for monolithic help.

---

## Available Tools

### Web Scraping and Search

| Tool | Purpose | API Key |
|------|---------|---------|
| `crawl4ai.py` | Fast web scraping | None (local MCP) |
| `firecrawl-cli/cli.py` | Advanced JS scraping, site mapping | `FIRECRAWL_API_KEY` |
| `exa.py` | Neural semantic search, agentic research | `EXA_API_KEY` |
| `brave-search-cli/cli.py` | Brave Search integration | `BRAVE_API_KEY` |
| `tavily-cli/cli.py` | Tavily search | `TAVILY_API_KEY` |
| `perplexity-cli/cli.py` | Perplexity AI search | `PERPLEXITY_API_KEY` |

### Documentation and Code

| Tool | Purpose | API Key |
|------|---------|---------|
| `ref-cli/cli.py` | Technical documentation search | `REF_API_KEY` |
| `deepwiki.py` | GitHub repository Q&A | None |
| `gitmcp.py` | Fetch repo docs (llms.txt, README) | None |
| `repomix.py` | Pack codebases for AI analysis | None |
| `semly.py` | Semantic code search | `SEMLY_API_KEY` |

### GitHub and Development

| Tool | Purpose | API Key |
|------|---------|---------|
| `github-cli/cli.py` | GitHub API operations | `GITHUB_TOKEN` |
| `xcode-cli/cli.py` | Xcode build/test control | None |
| `sequential-thinking-cli/cli.py` | Multi-step reasoning | None |

### Orchestration

| Tool | Purpose | API Key |
|------|---------|---------|
| `claude-flow.py` | Multi-agent orchestration | None |
| `flow-nexus.py` | Sandboxed code execution | None |

---

## Usage Examples

### Search Documentation
```bash
export REF_API_KEY="your-key"
uv run ref-cli/cli.py search --query "async await python"
```

### Neural and Agentic Search
```bash
export EXA_API_KEY="your-key"

# Semantic search using embeddings
uv run exa.py search "machine learning transformers 2025"

# Agentic research: plans, searches, and synthesizes across sources
uv run exa.py research "What are the tradeoffs between SSR and SSG in Next.js?"

# Code-specific search targeting GitHub, Stack Overflow, and docs
uv run exa.py code-search "async await Python examples"

# Extract full content with live crawl
uv run exa.py get-contents "https://example.com/article" --livecrawl
```

### Scrape a Webpage
```bash
uv run crawl4ai.py scrape --url https://example.com
uv run firecrawl-cli/cli.py scrape --url "https://spa-app.com" --only-main-content
```

### GitHub Operations
```bash
export GITHUB_TOKEN="ghp_..."
uv run github-cli/cli.py list_issues --owner org --repo repo
uv run github-cli/cli.py create_pull_request --owner org --repo repo --title "Feature" --head feature --base main
```

### Ask About a Repository
```bash
uv run deepwiki.py ask --owner facebook --repo react --question "How does the reconciler work?"
```

### Pack Codebase for AI
```bash
uv run repomix.py pack_codebase ~/my-project
```

### Multi-Step Reasoning
```bash
uv run sequential-thinking-cli/cli.py sequentialthinking \
  --thought "Step 1 analysis" --thoughtNumber 1 --totalThoughts 5 --nextThoughtNeeded true
```

---

## Output Formats

```bash
# Human-readable (default)
uv run ref-cli/cli.py list

# JSON (for scripting)
uv run ref-cli/cli.py --format json list

# Pipe to jq for filtering
uv run ref-cli/cli.py --format json list | jq '.functions[].name'
```

### Detail Levels (Token Optimization)

```bash
--detail minimal    # Status only (~50 tokens)
--detail standard   # Preview (~150 tokens)
--detail full       # Complete (default)
```

---

## Environment Setup

```bash
# Required API keys (varies by tool)
export GITHUB_TOKEN="ghp_..."
export FIRECRAWL_API_KEY="fc-..."
export REF_API_KEY="ref-..."
export BRAVE_API_KEY="..."
export EXA_API_KEY="..."

# Optional: Add to ~/.bashrc or ~/.zshrc for persistence
```

---

## Project Structure

```
cli-wrappers/
+-- *.py                    # Root-level standalone wrappers
+-- *-cli/                  # Sub-project wrappers with tests
|   +-- cli.py              # Main CLI script
|   +-- CLAUDE.md           # Development guidelines
|   +-- README.md           # User documentation
|   +-- tests/              # Unit tests
+-- generate-all-wrappers.py # Wrapper generator
+-- templates/              # Jinja2 templates
+-- .claude/                # Claude Code configuration
+-- .planning/              # Architecture documentation
```

---

## Running Tests

```bash
# Run tests for a sub-project
cd ref-cli
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

---

## Documentation

| Document | Purpose | Time |
|----------|---------|------|
| [QUICKSTART.md](QUICKSTART.md) | 5-minute setup guide | 5 min |
| [ONBOARDING.md](ONBOARDING.md) | Full developer onboarding | 30 min |
| [CLAUDE.md](CLAUDE.md) | Project rules and patterns | 20 min |
| [.claude/QUICK_START.md](.claude/QUICK_START.md) | Claude Code integration | 10 min |

### Architecture Documentation

Located in `.planning/codebase/`:
- `ARCHITECTURE.md` - Patterns, layers, data flow
- `STACK.md` - Technology stack details
- `CONVENTIONS.md` - Coding conventions
- `TESTING.md` - Testing patterns
- `CONCERNS.md` - Known issues and tech debt

---

## Requirements

- **Python 3.10+**
- **uv** (Astral) - Package manager for PEP 723 scripts
- **Node.js** (optional) - For `npx` MCP servers
- **Bun** (optional) - For `bunx` MCP servers

---

## Contributing

1. Read `CLAUDE.md` for project rules
2. Create a feature branch: `git checkout -b feature/new-wrapper`
3. Implement changes following the 4-level pattern
4. Test all help levels: `--help`, `list`, `info`, `example`
5. Run tests if applicable: `pytest tests/ -v`
6. Create PR with description

See [ONBOARDING.md](ONBOARDING.md) for full developer guide.

---

## Troubleshooting

### "uv: command not found"
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc  # or ~/.zshrc
```

### "Missing API key"
```bash
export REF_API_KEY="your-key"
# Check what's set: env | grep -i api_key
```

### "npx/bunx not found"
```bash
# Node.js: https://nodejs.org/
# Bun: curl -fsSL https://bun.sh/install | bash
```

### Validate JSON output
```bash
uv run cli.py --format json list | jq .
```

---

## Token Efficiency

| Level | Tokens | Use Case |
|-------|--------|----------|
| 1: --help | ~30 | Quick overview |
| 2: list/info | ~150 | Function details |
| 3: example | ~200 | Working examples |
| 4: FUNC --help | ~500 | Full reference |

**Savings**: 60-70% compared to traditional MCP tool calling.

---

## License

MIT

---

## Links

- [uv Documentation](https://docs.astral.sh/uv/)
- [MCP Specification](https://modelcontextprotocol.io/)
- [Click Documentation](https://click.palletsprojects.com/)
- [Rich Documentation](https://rich.readthedocs.io/)

---

**Start here**: `uv run crawl4ai.py --help`
