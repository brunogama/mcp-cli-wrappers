# Sequential Thinking CLI - Development Guidelines

## Overview

- **Type**: CLI Wrapper (MCP Tool)
- **Stack**: Python 3.10+ with `uv` (PEP 723 script execution)
- **Purpose**: Progressive-disclosure CLI wrapper for Sequential Thinking MCP
- **Architecture**: Single-file Python script with 4-level help system
- **Location**: `~/cli-wrappers/sequential-thinking-cli/`

This CLAUDE.md is the authoritative source for development guidelines.

---

## Universal Development Rules

### Code Quality (MUST)

- **MUST** use PEP 723 headers for uv script execution
- **MUST** return valid JSON from all functions
- **MUST** validate arguments before execution
- **MUST** follow 4-level progressive disclosure pattern
- **MUST NOT** add external CLI dependencies beyond `fastmcp`, `httpx`, `pydantic`, `click`, `rich`
- **MUST NOT** execute shell commands with `subprocess` without validation

### Best Practices (SHOULD)

- **SHOULD** use `rich` library for formatted output
- **SHOULD** provide clear error messages with recovery steps
- **SHOULD** include timeout limits on network requests (30s default)
- **SHOULD** support `--format json|text` output options
- **SHOULD** document all environment variables required
- **SHOULD** include helpful examples in `FUNCTION_EXAMPLES`

### Anti-Patterns (MUST NOT)

- **MUST NOT** store credentials in code (use environment variables)
- **MUST NOT** execute user input directly
- **MUST NOT** suppress errors silently (always log/display)
- **MUST NOT** block on long-running operations (use async when possible)
- **MUST NOT** skip argument validation before MCP calls

---

## 4-Level Progressive Disclosure Pattern

### Level 1: `--help`
```bash
uv run cli.py --help
```
- Quick overview (10-15 lines)
- Available functions listed
- Usage examples
- **Tokens**: ~30

### Level 2: `list` and `info FUNCTION`
```bash
uv run cli.py list
uv run cli.py info sequentialthinking
```
- Full function signature
- All parameters with types
- Return type and format
- **Tokens**: ~150

### Level 3: `example FUNCTION`
```bash
uv run cli.py example sequentialthinking
```
- 2-5 real working examples
- Success and error cases
- Copy-paste ready
- **Tokens**: ~200

### Level 4: `FUNCTION --help`
```bash
uv run cli.py sequentialthinking --help
```
- Complete argparse reference
- All options with detailed explanations
- **Tokens**: ~500

---

## Project Structure

```
sequential-thinking-cli/
├── cli.py              # Main CLI script (PEP 723)
├── .env.example        # Environment template
├── README.md           # User documentation
├── CLAUDE.md           # This file
├── .gitignore          # Git ignore rules
└── tests/
    ├── test_cli.py           # Unit tests
    └── test_integration.py   # Integration tests
```

---

## Core Commands

### Quick Start
```bash
cd ~/cli-wrappers/sequential-thinking-cli/

# Level 1
uv run cli.py --help

# Level 2
uv run cli.py list
uv run cli.py info sequentialthinking

# Level 3
uv run cli.py example sequentialthinking

# Level 4
uv run cli.py sequentialthinking --help
```

### Execute Function
```bash
uv run cli.py sequentialthinking \
  --thought "Your reasoning step" \
  --thoughtNumber 1 \
  --totalThoughts 3 \
  --nextThoughtNeeded true
```

### Live Introspection
```bash
uv run cli.py --discover
```

---

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DEBUG` | No | `false` | Enable debug output |
| `TIMEOUT` | No | `30` | Request timeout in seconds |

---

## Testing

### Run Tests
```bash
pytest tests/
```

### Run with Coverage
```bash
pytest tests/ --cov=. --cov-report=term-missing
```

### Pre-Commit Checks
```bash
# Verify wrapper works
timeout 10 uv run cli.py --help >/dev/null 2>&1 && echo "OK" || echo "FAILED"

# Validate JSON output
uv run cli.py list --format json | jq .
```

---

## Modifying the Wrapper

### Adding a New Function

1. Add entry to `FUNCTION_INFO`:
```python
FUNCTION_INFO = {
    "new_function": {
        "description": "Short description",
        "parameters": [
            {"name": "param1", "type": "string", "required": True, "description": "..."}
        ],
        "returns": "Dict[str, Any]"
    }
}
```

2. Add examples to `FUNCTION_EXAMPLES`:
```python
FUNCTION_EXAMPLES = {
    "new_function": [
        {
            "title": "Basic usage",
            "description": "How to use this function",
            "command": "uv run cli.py new_function --param1 value",
            "output": '{"result": "..."}'
        }
    ]
}
```

3. Update `QUICK_HELP` with new function listing.

### Modifying Parameters

Update the parameter definition in `FUNCTION_INFO`:
```python
{
    "name": "param_name",
    "type": "string|integer|boolean|number",
    "required": True|False,
    "default": None,
    "description": "Parameter description"
}
```

---

## Error Handling

### User-Facing Errors
```python
print(f"Error: {error_message}", file=sys.stderr)
sys.exit(1)
```

### JSON Error Response
```python
format_output({"error": error_message, "details": {...}}, "json")
sys.exit(1)
```

### Verbose Mode
```python
if args.verbose:
    import traceback
    traceback.print_exc()
```

---

## Git Workflow

### Commit Message Format
- `feat:` New function or feature
- `fix:` Bug fix or improvement
- `docs:` Documentation update
- `refactor:` Code reorganization
- `test:` Test additions/changes

### Before Committing
1. Test all levels: `--help`, `list`, `info`, `example`
2. Validate JSON output: `uv run cli.py list --format json | jq .`
3. Run tests: `pytest tests/`
4. Update README.md if needed

---

## Security Guidelines

### Credentials
- NEVER commit API keys or secrets
- Always use environment variables
- Check `.gitignore` includes `.env`

### Input Validation
- Validate all user inputs before MCP calls
- Sanitize inputs that go to shell commands
- Use argument types (string, integer, boolean)

---

## Performance

### Token Efficiency (Goal: 60-70% savings)
- Level 1: ~30 tokens
- Level 2: ~150 tokens
- Level 3: ~200 tokens
- Level 4: ~500 tokens

### Execution Speed
- `--help`: ~100ms (cached strings)
- `list`: ~200ms (function index)
- `info FUNC`: ~300ms (docstring formatting)
- Function call: 30-60s (network dependent)

---

## Troubleshooting

### MCP Connection Issues
```bash
# Check npx is available
which npx

# Test with discover
uv run cli.py --discover --verbose
```

### JSON Validation
```bash
uv run cli.py FUNCTION --format json | jq .
```

### Timeout Issues
```bash
export TIMEOUT=60
uv run cli.py FUNCTION ...
```

---

**This CLAUDE.md is the authoritative source for development guidelines.**
