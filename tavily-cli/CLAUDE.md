# Tavily CLI - Development Guidelines

## Overview

- **Type**: MCP CLI Wrapper
- **Stack**: Python 3.10+ with uv (PEP 723 script execution)
- **Purpose**: Progressive-disclosure CLI wrapper for Tavily MCP server
- **Architecture**: Single-file Python script with fastmcp integration
- **MCP Server**: `npx tavily-mcp@latest` (stdio transport)

---

## Code Quality Rules

### MUST

- Use PEP 723 headers for uv script execution
- Return valid JSON from all MCP tool calls
- Validate arguments before MCP execution
- Check TAVILY_API_KEY exists before MCP calls
- Follow 4-level progressive disclosure pattern
- Handle MCP response formats (data, content, text blocks)

### MUST NOT

- Execute shell commands with subprocess without validation
- Store credentials in code (use environment variables)
- Suppress errors silently
- Skip argument validation before MCP calls

### SHOULD

- Use rich library for formatted output
- Provide clear error messages with recovery steps
- Include timeout limits on network requests (30s default)
- Support --format json|text output options
- Include helpful examples in FUNCTION_EXAMPLES

---

## 4-Level Progressive Disclosure

### Level 1: --help (~30 tokens)
```bash
uv run cli.py --help
```
Quick overview with available functions.

### Level 2: list / info FUNCTION (~150 tokens)
```bash
uv run cli.py list
uv run cli.py info search
```
Full function signature, parameters, returns.

### Level 3: example FUNCTION (~200 tokens)
```bash
uv run cli.py example search
```
Working examples with descriptions.

### Level 4: FUNCTION --help (~500 tokens)
```bash
uv run cli.py search --help
```
Complete argparse reference.

---

## MCP Tool Mapping

| CLI Command | MCP Tool Name |
|-------------|---------------|
| search | tavily-search |
| extract | tavily-extract |
| map | tavily-map |
| crawl | tavily-crawl |

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| TAVILY_API_KEY | Yes | API key from tavily.com |

---

## Testing

```bash
# Syntax check
python -m py_compile cli.py

# Help levels work
uv run cli.py --help
uv run cli.py list
uv run cli.py info search
uv run cli.py example search

# Commands parse correctly
uv run cli.py search --help

# Live introspection (requires API key)
uv run cli.py --discover
```

---

## Commit Message Format

- `feat:` New function or major feature
- `fix:` Bug fix or improvement
- `docs:` Documentation update
- `refactor:` Code reorganization
- `test:` Test additions/changes
