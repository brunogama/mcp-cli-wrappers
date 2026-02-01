# Perplexity CLI - Development Guidelines

## Overview

- **Type**: CLI Wrapper for Perplexity MCP Server
- **Stack**: Python 3.10+ with `uv` (PEP 723 script execution)
- **Purpose**: Progressive-disclosure CLI for AI-powered web search and reasoning
- **Location**: `~/cli-wrappers/perplexity-cli/`

## Quick Reference

```bash
# Always start with help
uv run cli.py --help
uv run cli.py list

# Main functions
uv run cli.py ask "query"           # sonar-pro
uv run cli.py research "topic"      # sonar-deep-research
uv run cli.py reason "problem"      # sonar-reasoning-pro
uv run cli.py search "keywords"     # Search API
```

## Architecture

### Single-File Design
The entire CLI is contained in `cli.py` using PEP 723 inline dependencies:
- `click` - CLI framework
- `httpx` - HTTP client
- `rich` - Terminal formatting
- `python-dotenv` - Environment loading

### 4-Level Progressive Disclosure
1. `--help` → Quick overview (~30 tokens)
2. `list` / `info FUNC` → Function details (~150 tokens)
3. `example FUNC` → Working examples (~200 tokens)
4. `FUNC --help` → Full reference (~500 tokens)

### API Client Pattern
```python
class PerplexityClient:
    def chat_completion(messages, model, strip_thinking) -> dict
    def search(query, max_results, ...) -> dict
```

## Code Quality Rules

### MUST
- Return valid JSON from all functions
- Validate API key before requests
- Handle timeout errors gracefully
- Support `--format json|text|table`
- Provide clear error messages with recovery steps

### MUST NOT
- Execute shell commands with `shell=True`
- Store credentials in code
- Suppress errors silently
- Skip argument validation

### SHOULD
- Use `rich` for formatted output
- Include timeout limits (30s default)
- Cache responses when reasonable
- Document environment variables

## Environment Variables

| Variable | Required | Default |
|----------|----------|---------|
| `PERPLEXITY_API_KEY` | Yes | - |
| `PERPLEXITY_BASE_URL` | No | `https://api.perplexity.ai` |
| `PERPLEXITY_TIMEOUT_MS` | No | `300000` |
| `PERPLEXITY_PROXY` | No | - |

## Testing

```bash
# Verify help system
uv run cli.py --help
uv run cli.py list
uv run cli.py info ask
uv run cli.py example ask

# Test with API key
export PERPLEXITY_API_KEY="test"
uv run cli.py ask "test" --format json
```

## Extending

### Adding a New Function
1. Add to `FUNCTION_INFO` dict
2. Add to `FUNCTION_EXAMPLES` dict
3. Create `@cli.command()` function
4. Update `list_functions()` table
5. Test all 4 help levels

### Modifying Output
- JSON format: Use `json.dumps(result, indent=2)`
- Text format: Use `rich.markdown.Markdown()`
- Table format: Use `rich.table.Table()`

## Git Workflow

```bash
# Before committing
uv run cli.py list  # Verify CLI works

# Commit format
git commit -m "feat: add new function"
git commit -m "fix: handle timeout error"
git commit -m "docs: update examples"
```

## Troubleshooting

### Import Errors
```bash
# Dependencies are managed via PEP 723, uv handles them
uv run cli.py --help
```

### API Errors
```bash
# Check key is set
echo $PERPLEXITY_API_KEY

# Test connectivity
curl -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
     https://api.perplexity.ai/chat/completions
```

### Timeout Issues
```bash
# Increase timeout
export PERPLEXITY_TIMEOUT_MS=600000
```
