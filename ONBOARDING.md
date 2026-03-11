# CLI Wrappers - Developer Onboarding Guide

**Last Updated:** 2026-02-01

---

## 1. Project Overview

### What is CLI Wrappers?

A collection of **15+ self-contained Python CLI tools** that wrap Model Context Protocol (MCP) servers. Each tool provides a token-efficient, progressive-disclosure interface for AI assistants and developers.

### Purpose

- Reduce token usage by 60-70% compared to monolithic help systems
- Provide consistent CLI patterns across different MCP services
- Enable rapid prototyping and testing of MCP integrations

### Key Features

- **4-level progressive disclosure**: Help scales from 30 to 500 tokens as needed
- **PEP 723 execution**: Single-file scripts with inline dependencies via `uv run`
- **No installation required**: Dependencies resolved at runtime
- **Consistent patterns**: All tools follow the same CLI structure

---

## 2. Technology Stack

### Languages

| Language | Version | Usage |
|----------|---------|-------|
| Python | 3.10+ | All CLI wrappers |

### Runtime and Package Management

| Tool | Purpose |
|------|---------|
| `uv` (Astral) | PEP 723 script execution, dependency resolution |
| `python-dotenv` | Environment variable loading |

### Core Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `click` | 8.0+ | CLI framework (feature-rich wrappers) |
| `argparse` | stdlib | CLI framework (auto-generated wrappers) |
| `rich` | 13.0+ | Terminal formatting, tables, panels |
| `httpx` | 0.24.0+ | HTTP client for API calls |
| `pydantic` | 2.0+ | Data validation |
| `fastmcp` | 2.0+ | MCP client library |

### Architecture Pattern

**Monolithic Single-File Scripts** with two categories:

1. **Hand-crafted wrappers**: Click-based, rich output, full API integration
2. **Auto-generated wrappers**: Template-based, argparse, MCP tool calling

---

## 3. Repository Structure

```
cli-wrappers/
+-- CLAUDE.md                    # Project rules and patterns (READ FIRST)
+-- ONBOARDING.md                # This file
+-- QUICKSTART.md                # Minimal setup guide
|
+-- # ROOT-LEVEL WRAPPERS (single-file scripts)
+-- crawl4ai.py                  # Web scraping MCP
+-- deepwiki.py                  # GitHub wiki docs MCP
+-- gitmcp.py                    # GitHub docs via SSE
+-- repomix.py                   # Repository packing MCP
+-- exa.py                       # Neural semantic search and agentic research (v1.1.0)
+-- semly.py                     # Code search MCP
+-- claude-flow.py               # Multi-agent orchestration MCP
+-- flow-nexus.py                # Cloud execution MCP
|
+-- # SUB-PROJECT WRAPPERS (with tests)
+-- brave-search-cli/            # Brave Search integration
|   +-- cli.py
|   +-- CLAUDE.md
|   +-- README.md
|   +-- tests/
+-- firecrawl-cli/               # Advanced web scraping
|   +-- cli.py
|   +-- CLAUDE.md
|   +-- README.md
|   +-- tests/
+-- github-cli/                  # GitHub API operations
|   +-- cli.py
|   +-- CLAUDE.md
|   +-- README.md
|   +-- tests/
+-- perplexity-cli/              # Perplexity AI search
|   +-- cli.py
|   +-- CLAUDE.md
|   +-- README.md
+-- ref-cli/                     # Documentation search
|   +-- cli.py
|   +-- CLAUDE.md
|   +-- README.md
|   +-- tests/
+-- sequential-thinking-cli/     # Multi-step reasoning
|   +-- cli.py
|   +-- CLAUDE.md
|   +-- README.md
|   +-- tests/
+-- tavily-cli/                  # Tavily search
|   +-- cli.py
|   +-- CLAUDE.md
|   +-- README.md
+-- xcode-cli/                   # Xcode build/test control
|   +-- cli.py
|   +-- CLAUDE.md
|   +-- README.md
|   +-- tests/
|
+-- # GENERATOR and TEMPLATES
+-- generate-all-wrappers.py     # Master wrapper generator
+-- templates/
|   +-- wrapper.jinja2           # Jinja2 template for wrappers
+-- run_generator.py             # Generator runner
+-- test-wrapper-new.py          # Wrapper testing utility
+-- test-and-regenerate.sh       # Regeneration script
|
+-- # CONFIGURATION
+-- .claude/                     # Claude Code configuration
|   +-- settings.json            # Hooks configuration
|   +-- QUICK_START.md           # Quick start guide
|   +-- CLI_REFERENCE.md         # Complete CLI reference
|   +-- commands/                # Custom slash commands
|       +-- scrape.md
|       +-- search.md
|       +-- github-pr.md
|       +-- analyze-repo.md
|       +-- think.md
|
+-- .planning/                   # Architecture documentation
    +-- codebase/
        +-- ARCHITECTURE.md
        +-- STACK.md
        +-- CONVENTIONS.md
        +-- STRUCTURE.md
        +-- TESTING.md
        +-- CONCERNS.md
```

