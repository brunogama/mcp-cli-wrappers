# Technology Stack

**Analysis Date:** 2026-02-01

## Languages

**Primary:**
- Python 3.8+ - Core wrapper implementations (`exa.py`, `ref.py`)
- Python 3.10+ - Auto-generated MCP wrappers (all other `.py` files)

**Secondary:**
- None - Pure Python codebase

## Runtime

**Environment:**
- Python 3.8+ (minimum for `exa.py`, `ref.py`)
- Python 3.10+ (minimum for auto-generated wrappers)

**Package Manager:**
- uv (Astral) - All scripts use PEP 723 inline dependencies
- Lockfile: Not applicable - inline dependency declarations

**Execution Model:**
- Scripts use shebang `#!/usr/bin/env -S uv run`
- Dependencies declared inline via PEP 723 script metadata
- No installation required - uv handles dependency resolution at runtime

## Frameworks

**Core:**
- click 8.1.0+ - CLI framework for feature-rich wrappers (`exa.py`, `ref.py`)
- argparse (stdlib) - CLI framework for auto-generated wrappers

**HTTP/Networking:**
- httpx 0.24.0+ - Async HTTP client (declared in all wrappers)

**Data Validation:**
- pydantic 2.0+ - Data validation and serialization

**Terminal UI:**
- rich 13.0.0+ - Console output formatting, tables, panels, syntax highlighting (`exa.py`, `ref.py`)

**Environment:**
- python-dotenv 1.0.0+ - Environment variable loading (`exa.py`, `ref.py`)

## Key Dependencies

**Critical:**
- `exa-py 1.0.0+` - Exa AI SDK for web search (`exa.py`)
- `click 8.1.0+` - CLI framework for interactive wrappers
- `rich 13.0.0+` - Terminal formatting and display

**Infrastructure:**
- `httpx 0.24.0+` - HTTP client for API communication
- `pydantic 2.0+` - Input validation and data modeling
- `python-dotenv 1.0.0+` - Environment configuration

## Configuration

**Environment:**
- `EXA_API_KEY` - Required for `exa.py` (Exa AI API)
- `REF_API_KEY` - Optional for `ref.py` (defaults to built-in key)
- `REF_ENV` - Environment selector for ref-tools-mcp

**Build:**
- No build step required
- Scripts are executable Python with inline dependencies
- uv resolves and caches dependencies on first run

## Dependency Declaration Pattern

All scripts use PEP 723 inline script metadata:

```python
#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "httpx>=0.24.0",
#     "pydantic>=2.0",
# ]
# ///
```

**Feature-rich wrappers** (`exa.py`, `ref.py`):
```python
# dependencies = [
#     "click>=8.1.0",
#     "httpx>=0.24.0",
#     "pydantic>=2.0.0",
#     "rich>=13.0.0",
#     "python-dotenv>=1.0.0",
#     "exa-py>=1.0.0",  # exa.py only
# ]
```

**Auto-generated wrappers**:
```python
# dependencies = [
#     "httpx>=0.24.0",
#     "pydantic>=2.0",
# ]
```

## Platform Requirements

**Development:**
- macOS, Linux, or Windows with Python 3.8+
- uv package manager installed
- Internet access for dependency resolution

**Production:**
- Same as development
- API keys configured in environment
- External MCP servers accessible (npx, bunx commands)

## External Tool Dependencies

Several wrappers invoke external MCP servers:

| Wrapper | External Dependency |
|---------|---------------------|
| `ref.py` | `npx ref-tools-mcp@latest` |
| `repomix.py` | `npx -y repomix --mcp` |
| `firecrawl.py` | `npx -y firecrawl-mcp` |
| `sequential-thinking.py` | `bunx @modelcontextprotocol/server-sequential-thinking` |
| `github.py` | `bunx @modelcontextprotocol/server-github` |
| `claude-flow.py` | `npx claude-flow@alpha mcp start` |
| `flow-nexus-cli-wrapper.py` | `npx flow-nexus@latest mcp start` |
| `semly.py` | `semly mcp` |
| `crawl4ai.py` | Local: `uv --directory /Users/bruno/Developer/crawl4ai-mcp run main.py` |

**HTTP-based MCP endpoints:**
- `ref.py` (alternative): `https://api.ref.tools/mcp`
- `deepwiki.py`: `https://mcp.deepwiki.com/mcp`

---

*Stack analysis: 2026-02-01*
