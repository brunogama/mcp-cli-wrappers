# Sequential Thinking CLI

CLI wrapper for the Sequential Thinking MCP server with 4-level progressive disclosure.

Sequential Thinking enables multi-step reasoning for complex problems, breaking down analysis into structured thought chains with support for revision and branching.

## Installation

Requires Python 3.10+ and `uv`:

```bash
# Navigate to the project
cd sequential-thinking-cli

# Run directly (uv handles dependencies)
uv run cli.py --help
```

## Quick Start

```bash
# Level 1: Quick overview
uv run cli.py --help

# Level 2: List functions
uv run cli.py list

# Level 2: Function documentation
uv run cli.py info sequentialthinking

# Level 3: Working examples
uv run cli.py example sequentialthinking

# Level 4: Execute function
uv run cli.py sequentialthinking \
  --thought "First step of analysis" \
  --thoughtNumber 1 \
  --totalThoughts 3 \
  --nextThoughtNeeded true
```

## 4-Level Progressive Disclosure

This CLI implements progressive disclosure for token efficiency:

| Level | Command | Tokens | Use Case |
|-------|---------|--------|----------|
| 1 | `--help` | ~30 | Quick overview |
| 2 | `list` / `info FUNC` | ~150 | Detailed docs |
| 3 | `example FUNC` | ~200 | Working examples |
| 4 | `FUNC --help` | ~500 | Full reference |

## Functions

### sequentialthinking

Run sequential thinking process with structured thought chains.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--thought` | string | Yes | Current thought or reasoning step |
| `--thoughtNumber` | integer | Yes | Position in thought sequence (1-indexed) |
| `--totalThoughts` | integer | Yes | Estimated total thoughts needed |
| `--nextThoughtNeeded` | boolean | Yes | Whether another step is required |
| `--isRevision` | boolean | No | Whether this revises a previous thought |
| `--revisesThought` | integer | No | Which thought number this revises |
| `--branchFromThought` | integer | No | Create branch from this thought |
| `--branchId` | string | No | Identifier for current branch |
| `--needsMoreThoughts` | boolean | No | Signal more thoughts needed |

## Usage Examples

### Basic Thought Chain

```bash
# Start reasoning
uv run cli.py sequentialthinking \
  --thought "Let me analyze the authentication flow" \
  --thoughtNumber 1 \
  --totalThoughts 4 \
  --nextThoughtNeeded true

# Continue chain
uv run cli.py sequentialthinking \
  --thought "The token validation uses JWT with RS256" \
  --thoughtNumber 2 \
  --totalThoughts 4 \
  --nextThoughtNeeded true

# Complete chain
uv run cli.py sequentialthinking \
  --thought "Conclusion: vulnerability is in token refresh" \
  --thoughtNumber 4 \
  --totalThoughts 4 \
  --nextThoughtNeeded false
```

### Revising a Thought

```bash
uv run cli.py sequentialthinking \
  --thought "Actually, it uses HS256 not RS256" \
  --thoughtNumber 3 \
  --totalThoughts 4 \
  --nextThoughtNeeded true \
  --isRevision true \
  --revisesThought 2
```

### Creating a Branch

```bash
uv run cli.py sequentialthinking \
  --thought "Alternative: what if issue is in generation?" \
  --thoughtNumber 3 \
  --totalThoughts 4 \
  --nextThoughtNeeded true \
  --branchFromThought 2 \
  --branchId "alt-generation"
```

## Output Formats

```bash
# Human-readable (default)
uv run cli.py sequentialthinking ...

# Machine-readable JSON (--format must come before subcommand)
uv run cli.py --format json sequentialthinking ...
```

## Live Introspection

Discover tools directly from the MCP server:

```bash
uv run cli.py --discover
```

## Configuration

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Available settings:

| Variable | Default | Description |
|----------|---------|-------------|
| `DEBUG` | `false` | Enable debug output |
| `TIMEOUT` | `30` | Request timeout in seconds |

## Development

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=.
```

### Project Structure

```
sequential-thinking-cli/
├── cli.py           # Main CLI (PEP 723 script)
├── .env.example     # Environment template
├── README.md        # This file
├── CLAUDE.md        # Development guidelines
├── .gitignore       # Git ignore rules
└── tests/
    ├── test_cli.py           # Unit tests
    └── test_integration.py   # Integration tests
```

## Troubleshooting

### MCP Server Not Found

Ensure npx is available:

```bash
which npx
npx --version
```

### Connection Timeout

Increase timeout:

```bash
export TIMEOUT=60
uv run cli.py sequentialthinking ...
```

### Verbose Output

Enable for debugging:

```bash
uv run cli.py --verbose sequentialthinking ...
```

## License

MIT