### Directory Purposes

| Directory | Purpose |
|-----------|---------|
| Root `*.py` | Single-file executable wrappers |
| `*-cli/` | Sub-project wrappers with tests and docs |
| `templates/` | Jinja2 templates for code generation |
| `.claude/` | Claude Code hooks, commands, and config |
| `.planning/codebase/` | Architecture analysis documents |

---

## 4. Getting Started

### Prerequisites

1. **Python 3.10+**
   ```bash
   python3 --version  # Must be >= 3.10
   ```

2. **uv package manager**
   ```bash
   # Install uv
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Verify installation
   uv --version
   ```

3. **Optional: Node.js and Bun** (for some MCP servers)
   ```bash
   # Node.js for npx commands
   node --version

   # Bun for bunx commands
   curl -fsSL https://bun.sh/install | bash
   ```

4. **API Keys** (varies by tool)
   ```bash
   # GitHub operations
   export GITHUB_TOKEN="ghp_..."

   # Firecrawl web scraping
   export FIRECRAWL_API_KEY="fc-..."

   # Ref documentation search
   export REF_API_KEY="ref-..."

   # Brave Search
   export BRAVE_API_KEY="..."

   # Exa AI neural search and agentic research
   export EXA_API_KEY="..."
   ```

### Environment Setup

```bash
# Clone or navigate to the project
cd ~/cli-wrappers

# Verify a wrapper works
uv run crawl4ai.py --help

# Expected output: Quick help with available functions
```

### Installing Dependencies

**No installation required!** Each script uses PEP 723 inline dependencies:

```python
#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "httpx>=0.24.0",
#     "pydantic>=2.0",
#     "click>=8.0",
#     "rich>=13.0",
# ]
# ///
```

When you run `uv run script.py`, dependencies are automatically resolved and cached.

### Configuration

1. **Create `.env` files** for sub-projects that need them:
   ```bash
   cp ref-cli/.env.example ref-cli/.env
   # Edit .env with your API keys
   ```

2. **Set environment variables**:
   ```bash
   # Add to ~/.bashrc or ~/.zshrc
   export GITHUB_TOKEN="your-token"
   export REF_API_KEY="your-key"
   ```

### Running the Project Locally

```bash
# Run any wrapper
uv run crawl4ai.py --help

# Run sub-project wrapper
uv run ref-cli/cli.py --help

# Execute a function
uv run ref-cli/cli.py search --query "async python"
```

### Running Tests

```bash
# Run tests for a sub-project
cd ref-cli
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

### Building for Production

No build step required. Scripts are directly executable:

```bash
# Direct execution (if chmod +x)
./crawl4ai.py --help

