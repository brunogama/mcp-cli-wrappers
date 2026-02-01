# Ref CLI - Development Guidelines

## Overview

- **Type**: MCP CLI Wrapper
- **Stack**: Python 3.10+ with uv (PEP 723 script execution)
- **Purpose**: CLI wrapper for ref-tools-mcp documentation server
- **Pattern**: 4-level progressive disclosure

## Universal Development Rules

### Code Quality (MUST)

- **MUST** use PEP 723 headers for uv script execution
- **MUST** return valid JSON from all API functions
- **MUST** validate arguments before API calls
- **MUST** check API key exists before requests
- **MUST** follow 4-level progressive disclosure pattern
- **MUST** use type hints for all function signatures
- **MUST NOT** store credentials in code (use environment variables)
- **MUST NOT** suppress errors silently

### Best Practices (SHOULD)

- **SHOULD** use Rich library for formatted output
- **SHOULD** provide clear error messages with recovery steps
- **SHOULD** include timeout limits (30s default)
- **SHOULD** support `--format json|text` output options
- **SHOULD** mask sensitive data in config output

### Anti-Patterns (MUST NOT)

- **MUST NOT** execute user input directly without validation
- **MUST NOT** use subprocess with shell=True
- **MUST NOT** commit .env files
- **MUST NOT** block on long operations without timeout

## 4-Level Progressive Disclosure Pattern

### Level 1: `--help` (~30 tokens)
```bash
uv run cli.py --help
```
- Quick overview (10-15 lines)
- Available functions listed
- Usage examples

### Level 2: `list` and `info FUNCTION` (~150 tokens)
```bash
uv run cli.py list
uv run cli.py info FUNCTION_NAME
```
- Full function signature
- All parameters with types
- Return type and format

### Level 3: `example FUNCTION` (~200 tokens)
```bash
uv run cli.py example FUNCTION_NAME
```
- 2-3 real working examples
- Copy-paste ready

### Level 4: `FUNCTION --help` (~500 tokens)
```bash
uv run cli.py FUNCTION_NAME --help
```
- Complete argparse reference
- All options with explanations

## Project Structure

```
ref-cli/
├── cli.py              # Main CLI script
├── .env.example        # Environment template
├── .env                # Local config (git-ignored)
├── .gitignore          # Git ignore rules
├── README.md           # User documentation
├── CLAUDE.md           # This file
└── tests/
    ├── test_cli.py           # Unit tests
    └── test_integration.py   # Integration tests
```

## Core Commands

### Quick Test
```bash
uv run cli.py --help
uv run cli.py list
uv run cli.py config
```

### Function Discovery
```bash
uv run cli.py info search
uv run cli.py example search
```

### Execution
```bash
uv run cli.py search --query "async python"
uv run cli.py --format json search --query "test"
```

## Required Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `REF_API_KEY` | Yes | API key for authentication |
| `REF_API_URL` | No | API endpoint (default: https://api.ref.tools) |
| `REF_TIMEOUT` | No | Request timeout in seconds (default: 30) |

## Security Guidelines

### Credentials
- Store API keys in environment variables only
- Mask keys in config output
- Never commit .env files

### Input Validation
- Validate all user inputs
- Sanitize file paths
- Check URL formats

## Testing

### Run Unit Tests
```bash
pytest tests/test_cli.py -v
```

### Run Integration Tests
```bash
REF_API_KEY=your-key pytest tests/test_integration.py -v
```

### Test All Levels
```bash
uv run cli.py --help
uv run cli.py list
uv run cli.py info search
uv run cli.py example search
```

## Adding New Functions

1. Add to `FUNCTION_INFO`:
```python
FUNCTION_INFO["new_function"] = {
    "name": "new_function",
    "description": "Short description",
    "long_description": "Detailed explanation...",
    "parameters": [
        {"name": "param1", "type": "string", "required": True, "description": "..."}
    ],
    "returns": "Return type description",
    "related": ["other_function"]
}
```

2. Add to `FUNCTION_EXAMPLES`:
```python
FUNCTION_EXAMPLES["new_function"] = [
    {
        "title": "Example title",
        "command": "uv run cli.py new_function --param1 value",
        "description": "What this example does"
    }
]
```

3. Add execution logic in `execute_function()`

4. Add subparser in `main()`

5. Write tests in `tests/test_cli.py`

## Git Workflow

### Commit Message Format
- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation updates
- `test:` Test additions
- `refactor:` Code changes

### Before Committing
1. Run tests: `pytest tests/ -v`
2. Test help levels manually
3. Verify JSON output: `uv run cli.py --format json list | jq .`

## Common Patterns

### Error Handling
```python
try:
    result = client.method(args)
    format_output(result, format_type)
except Exception as e:
    if verbose:
        traceback.print_exc()
    console.print(f"[red]Error: {e}[/red]", file=sys.stderr)
    sys.exit(1)
```

### Output Formatting
```python
def format_output(data: Any, format_type: str = "text") -> None:
    if format_type == "json":
        console.print_json(json.dumps(data, indent=2))
    else:
        # Rich table/panel formatting
        ...
```

### Credential Validation
```python
def validate_credentials() -> bool:
    if not REF_API_KEY:
        console.print(Panel("[red]REF_API_KEY not set[/red]", title="Error"))
        return False
    return True
```

## Performance

### Token Efficiency Goal
- Level 1: ~30 tokens (vs 500 for monolithic help)
- Total savings: 60-70%

### Execution Speed
- Help commands: ~100ms (cached)
- Network calls: 30-60s timeout

## Troubleshooting

### Missing API Key
```bash
export REF_API_KEY="your-key"
```

### Timeout Issues
```bash
export REF_TIMEOUT=60
```

### JSON Validation
```bash
uv run cli.py --format json list | jq .
```
