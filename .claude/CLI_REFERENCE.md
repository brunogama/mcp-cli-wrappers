# CLI Wrappers Quick Reference

**MANDATORY**: Before using any tool, ALWAYS run:
```bash
uv run TOOL --help    # Quick overview
uv run TOOL list      # See all functions
```

---

## Web Scraping & Content

### crawl4ai.py
**What**: Fast web scraper with HTML-to-markdown conversion
**When**: Scrape single pages, extract content quickly
**Path**: `~/cli-wrappers/crawl4ai.py`

```bash
uv run crawl4ai.py --help
uv run crawl4ai.py list
uv run crawl4ai.py scrape --url https://example.com
uv run crawl4ai.py crawl --url https://example.com --crawl-depth 2
```

### firecrawl-cli/cli.py
**What**: Advanced scraping with JS rendering, structured extraction
**When**: JS-heavy sites, map URLs, search web, extract structured data
**Path**: `~/cli-wrappers/firecrawl-cli/cli.py`
**Requires**: `FIRECRAWL_API_KEY`

```bash
uv run firecrawl-cli/cli.py --help
uv run firecrawl-cli/cli.py list
uv run firecrawl-cli/cli.py scrape --url https://example.com
uv run firecrawl-cli/cli.py crawl --url https://example.com
uv run firecrawl-cli/cli.py map --url https://example.com
uv run firecrawl-cli/cli.py search --query "topic"
uv run firecrawl-cli/cli.py extract --url URL --prompt "Extract prices"
```

### tavily-cli/cli.py
**What**: AI-powered web search with ranking, extraction, crawling
**When**: Web search with AI answers, extract data, map/crawl sites
**Path**: `~/cli-wrappers/tavily-cli/cli.py`
**Requires**: `TAVILY_API_KEY`

```bash
uv run tavily-cli/cli.py --help
uv run tavily-cli/cli.py list
uv run tavily-cli/cli.py search --query "Python best practices"
uv run tavily-cli/cli.py search --query "ML frameworks" --search-depth advanced --max-results 10
uv run tavily-cli/cli.py extract --urls https://example.com
uv run tavily-cli/cli.py map --url https://docs.example.com
uv run tavily-cli/cli.py crawl --url https://blog.example.com --max-depth 2
```

---

## Documentation & Search

### ref-cli/cli.py
**What**: Search and read official documentation
**When**: Find API docs, framework references, library documentation
**Path**: `~/cli-wrappers/ref-cli/cli.py`
**Requires**: `REF_API_KEY`

```bash
uv run ref-cli/cli.py --help
uv run ref-cli/cli.py list
uv run ref-cli/cli.py search "async patterns python"
uv run ref-cli/cli.py read_url --url "https://docs.python.org/..."
uv run ref-cli/cli.py analyze --path /path/to/code
```

### deepwiki.py
**What**: AI-powered GitHub repo documentation
**When**: Understand repos, ask questions about codebases
**Path**: `~/cli-wrappers/deepwiki.py`

```bash
uv run deepwiki.py --help
uv run deepwiki.py list
uv run deepwiki.py structure --owner facebook --repo react
uv run deepwiki.py contents --owner owner --repo repo
uv run deepwiki.py ask --owner owner --repo repo --question "How does X work?"
```

### gitmcp.py
**What**: Fetch GitHub repo docs (llms.txt, READMEs)
**When**: Get documentation directly from repos, search code
**Path**: `~/cli-wrappers/gitmcp.py`

```bash
uv run gitmcp.py --help
uv run gitmcp.py list
uv run gitmcp.py fetch_generic_documentation --owner anthropics --repo claude-code
uv run gitmcp.py search_generic_documentation --owner owner --repo repo --query "hooks"
uv run gitmcp.py search_generic_code --owner owner --repo repo --query "function"
```

---

## Code Analysis

### semly.py
**What**: Code search, outline generation, explanation
**When**: Analyze code structure, find patterns, understand implementations
**Path**: `~/cli-wrappers/semly.py`

```bash
uv run semly.py --help
uv run semly.py list
uv run semly.py outline /path/to/code
uv run semly.py explain /path/to/file.py
uv run semly.py locate /path --pattern "class.*Handler"
uv run semly.py retrieve /path --query "authentication"
```

### repomix.py
**What**: Pack codebases into single files for AI analysis
**When**: Prepare code for LLM, generate project summaries
**Path**: `~/cli-wrappers/repomix.py`

```bash
uv run repomix.py --help
uv run repomix.py list
uv run repomix.py pack_codebase ~/my-project
uv run repomix.py pack_remote_repository owner/repo
uv run repomix.py generate_skill --output SKILL.md
```

---

## GitHub Operations

### github-cli/cli.py
**What**: Full GitHub API (issues, PRs, files, workflows)
**When**: Automate GitHub, manage issues/PRs, CI/CD operations
**Path**: `~/cli-wrappers/github-cli/cli.py`
**Requires**: `GITHUB_TOKEN`