# Via uv (recommended)
uv run crawl4ai.py --help
```

---

## 5. Key Components

### Entry Points

| File | Purpose | Execution |
|------|---------|-----------|
| `*/cli.py` | Main CLI entry point | `uv run cli.py [COMMAND]` |
| `*.py` (root) | Standalone wrapper | `uv run wrapper.py [COMMAND]` |
| `generate-all-wrappers.py` | Template generator | `uv run generate-all-wrappers.py` |

### Core Business Logic

**Progressive Disclosure System** (all wrappers):

```python
QUICK_HELP = """..."""       # Level 1: --help
FUNCTION_INFO = {...}        # Level 2: list, info FUNCTION
FUNCTION_EXAMPLES = {...}    # Level 3: example FUNCTION
# Level 4: FUNCTION --help   # Argparse auto-generated
```

**MCP Tool Calling** (functional wrappers like `crawl4ai.py`):

```python
async def call_mcp_tool(tool_name: str, arguments: Dict[str, Any]):
    async with get_client() as client:
        result = await client.call_tool(tool_name, arguments)
        return result
```

### Configuration Management

- **Environment variables**: `os.environ.get("VAR_NAME", "default")`
- **python-dotenv**: `load_dotenv()` for `.env` file support
- **No config files**: All configuration via environment

### External Services

| Wrapper | External Dependency |
|---------|---------------------|
| `ref-cli` | `https://api.ref.tools` |
| `firecrawl-cli` | `npx -y firecrawl-mcp` |
| `github-cli` | `bunx @modelcontextprotocol/server-github` |
| `sequential-thinking-cli` | `bunx @modelcontextprotocol/server-sequential-thinking` |
| `xcode-cli` | XcodeMCP server (local) |
| `crawl4ai` | Local: `~/Developer/crawl4ai-mcp` |

---

## 6. Development Workflow

### Git Branch Naming

- `feature/new-wrapper` - New wrapper implementation
- `fix/wrapper-name-issue` - Bug fixes
- `docs/update-readme` - Documentation changes
- `refactor/cleanup` - Code reorganization

### Commit Message Format

```
feat: add new wrapper for service X
fix: correct JSON parsing in ref-cli
docs: update CLAUDE.md with new patterns
test: add integration tests for github-cli
refactor: simplify error handling
```

### Starting a New Feature

```bash
# Create feature branch
git checkout -b feature/new-wrapper

# Make changes
# ...

# Test
uv run new-wrapper.py --help
uv run new-wrapper.py list

# Commit
git add .
git commit -m "feat: add new-wrapper for service X"
```

### Testing Requirements

1. **Manual testing**: All 4 help levels must work
   ```bash
   uv run wrapper.py --help
   uv run wrapper.py list
   uv run wrapper.py info FUNCTION
   uv run wrapper.py example FUNCTION
   ```

2. **Unit tests**: For sub-projects with `tests/` directory
   ```bash
   pytest tests/test_cli.py -v
   ```

3. **JSON validation**:
   ```bash
   uv run wrapper.py --format json list | jq .
   ```

### Code Style

- **Formatting**: PEP 8 (4-space indentation)
- **Linting**: ruff (configured in `.claude/settings.json` PostToolUse hook)
- **Type hints**: Required for all function signatures
- **Docstrings**: Triple-quoted, brief descriptions

### PR Process

1. Create feature branch
2. Implement changes
3. Test all 4 help levels
4. Run unit tests if applicable
5. Create PR with description
6. Address review feedback
7. Squash and merge

### CI/CD Pipeline

Currently manual. Hooks in `.claude/settings.json` provide:
- **PreToolUse**: Block dangerous operations (`rm -rf`, force push)
- **PostToolUse**: Auto-lint Python files with ruff

---

## 7. Architecture Decisions

### Design Patterns

| Pattern | Usage |
|---------|-------|
| **Progressive Disclosure** | 4-level help system reduces cognitive load |
| **PEP 723 Scripts** | Self-contained, no installation needed |
| **Template Generation** | Consistent structure across wrappers |
| **Lazy Client Init** | Client created only when needed |

