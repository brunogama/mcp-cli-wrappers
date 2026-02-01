# Codebase Structure

**Analysis Date:** 2026-02-01

## Directory Layout

```
/Users/bruno/cli-wrappers/
├── .git/                           # Git repository
├── .planning/                      # Planning documents
│   └── codebase/                   # Architecture documentation
├── README.md                       # Project overview and usage guide
├── INDEX.md                        # Complete index of all CLI tools
├── SUMMARY.txt                     # Project summary
├── generate-all-wrappers.py        # Generator script for auto-generated wrappers
├── crawl4ai.py                     # Auto-generated: Crawl4AI MCP wrapper
├── deepwiki.py                     # Auto-generated: DeepWiki MCP wrapper
├── firecrawl.py                    # Auto-generated: Firecrawl MCP wrapper
├── github.py                       # Auto-generated: GitHub MCP wrapper
├── repomix.py                      # Auto-generated: Repomix MCP wrapper
├── semly.py                        # Auto-generated: Semly MCP wrapper
├── sequential-thinking.py          # Auto-generated: Sequential Thinking MCP wrapper
├── claude-flow.py                  # Auto-generated: Claude Flow MCP wrapper
├── flow-nexus-cli-wrapper.py       # Auto-generated: Flow Nexus MCP wrapper
├── exa.py                          # Hand-crafted: Exa AI search CLI
├── exa-cli.md                      # Documentation for exa.py
├── ref.py                          # Hand-crafted: Ref Tools MCP CLI
└── ref.md                          # Documentation for ref.py
```

## Directory Purposes

### Root Directory (`/Users/bruno/cli-wrappers/`)

**Purpose:** Contains all CLI wrapper scripts and documentation
**Contains:** Python executable scripts, markdown documentation
**Key files:**
- `generate-all-wrappers.py`: Central generator for template-based wrappers
- `*.py`: CLI wrapper scripts (executable)
- `*.md`: Documentation files

### `.planning/codebase/`

**Purpose:** Architecture and codebase analysis documentation
**Contains:** Markdown documents describing system architecture
**Key files:**
- `ARCHITECTURE.md`: Patterns, layers, data flow
- `STRUCTURE.md`: This file

## Key File Locations

### Entry Points

- `generate-all-wrappers.py`: Generates all auto-generated wrappers
- Any `*.py` file: Direct CLI execution via `uv run`

### Documentation

- `README.md`: Main project documentation
- `INDEX.md`: Complete tool index with usage examples
- `SUMMARY.txt`: Quick project summary
- `exa-cli.md`: Exa CLI documentation
- `ref.md`: Ref Tools CLI documentation

### Auto-Generated Wrappers

| File | MCP Service | Functions |
|------|-------------|-----------|
| `crawl4ai.py` | Crawl4AI | scrape, crawl, extract |
| `deepwiki.py` | DeepWiki | read_wiki_structure, read_wiki_contents, ask_question |
| `firecrawl.py` | Firecrawl | scrape, crawl, extract, map, search |
| `github.py` | GitHub | create_pull_request, create_issue, etc. |
| `repomix.py` | Repomix | pack_codebase, pack_remote_repository, etc. |
| `semly.py` | Semly | outline, explain, list_indexed_projects, etc. |
| `sequential-thinking.py` | Sequential Thinking | sequentialthinking |
| `claude-flow.py` | Claude Flow | swarm_init, agent_spawn, task_orchestrate |
| `flow-nexus-cli-wrapper.py` | Flow Nexus | swarm_init, swarm_scale, agent_spawn, etc. |

### Hand-Crafted Wrappers

| File | Service | Lines | Features |
|------|---------|-------|----------|
| `exa.py` | Exa AI | 1064 | Full search API, rich output, multiple commands |
| `ref.py` | Ref Tools MCP | 287 | Subprocess MCP client, JSON/table output |

## Naming Conventions

### Files