```bash
uv run github-cli/cli.py --help
uv run github-cli/cli.py list
uv run github-cli/cli.py get-me
uv run github-cli/cli.py list-issues --repo owner/repo
uv run github-cli/cli.py create-issue --repo owner/repo --title "Bug" --body "Description"
uv run github-cli/cli.py create-pull-request --repo owner/repo --title "Feature" --head branch --base main
uv run github-cli/cli.py search-repositories --query "cli tools"
uv run github-cli/cli.py get-file-contents --repo owner/repo --path "README.md"
uv run github-cli/cli.py list-workflow-runs --repo owner/repo
```

---

## Reasoning & Orchestration

### sequential-thinking-cli/cli.py
**What**: Multi-step reasoning for complex problems
**When**: Design decisions, debugging strategies, complex analysis
**Path**: `~/cli-wrappers/sequential-thinking-cli/cli.py`

```bash
uv run sequential-thinking-cli/cli.py --help
uv run sequential-thinking-cli/cli.py list
uv run sequential-thinking-cli/cli.py sequentialthinking --thought "Design a caching strategy for high-traffic API"
```

### claude-flow.py
**What**: Agentic workflow orchestration
**When**: Coordinate multiple agents, complex multi-step tasks
**Path**: `~/cli-wrappers/claude-flow.py`

```bash
uv run claude-flow.py --help
uv run claude-flow.py list
uv run claude-flow.py swarm_init
uv run claude-flow.py agent_spawn
uv run claude-flow.py task_orchestrate
```

### flow-nexus.py
**What**: Cloud orchestration with sandboxed execution
**When**: Run code safely, scale agent swarms
**Path**: `~/cli-wrappers/flow-nexus.py`

```bash
uv run flow-nexus.py --help
uv run flow-nexus.py list
uv run flow-nexus.py sandbox_create
uv run flow-nexus.py sandbox_execute
uv run flow-nexus.py swarm_scale
```

---

## Quick Decision Table

| Need | Tool | Command |
|------|------|---------|
| Scrape webpage (fast) | crawl4ai | `uv run crawl4ai.py scrape --url URL` |
| Scrape JS site | firecrawl-cli | `uv run firecrawl-cli/cli.py scrape --url URL` |
| Map all URLs on site | firecrawl-cli | `uv run firecrawl-cli/cli.py map --url URL` |
| Search the web | firecrawl-cli | `uv run firecrawl-cli/cli.py search --query Q` |
| AI web search + answers | tavily-cli | `uv run tavily-cli/cli.py search --query Q` |
| Search official docs | ref-cli | `uv run ref-cli/cli.py search "query"` |
| Read doc URL | ref-cli | `uv run ref-cli/cli.py read_url --url URL` |
| Understand GitHub repo | deepwiki | `uv run deepwiki.py ask --owner O --repo R --question Q` |
| Get repo documentation | gitmcp | `uv run gitmcp.py fetch_generic_documentation --owner O --repo R` |
| Analyze code structure | semly | `uv run semly.py outline /path` |
| Pack code for AI | repomix | `uv run repomix.py pack_codebase /path` |
| List GitHub issues | github-cli | `uv run github-cli/cli.py list-issues --repo owner/repo` |
| Create GitHub PR | github-cli | `uv run github-cli/cli.py create-pull-request ...` |
| Complex reasoning | sequential-thinking-cli | `uv run sequential-thinking-cli/cli.py sequentialthinking --thought Q` |

---

## Environment Variables

```bash
# Required
export GITHUB_TOKEN="ghp_..."           # github-cli
export FIRECRAWL_API_KEY="fc-..."       # firecrawl-cli
export TAVILY_API_KEY="tvly-..."        # tavily-cli
export REF_API_KEY="ref-..."            # ref-cli

# Optional
export CRAWL4AI_MCP_DIR="~/Developer/crawl4ai-mcp"
export EXA_API_KEY="..."
export SEMLY_API_KEY="..."
```

---

## Universal Commands (All Tools)

```bash
uv run TOOL --help              # Level 1: Quick overview
uv run TOOL list                # Level 2: All functions
uv run TOOL info FUNCTION       # Level 2: Detailed docs
uv run TOOL example FUNCTION    # Level 3: Working examples
uv run TOOL FUNCTION --help     # Level 4: Full reference
uv run TOOL --discover          # Live MCP introspection
```

---

## File Locations

```
~/cli-wrappers/
├── crawl4ai.py                    # Web scraping
├── deepwiki.py                    # GitHub repo docs
├── gitmcp.py                      # GitHub docs via SSE
├── semly.py                       # Code analysis
├── repomix.py                     # Pack codebases
├── claude-flow.py                 # Orchestration
├── flow-nexus.py                  # Cloud execution
├── firecrawl-cli/cli.py           # Advanced scraping
├── tavily-cli/cli.py              # AI web search
├── github-cli/cli.py              # GitHub operations
├── ref-cli/cli.py                 # Doc search
└── sequential-thinking-cli/cli.py # Reasoning
```