### State Management

- **Stateless**: Each invocation is independent
- **No persistent state**: Configuration via environment only
- **No caching between runs**: Fresh execution each time

### Error Handling

```python
try:
    result = client.method(args)
    format_output(result, format_type)
except Exception as e:
    console.print(f"[red]Error: {e}[/red]", file=sys.stderr)
    sys.exit(1)
```

**Exit Codes:**
- `0`: Success
- `1`: General error
- `130`: Keyboard interrupt (SIGINT)

### Logging

- **No traditional logging**: Uses `rich.Console.print()` for all output
- **Verbose mode**: `--verbose` flag enables tracebacks
- **Format options**: `--format json|text` for output control

### Security Measures

- API keys via environment variables only
- No hardcoded credentials in committed code
- Masked output for sensitive values in `config` commands
- Input validation before API calls

---

## 8. Common Tasks

### Adding a New Auto-Generated Wrapper

1. **Edit `generate-all-wrappers.py`** - Add to MCP_DEFINITIONS:
   ```python
   MCP_DEFINITIONS["new-service"] = {
       "command": "npx @org/new-service-mcp",
       "type": "stdio",  # or "http"
       "functions": [
           {"name": "func1", "description": "Function 1 description"}
       ]
   }
   ```

2. **Run generator**:
   ```bash
   uv run generate-all-wrappers.py
   ```

3. **Test**:
   ```bash
   uv run new-service.py --help
   uv run new-service.py list
   ```

### Adding a New Hand-Crafted Wrapper

1. **Create directory**:
   ```bash
   mkdir new-service-cli
   ```

2. **Create `cli.py`** following ref-cli pattern:
   ```python
   #!/usr/bin/env -S uv run
   # /// script
   # requires-python = ">=3.10"
   # dependencies = [...]
   # ///

   # Include QUICK_HELP, FUNCTION_INFO, FUNCTION_EXAMPLES
   # Implement client class
   # Create CLI with click or argparse
   ```

3. **Create supporting files**:
   ```bash
   cp ref-cli/.env.example new-service-cli/.env.example
   cp ref-cli/CLAUDE.md new-service-cli/CLAUDE.md  # Edit accordingly
   ```

4. **Add tests**:
   ```bash
   mkdir new-service-cli/tests
   touch new-service-cli/tests/__init__.py
   touch new-service-cli/tests/test_cli.py
   ```

### Writing Tests

```python
# tests/test_cli.py
import pytest
from click.testing import CliRunner
from cli import cli  # or main for argparse

def test_help_displays():
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'Available functions' in result.output

def test_list_command():
    runner = CliRunner()
    result = runner.invoke(cli, ['list'])
    assert result.exit_code == 0
```

### Debugging Runtime Errors

1. **Enable verbose mode**:
   ```bash
   uv run cli.py --verbose search --query "test"
   ```

2. **Check environment**:
   ```bash
   uv run cli.py config
   ```

3. **Validate JSON output**:
   ```bash
   uv run cli.py --format json list | jq .
   ```

### Updating Dependencies

Edit the PEP 723 header in the script:

```python
# /// script
# dependencies = [
#     "httpx>=0.25.0",  # Updated version
# ]
# ///
```

Dependencies are resolved fresh on next `uv run`.

---

## 9. Potential Gotchas

### Environment Variables

- **Must be set before running**: Scripts read env vars at startup
- **No `.env` auto-loading in root scripts**: Only sub-projects with `load_dotenv()`
- **Case-sensitive**: `REF_API_KEY` not `ref_api_key`

### External Dependencies

| Issue | Solution |
|-------|----------|
| `npx` not found | Install Node.js and npm |
| `bunx` not found | Install Bun: `curl -fsSL https://bun.sh/install \| bash` |
| MCP server not starting | Check network, verify package exists |

### Known Issues