**CLI Wrappers:**
- Pattern: `{mcp-name}.py`
- Examples: `crawl4ai.py`, `github.py`, `exa.py`
- Hyphenated names allowed: `sequential-thinking.py`, `claude-flow.py`

**Documentation:**
- Pattern: `{topic}.md` or `{tool}-cli.md`
- Examples: `README.md`, `INDEX.md`, `exa-cli.md`

**Generator:**
- Pattern: Descriptive action name
- Example: `generate-all-wrappers.py`

### Functions/Commands

**Auto-generated wrappers:** snake_case matching MCP function names
- `pack_codebase`, `create_pull_request`, `read_wiki_contents`

**Hand-crafted wrappers:** Verb-based, lowercase
- `search`, `contents`, `similar`, `answer`, `quick`

### Constants

**Pattern:** UPPER_SNAKE_CASE
**Examples:**
- `QUICK_HELP`, `FUNCTION_INFO`, `FUNCTION_EXAMPLES`
- `MCP_DEFINITIONS`, `WRAPPER_TEMPLATE`

### Classes

**Pattern:** PascalCase with descriptive suffix
**Examples:**
- `ExaClient` in `exa.py`
- `RefMCPClient` in `ref.py`

## Where to Add New Code

### New Auto-Generated Wrapper

1. Add MCP definition to `generate-all-wrappers.py`:
   ```python
   MCP_DEFINITIONS = {
       "new-mcp": {
           "command": "npx new-mcp-package",
           "type": "stdio",
           "functions": [
               {"name": "func1", "description": "Description"}
           ]
       }
   }
   ```
2. Run: `uv run generate-all-wrappers.py`
3. New file created: `new-mcp.py`

### New Hand-Crafted Wrapper

1. Create new file: `/Users/bruno/cli-wrappers/{tool-name}.py`
2. Follow the pattern from `exa.py` or `ref.py`
3. Include PEP 723 header with dependencies
4. Use Click for CLI framework
5. Use Rich for output formatting
6. Create companion docs: `{tool-name}.md` or `{tool-name}-cli.md`

### Template for New Hand-Crafted Wrapper

```python
#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "click>=8.1.0",
#     "httpx>=0.24.0",
#     "rich>=13.0.0",
#     "python-dotenv>=1.0.0",
# ]
# ///

import os
import sys
import click
from rich.console import Console
from dotenv import load_dotenv

load_dotenv()
console = Console()

class YourClient:
    def __init__(self):
        self.api_key = os.getenv("YOUR_API_KEY")

@click.group()
@click.version_option()
def cli():
    """Your tool description."""
    pass

@cli.command()
def your_command():
    """Command description."""
    pass

if __name__ == "__main__":
    cli()
```

### New Utility Functions

**Within existing wrapper:**
- Add as module-level function or class method
- No shared utility library exists

**Shared utilities:**
- Currently not supported (monolithic design)
- Each wrapper is self-contained

### New Documentation

**Tool documentation:** `/Users/bruno/cli-wrappers/{tool}.md`
**Planning docs:** `/Users/bruno/cli-wrappers/.planning/codebase/`

## Special Directories

### `.git/`

**Purpose:** Git version control
**Generated:** Yes
**Committed:** N/A (is the VCS)

### `.planning/`

**Purpose:** Project planning and architecture documentation
**Generated:** No (manually created)
**Committed:** Yes

### `.planning/codebase/`

**Purpose:** Codebase analysis documents for GSD tooling
**Generated:** By `gsd:map-codebase` command
**Committed:** Yes

## File Size Distribution

| Category | Files | Lines (approx) |
|----------|-------|----------------|
| Hand-crafted wrappers | 2 | 1,350 |
| Auto-generated wrappers | 9 | 1,530 (170 each) |
| Generator script | 1 | 325 |
| Documentation (md) | 4 | ~1,000 |

## Execution Permissions

All `.py` files are executable (chmod 755):
- Shebang: `#!/usr/bin/env -S uv run`
- Can be run directly: `./exa.py --help`
- Or via uv: `uv run exa.py --help`

---

*Structure analysis: 2026-02-01*
