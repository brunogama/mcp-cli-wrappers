# XcodeMCP CLI - Development Guidelines

## Overview

- **Type**: MCP CLI Wrapper
- **Stack**: Python 3.10+ with `uv` (PEP 723)
- **MCP Server**: [lapfelix/XcodeMCP](https://github.com/lapfelix/XcodeMCP)
- **Functions**: 26 tools across 4 categories

## MANDATORY: Before Using

```bash
cd ~/cli-wrappers/xcode-cli
uv run cli.py --help    # Quick overview
uv run cli.py list      # See all functions
```

## Code Quality Rules

### MUST
- Use PEP 723 headers for uv script execution
- Return valid JSON from all functions
- Validate arguments before MCP calls
- Follow 4-level progressive disclosure pattern
- Handle MCP connection errors gracefully

### MUST NOT
- Execute shell commands with `subprocess` without validation
- Store credentials in code
- Suppress errors silently
- Block on long-running operations without timeout

## 4-Level Progressive Disclosure

### Level 1: `--help` (~30 tokens)
```bash
uv run cli.py --help
```

### Level 2: `list` and `info` (~150 tokens)
```bash
uv run cli.py list
uv run cli.py info xcode_build
```

### Level 3: `example` (~200 tokens)
```bash
uv run cli.py example xcode_test
```

### Level 4: Full reference (~500 tokens)
```bash
uv run cli.py xcode_test --help
```

## Adding New Functions

1. Add to `FUNCTION_INFO` dict with:
   - `description`: Short description
   - `category`: One of Project Management, Build Operations, Configuration, XCResult Analysis
   - `parameters`: Dict with type, required, description
   - `returns`: Expected return format
   - `related`: List of related functions

2. Add to `FUNCTION_EXAMPLES` with 2-3 examples

3. Create click command with proper options

4. Call `call_mcp_tool()` with tool name and arguments

## Testing

```bash
# Test help levels
uv run cli.py --help
uv run cli.py list
uv run cli.py info xcode_build
uv run cli.py example xcode_build

# Test with real project (requires Xcode)
uv run cli.py xcode_get_schemes --xcodeproj /path/to/project.xcodeproj
```

## Error Handling

```python
# Always return structured errors
{
    "success": False,
    "error": "Description of what went wrong",
    "tool": "tool_name"
}
```

## MCP Communication

Uses `claude mcp call` command to invoke XcodeMCP tools:

```python
result = subprocess.run(
    ["claude", "mcp", "call", "xcode-mcp", tool_name, json.dumps(arguments)],
    capture_output=True,
    text=True,
    timeout=300
)
```

## Dependencies

- `click>=8.1.0` - CLI framework
- `rich>=13.0.0` - Terminal formatting
- `httpx>=0.27.0` - HTTP client (for future use)
- `pydantic>=2.0.0` - Data validation

## File Structure

```
xcode-cli/
├── cli.py              # Main CLI script (PEP 723)
├── .env.example        # Environment template
├── README.md           # User documentation
├── CLAUDE.md           # This file
├── tests/
│   ├── test_cli.py
│   └── test_integration.py
└── .gitignore
```

## Commit Message Format

- `feat:` New function or feature
- `fix:` Bug fix
- `docs:` Documentation update
- `refactor:` Code reorganization

## Security

- No API keys required (uses local Xcode)
- Validate all file paths before passing to MCP
- Never execute arbitrary code from MCP responses
