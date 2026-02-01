# External Integrations

**Analysis Date:** 2026-02-01

## APIs & External Services

**Web Search & Content:**
- Exa AI - AI-powered web search and content retrieval
  - SDK/Client: `exa-py` package
  - Auth: `EXA_API_KEY` environment variable
  - Dashboard: https://exa.ai/dashboard
  - Wrapper: `exa.py`

**Documentation:**
- Ref Tools MCP - Documentation search and analysis
  - SDK/Client: `npx ref-tools-mcp@latest` (CLI subprocess)
  - Auth: `REF_API_KEY` (default: `ref-fb8a5211ed4144376a89`)
  - HTTP endpoint: `https://api.ref.tools/mcp`
  - Wrapper: `ref.py`

- DeepWiki - AI-powered GitHub documentation
  - SDK/Client: HTTP requests
  - Auth: None required (public endpoint)
  - HTTP endpoint: `https://mcp.deepwiki.com/mcp`
  - Wrapper: `deepwiki.py`

**Web Scraping:**
- Firecrawl - Web scraping and data extraction
  - SDK/Client: `npx -y firecrawl-mcp` (CLI subprocess)
  - Auth: Firecrawl API key (via MCP config)
  - Wrapper: `firecrawl.py`

- Crawl4AI - Local web crawling with AI
  - SDK/Client: Local Python server
  - Command: `uv --directory /Users/bruno/Developer/crawl4ai-mcp run main.py`
  - Auth: None (local)
  - Wrapper: `crawl4ai.py`

**Code Analysis:**
- Repomix - Repository packing and analysis
  - SDK/Client: `npx -y repomix --mcp` (CLI subprocess)
  - Auth: None required
  - Wrapper: `repomix.py`

- Semly - Semantic code search
  - SDK/Client: `semly mcp` (CLI subprocess)
  - Auth: Semly API key (via MCP config)
  - Wrapper: `semly.py`

**Version Control:**
- GitHub MCP - GitHub repository operations
  - SDK/Client: `bunx @modelcontextprotocol/server-github` (CLI subprocess)
  - Auth: `GITHUB_TOKEN` (via MCP config)
  - Wrapper: `github.py`

**AI Agent Orchestration:**
- Claude Flow - Agentic workflow orchestration
  - SDK/Client: `npx claude-flow@alpha mcp start` (CLI subprocess)
  - Auth: Anthropic API key (via MCP config)
  - Wrapper: `claude-flow.py`

- Flow Nexus - Advanced cloud orchestration
  - SDK/Client: `npx flow-nexus@latest mcp start` (CLI subprocess)
  - Auth: Platform-specific keys (via MCP config)
  - Wrapper: `flow-nexus-cli-wrapper.py`

**Reasoning:**
- Sequential Thinking MCP - Multi-step reasoning
  - SDK/Client: `bunx @modelcontextprotocol/server-sequential-thinking` (CLI subprocess)
  - Auth: None required
  - Wrapper: `sequential-thinking.py`

## Data Storage

**Databases:**
- None - All wrappers are stateless CLI tools

**File Storage:**
- Local filesystem only
- No persistent state between invocations

**Caching:**
- uv dependency cache (automatic)
- No application-level caching

## Authentication & Identity

**Auth Provider:**
- Environment variable based authentication
  - `EXA_API_KEY` - Exa AI service
  - `REF_API_KEY` - Ref Tools service
  - Additional keys configured via Claude MCP settings

**Implementation:**
```python
# Pattern from exa.py
self.api_key = os.getenv("EXA_API_KEY")
if not self.api_key:
    raise ValueError("EXA_API_KEY environment variable not set")
```

```python
# Pattern from ref.py
self.api_key = os.getenv("REF_API_KEY", "ref-fb8a5211ed4144376a89")
self.env = {**os.environ, "REF_API_KEY": self.api_key}
```

## Monitoring & Observability

**Error Tracking:**
- None - Errors displayed via rich Panel to console
- Exit codes indicate success (0) or failure (1, 130)

**Logs:**
- Console output via `rich.console.Console`
- No file-based logging
- Warning panels for configuration issues

## CI/CD & Deployment

**Hosting:**
- Local execution only
- No deployment target

**CI Pipeline:**
- None detected

## Environment Configuration

**Required env vars:**
- `EXA_API_KEY` - Required for `exa.py`

**Optional env vars:**
- `REF_API_KEY` - For `ref.py` (has default)
- `REF_ENV` - Environment selector for ref-tools
- MCP-specific keys configured via Claude settings

**Secrets location:**
- Shell environment variables
- `.env` file (loaded via python-dotenv)
- Claude MCP configuration file

## MCP Communication Patterns

**Subprocess (stdio):**
Most wrappers communicate with MCP servers via subprocess:
```python
# Pattern from ref.py
cmd = ["npx", "ref-tools-mcp@latest"] + list(args)
result = subprocess.run(
    cmd,
    capture_output=True,
    text=True,
    env=self.env,
    check=False
)
```

**HTTP (SSE):**
Some MCPs use HTTP endpoints:
- `https://api.ref.tools/mcp?apiKey=...`
- `https://mcp.deepwiki.com/mcp`

**Direct SDK:**
`exa.py` uses the official Python SDK:
```python
from exa_py import Exa
self.client = Exa(self.api_key)
response = self.client.search(query_str, **search_params)
```

## Webhooks & Callbacks

**Incoming:**
- None - All wrappers are CLI tools, not servers

**Outgoing:**
- None - Request/response model only

## Integration Summary Table

| Wrapper | MCP Type | Auth Required | External Dependency |
|---------|----------|---------------|---------------------|
| `exa.py` | Direct SDK | Yes (EXA_API_KEY) | exa-py package |
| `ref.py` | stdio/HTTP | Optional | npx ref-tools-mcp |
| `deepwiki.py` | HTTP | No | HTTPS endpoint |
| `firecrawl.py` | stdio | Yes (MCP config) | npx firecrawl-mcp |
| `crawl4ai.py` | stdio | No | Local Python server |
| `repomix.py` | stdio | No | npx repomix |
| `github.py` | stdio | Yes (GITHUB_TOKEN) | bunx server-github |
| `semly.py` | stdio | Yes (MCP config) | semly CLI |
| `claude-flow.py` | stdio | Yes (MCP config) | npx claude-flow |
| `flow-nexus-cli-wrapper.py` | stdio | Yes (MCP config) | npx flow-nexus |
| `sequential-thinking.py` | stdio | No | bunx server-sequential-thinking |

---

*Integration audit: 2026-02-01*