1. **Some auto-generated wrappers are stubs**: Display help but may lack full MCP implementation
2. **Example commands**: May reference placeholder filenames in some generated wrappers
3. **Empty parameter lists**: Some auto-generated wrappers have undocumented parameters

### Performance Considerations

- **First run is slower**: uv caches dependencies after first execution
- **No connection pooling**: Each invocation spawns fresh processes
- **No retry logic**: Transient failures cause immediate command failure

### Technical Debt

See `.planning/codebase/CONCERNS.md` for full list:
- Some wrappers are stubs with incomplete MCP integration
- No shared utility library (each wrapper is self-contained)
- Test coverage is minimal for root-level wrappers

---

## 10. Documentation and Resources

### Project Documentation

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Universal rules and patterns (authoritative) |
| `ONBOARDING.md` | This comprehensive guide |
| `QUICKSTART.md` | Minimal 5-minute setup |
| `.claude/QUICK_START.md` | Claude Code integration guide |
| `.claude/CLI_REFERENCE.md` | Complete CLI reference |

### Sub-Project Documentation

Each sub-project has:
- `README.md` - User documentation
- `CLAUDE.md` - Development guidelines
- `.env.example` - Environment template

### Architecture Documentation

Located in `.planning/codebase/`:
- `ARCHITECTURE.md` - Patterns, layers, data flow
- `STACK.md` - Technology stack details
- `CONVENTIONS.md` - Coding conventions
- `STRUCTURE.md` - Directory layout
- `TESTING.md` - Testing patterns
- `CONCERNS.md` - Known issues and tech debt

### External Resources

- [uv documentation](https://docs.astral.sh/uv/)
- [Click documentation](https://click.palletsprojects.com/)
- [Rich documentation](https://rich.readthedocs.io/)
- [MCP specification](https://modelcontextprotocol.io/)

---

## 11. Next Steps - Onboarding Checklist

### Day 1: Environment Setup

- [ ] Verify Python 3.10+ installed: `python3 --version`
- [ ] Install uv package manager: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- [ ] Clone/navigate to `~/cli-wrappers`
- [ ] Run `uv run crawl4ai.py --help` to verify setup
- [ ] Read `CLAUDE.md` (20 minutes)

### Day 1: Explore the Codebase

- [ ] Run `uv run ref-cli/cli.py list` - see all functions
- [ ] Run `uv run ref-cli/cli.py info search` - detailed docs
- [ ] Run `uv run ref-cli/cli.py example search` - examples
- [ ] Read `ref-cli/cli.py` to understand the pattern

### Day 2: Make a Test Change

- [ ] Create a branch: `git checkout -b test/my-first-change`
- [ ] Modify help text in a wrapper
- [ ] Test: `uv run wrapper.py --help`
- [ ] Commit: `git commit -m "test: modify help text"`

### Day 2: Run Tests

- [ ] Navigate to a sub-project: `cd ref-cli`
- [ ] Run tests: `pytest tests/ -v`
- [ ] Review test output

### Day 3: Understand Main User Flow

- [ ] Try the 4-level progressive disclosure on 3 different wrappers
- [ ] Test `--format json` output
- [ ] Pipe output to jq: `uv run cli.py --format json list | jq .`

### Day 3: First Contribution

- [ ] Pick a small issue from `.planning/codebase/CONCERNS.md`
- [ ] Create a branch
- [ ] Implement fix
- [ ] Test all 4 help levels
- [ ] Create PR

---

## Summary

CLI Wrappers is a collection of token-efficient MCP CLI tools following consistent patterns. Key points:

1. **No installation**: Use `uv run script.py` directly
2. **4 levels of help**: Scale from 30 to 500 tokens as needed
3. **Self-contained**: Each wrapper is a single file with inline dependencies
4. **Consistent patterns**: All tools follow the same structure
5. **Environment-based config**: API keys and settings via env vars

Start by reading `CLAUDE.md`, then explore a wrapper's 4 help levels, and make a small test change to get comfortable with the workflow.
