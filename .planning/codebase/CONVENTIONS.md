# Coding Conventions

**Analysis Date:** 2026-02-01

## Naming Patterns

**Files:**
- Use lowercase with hyphens for multi-word names: `flow-nexus-cli-wrapper.py`, `sequential-thinking.py`
- Python files use `.py` extension
- Generator scripts use descriptive names: `generate-all-wrappers.py`

**Functions:**
- Use snake_case for all function names: `show_quick_help()`, `show_function_info()`, `get_client()`
- Use descriptive action-verb prefixes: `show_`, `get_`, `format_`, `generate_`, `check_`
- MCP function names follow snake_case: `pack_codebase`, `search_repositories`, `create_pull_request`

**Variables:**
- Use snake_case for variables: `api_key`, `func_name`, `search_params`
- Use SCREAMING_SNAKE_CASE for module-level constants: `QUICK_HELP`, `FUNCTION_INFO`, `FUNCTION_EXAMPLES`, `MCP_DEFINITIONS`

**Classes:**
- Use PascalCase for class names: `ExaClient`, `RefMCPClient`

**Types:**
- Use standard Python typing conventions: `Dict[str, Any]`, `Optional[str]`, `List[Dict]`

## Code Style

**Formatting:**
- No explicit formatter configured (no .prettierrc, black config, etc.)
- Indentation: 4 spaces (Python standard)
- Maximum line length: ~100 characters observed

**Linting:**
- No linting configuration files detected (.eslintrc, ruff.toml, etc.)
- Code follows PEP 8 conventions implicitly

## Script Headers

**Shebang Pattern:**
- All scripts use uv runner: `#!/usr/bin/env -S uv run`

**PEP 723 Inline Dependencies:**
```python
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "httpx>=0.24.0",
#     "pydantic>=2.0",
# ]
# ///
```

**Docstrings:**
- Triple-quoted module docstrings at top of file
- Include run instructions and level descriptions
- Example from `repomix.py`:
```python
"""
CLI Wrapper for Repomix MCP
Auto-generated wrapper with 4-level progressive disclosure.

Run with: uv run repomix.py [COMMAND] [ARGS]

Levels:
  1. --help              Quick overview
  2. info TOOL          Detailed documentation
  3. example TOOL       Working examples
  4. TOOL --help        Complete reference
"""
```

## Import Organization

**Order:**
1. Standard library imports (`os`, `sys`, `json`, `argparse`, `subprocess`, `asyncio`)
2. Third-party imports (`click`, `rich`, `httpx`, `pydantic`, `dotenv`)
3. Local imports (none observed - flat structure)

**Pattern from `exa.py`:**
```python
import os
import sys
import json
import asyncio
from pathlib import Path
from typing import Any, Optional, Dict, List
import click
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress
from dotenv import load_dotenv
```

**Path Aliases:**
- None used - direct imports only

## Error Handling

**Patterns:**
- Try/except blocks with specific exception types
- Exit with status codes: `sys.exit(1)` for errors, `sys.exit(130)` for keyboard interrupt
- Rich Panel for error display

**Standard error handling block (from `exa.py`):**
```python
try:
    check_api_key()
    cli()
except KeyboardInterrupt:
    console.print("\n[red]Interrupted by user[/red]")
    sys.exit(130)
except Exception as e:
    console.print(Panel(str(e), title="Unexpected Error", style="red"))
    sys.exit(1)
```

**Command-level error handling:**
```python
try:
    client = get_client()
    # ... operation ...
except Exception as e:
    console.print(Panel(str(e), title="Error", style="red"))
    sys.exit(1)
```

## Logging

**Framework:** Rich Console (no traditional logging)

**Patterns:**
- Use `console.print()` for all output
- Use `Panel()` for structured messages with titles
- Use `Table()` for tabular data
- Use `Syntax()` for formatted JSON output
- Use `Progress()` for long-running operations

**Example:**
```python
console = Console()
console.print(Panel("Error message", title="Error", style="red"))
console.print(Panel("Warning", style="yellow", title="Configuration"))
```

## Comments

**When to Comment:**
- Section headers use comment blocks: `# ===== LEVEL 1: QUICK HELP =====`
- Brief inline comments for non-obvious operations
- No excessive commenting observed

**Docstrings:**
- Function docstrings are brief: `"""Level 1: --help"""`
- Class docstrings describe purpose: `"""Client for interacting with Exa AI API."""`

## Function Design

**Size:**
- Functions are small and focused (10-50 lines typical)
- Each function has single responsibility

**Parameters:**
- Use keyword arguments for Click options
- Use `nargs=-1` for variadic arguments
- Use `type=click.Choice()` for constrained values
- Use `is_flag=True` for boolean flags
- Use `multiple=True` for repeatable options

**Return Values:**
- Return `None` for display functions
- Return `Dict[str, Any]` for data functions
- Use `sys.exit()` for error termination

## Module Design

**Two patterns observed:**

**1. Full CLI (Click-based) - `exa.py`, `ref.py`:**
- Rich terminal output
- Click command groups
- Client class pattern
- Environment variable configuration
- Comprehensive help text

**2. Auto-generated wrapper - all other `.py` files:**
- Argparse-based
- Dictionary-based function registration
- Progressive disclosure pattern
- Minimal dependencies

**Exports:**
- No `__all__` declarations
- Scripts are entry points, not libraries

**Barrel Files:**
- Not used - flat file structure

## CLI Architecture

**Progressive Disclosure Pattern:**
```
Level 1: --help              Quick overview
Level 2: info FUNCTION       Detailed documentation
Level 3: example FUNCTION    Working examples
Level 4: FUNCTION --help     Complete reference
```

**Standard subcommands for auto-generated wrappers:**
- `list` - Show all available functions
- `info <function>` - Show function documentation
- `example <function>` - Show usage examples

## Configuration Pattern

**Environment Variables:**
- Load with `python-dotenv`: `load_dotenv()`
- Access with `os.getenv("VAR_NAME", "default")`
- API keys: `EXA_API_KEY`, `REF_API_KEY`

**Key masking for display:**
```python
masked_key = (api_key[:6] + "*" * (len(api_key) - 10) + api_key[-4:]) if len(api_key) > 10 else "***"
```

---

*Convention analysis: 2026-02-01*
