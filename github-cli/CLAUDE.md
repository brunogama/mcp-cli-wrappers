# GitHub MCP CLI - Development Guidelines

## Overview

- **Type**: MCP CLI Wrapper
- **Stack**: Python 3.10+ with uv (PEP 723)
- **Pattern**: 4-level progressive disclosure
- **Location**: ~/cli-wrappers/github-cli/

## Code Quality Rules

### MUST
- Use PEP 723 headers for uv script execution
- Return valid JSON from all functions when --format json
- Validate GITHUB_TOKEN before any API calls
- Follow 4-level progressive disclosure pattern
- Use Click for CLI argument parsing
- Use Rich for formatted output

### MUST NOT
- Execute shell commands with subprocess without validation
- Store credentials in code (use environment variables)
- Suppress errors silently (always log/display)
- Add external dependencies beyond httpx, pydantic, click, rich, python-dotenv

## 4-Level Progressive Disclosure

### Level 1: QUICK_HELP (~30 tokens)
- Namespaces overview
- Quick start commands
- Pointer to Level 2

### Level 2: FUNCTION_INFO (~150 tokens)
- Function signature
- All parameters with types
- Related functions

### Level 3: FUNCTION_EXAMPLES (~200 tokens)
- 2-3 real working examples
- Success cases
- Copy-paste ready

### Level 4: Click --help (~500 tokens)
- Auto-generated from decorators
- Complete parameter reference

## Adding New Functions

1. Add to FUNCTION_INFO dict:
```python
"new_function": {
    "namespace": "repo",
    "description": "...",
    "parameters": [...],
    "returns": "...",
    "related": [...],
}
```

2. Add examples to FUNCTION_EXAMPLES:
```python
"new_function": [
    {"title": "Example 1", "command": "uv run cli.py new_function ..."},
]
```

3. Implement Click command:
```python
@cli.command()
@click.option("--param", required=True, help="...")
@click.pass_context
def new_function(ctx, param):
    """Docstring shown in --help."""
    if not validate_credentials():
        sys.exit(1)
    # Implementation
```

## Testing

```bash
# Syntax check
python -m py_compile cli.py

# Help levels work
uv run cli.py --help
uv run cli.py list
uv run cli.py info get_file_contents
uv run cli.py example list_issues

# Commands parse correctly
uv run cli.py get_file_contents --help
```

## Security

- Never commit .env files
- Validate all user input before MCP calls
- Check GITHUB_TOKEN exists before API operations
- Use environment variables for all credentials

## Git Workflow

- Commit messages: `feat: add new_function command`
- Test all 4 levels before committing
- Update README.md with new functions
