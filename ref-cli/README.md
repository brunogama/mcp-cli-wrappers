# Ref Tools MCP CLI

A production-ready CLI wrapper for the ref-tools-mcp documentation server with 4-level progressive disclosure help system.

## Features

- Search and read technical documentation
- File validation against ref-tools rules
- Directory/file analysis
- 4-level progressive disclosure help (60-70% token savings)
- Rich terminal output with tables and panels
- JSON/text output formats
- Environment-based configuration

## Quick Start

```bash
# Navigate to project
cd ref-cli

# View quick help (Level 1)
uv run cli.py --help

# List all functions (Level 2)
uv run cli.py list

# Get detailed docs for a function (Level 2)
uv run cli.py info search

# See working examples (Level 3)
uv run cli.py example search

# Execute a function (Level 4)
uv run cli.py search --query "async python"
```

## Installation

### Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) package manager

### Setup

1. Clone or copy the project:
   ```bash
   git clone <repository-url> ref-cli
   cd ref-cli
   ```

2. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your API key
   ```

3. Test installation:
   ```bash
   uv run cli.py --help
   ```

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `REF_API_KEY` | Yes | - | API key for authentication |
| `REF_API_URL` | No | `https://api.ref.tools` | API endpoint |
| `REF_TIMEOUT` | No | `30` | Request timeout in seconds |

### Setting Up

Create a `.env` file in the project root:

```bash
REF_API_KEY=your-api-key-here
```

Or export directly:

```bash
export REF_API_KEY="your-api-key-here"
```

## 4-Level Progressive Disclosure

This CLI implements a token-efficient help system:

### Level 1: Quick Overview (~30 tokens)
```bash
uv run cli.py --help
```
Shows available commands and basic usage.

### Level 2: Function Discovery (~150 tokens)
```bash
uv run cli.py list              # See all functions
uv run cli.py info search       # Detailed docs for 'search'
```

### Level 3: Working Examples (~200 tokens)
```bash
uv run cli.py example search    # Copy-paste ready examples
```

### Level 4: Full Reference (~500 tokens)
```bash
uv run cli.py search --help     # Complete argument reference
```

## Available Functions

| Function | Description |
|----------|-------------|
| `search` | Search documentation by query |
| `read_url` | Read content from documentation URL |
| `check` | Validate file against ref-tools rules |
| `analyze` | Analyze directory or file structure |
| `info` | Show server information |
| `version` | Display version information |
| `config` | Show current configuration |

## Usage Examples

### Search Documentation

```bash
# Basic search
uv run cli.py search --query "async await python"

# Search with limit
uv run cli.py search --query "react hooks" --limit 5

# Search with filter and JSON output
uv run cli.py search --query "type hints" --filter python --format json
```

### Read Documentation URLs

```bash
# Read a documentation page
uv run cli.py read_url --url "https://docs.python.org/3/library/asyncio.html"

# Read with code extraction
uv run cli.py read_url --url "https://example.com/docs" --extract-code

# Read with metadata
uv run cli.py read_url --url "https://example.com/api" --include-metadata --format json
```

### Check Files

```bash
# Check a Python file
uv run cli.py check --filepath src/main.py

# Strict checking mode
uv run cli.py check --filepath README.md --strict
```

### Analyze Directories

```bash
# Analyze current directory
uv run cli.py analyze --path .

# Recursive analysis with filters
uv run cli.py analyze --path ./src --recursive --include "*.py" --exclude "__pycache__"
```

### Configuration and Info

```bash
# Show current configuration (API key masked)
uv run cli.py config

# Show server information
uv run cli.py info_server

# Show version
uv run cli.py version
```

## Output Formats

### Text (Default)
Human-readable output with Rich formatting:
```bash
uv run cli.py search --query "python"
```

### JSON
Machine-readable output:
```bash
uv run cli.py --format json search --query "python"
```

Pipe to jq for filtering:
```bash
uv run cli.py --format json search --query "python" | jq '.results[] | {title, url}'
```

## Testing

### Run Unit Tests
```bash
pytest tests/test_cli.py -v
```

### Run Integration Tests
Requires `REF_API_KEY` to be set:
```bash
REF_API_KEY=your-key pytest tests/test_integration.py -v
```

### Run All Tests
```bash
pytest tests/ -v
```

## Project Structure

```
ref-cli/
├── cli.py                    # Main CLI script (PEP 723)
├── .env.example              # Environment template
├── .env                      # Your configuration (git-ignored)
├── .gitignore                # Git ignore rules
├── README.md                 # This file
├── CLAUDE.md                 # Development guidelines
└── tests/
    ├── test_cli.py           # Unit tests
    └── test_integration.py   # Integration tests
```

## Troubleshooting

### "REF_API_KEY not set"
```bash
export REF_API_KEY="your-api-key"
# or create .env file
```

### "uv: command not found"
Install uv:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### "Connection timeout"
Increase timeout:
```bash
export REF_TIMEOUT=60
uv run cli.py search --query "test"
```

### Invalid JSON output
Use text format for debugging:
```bash
uv run cli.py --format text search --query "test"
```

### Permission denied
Make CLI executable:
```bash
chmod +x cli.py
```

## Development

### Code Quality
- Follow PEP 8 style guide
- Use type hints
- Write docstrings for public functions
- Test before committing

### Adding New Functions
1. Add function info to `FUNCTION_INFO` dict
2. Add examples to `FUNCTION_EXAMPLES` dict
3. Implement execution in `execute_function()`
4. Add subparser in `main()`
5. Write tests

### Commit Messages
- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation updates
- `test:` Test additions/changes
- `refactor:` Code refactoring

## License

Same as parent project.
