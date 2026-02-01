# Claude Code Quick Start Guide

Everything you need to get started with CLI Wrappers in Claude Code.

---

## 1. Understand the Project (2 minutes)

**What**: 12 self-contained Python CLI tools wrapping Model Context Protocol (MCP) servers.

**Why**: Progressive-disclosure help system saves 60-70% tokens vs traditional help.

**Location**: `~/cli-wrappers/`

**Key Features**:
- 4-level help system (quick → detailed → examples → full reference)
- All tools work with `uv run`
- No external dependencies beyond `httpx`, `pydantic`, `click`, `rich`

---

## 2. Explore Available Tools (5 minutes)

### Quick Overview
```bash
cd ~/cli-wrappers

# See all available tools
ls *.py

# Get help on any tool
uv run TOOL_NAME.py --help
```

### The 12 Tools

| Tool | Purpose | Command |
|------|---------|---------|
| **crawl4ai.py** | Web scraping | `uv run crawl4ai.py scrape https://example.com` |
| **firecrawl.py** | Advanced scraping | `uv run firecrawl.py scrape https://example.com` |
| **ref.py** | Docs search | `uv run ref.py search "query"` |
| **github.py** | GitHub ops | `uv run github.py list_issues --repo owner/repo` |
| **exa.py** | Web search | `uv run exa.py search "machine learning"` |
| **semly.py** | Code search | `uv run semly.py outline /path/to/code` |
| **repomix.py** | Repo analysis | `uv run repomix.py pack_codebase ~/project` |
| **deepwiki.py** | GitHub docs | `uv run deepwiki.py read_wiki_contents` |
| **sequential-thinking.py** | Complex reasoning | `uv run sequential-thinking.py sequentialthinking "question"` |
| **claude-flow.py** | Orchestration | `uv run claude-flow.py swarm_init` |
| **flow-nexus-cli-wrapper.py** | Cloud setup | `uv run flow-nexus-cli-wrapper.py swarm_init` |
| **generate-all-wrappers.py** | Generator | `uv run generate-all-wrappers.py` |

---

## 3. Learn the 4-Level Help System (10 minutes)

Every tool has 4 levels of help. Using GitHub as example:

### Level 1: Quick Overview (30 tokens)
```bash
uv run github.py --help
```
Output: Quick function list, basic usage, pointer to next level.

### Level 2: Detailed Docs (150 tokens)
```bash
uv run github.py list            # See all functions
uv run github.py info create_pull_request  # Get detailed docs
```
Output: Full signature, all parameters, return types, examples.

### Level 3: Working Examples (200 tokens)
```bash
uv run github.py example create_pull_request
```
Output: 2-3 real working examples you can copy-paste.

### Level 4: Complete Reference (500 tokens)
```bash
uv run github.py create_pull_request --help
```
Output: Full argparse reference, all options, error cases.

**Why this matters**: You can go from 30 tokens (just help) to 500 tokens (everything). Save 70% tokens by exploring progressively.

---

## 4. Set Up Your First Tool (10 minutes)

### Example: GitHub Operations

#### Step 1: Get Your Token
```bash
# Go to: https://github.com/settings/tokens/new
# Create token with: repo, issues, pull_requests scopes
# Copy the token
```

#### Step 2: Set Environment Variable
```bash
export GITHUB_TOKEN="ghp_your_token_here"

# Verify it works
uv run github.py list_issues --repo anthropic/anthropic-sdk-python
```

#### Step 3: Try Common Operations
```bash
# List issues
uv run github.py list_issues --repo owner/repo

# Get file content
uv run github.py get_file_contents --repo owner/repo --path "README.md"

# See all options
uv run github.py --help
```

---

## 5. Explore the Documentation (5 minutes)

### Key Files

| File | Purpose |
|------|---------|
| **CLAUDE.md** | Universal rules & patterns |
| **README.md** | Project overview |
| **INDEX.md** | Complete tool index |
| **.claude/MCP_SETUP.md** | MCP configuration guide |
| **.claude/QUICK_START.md** | This file |
| **.claude/commands/*.md** | Workflow guides |

### Start Reading
```bash
# Understand the project
cat CLAUDE.md

# See all tools
cat INDEX.md

# Learn MCP setup
cat .claude/MCP_SETUP.md

# Read workflow guides
cat .claude/commands/scrape.md
cat .claude/commands/search.md
cat .claude/commands/github-pr.md
```

---

## 6. Use in Claude Code (5 minutes)

### Option A: Use from Terminal
```bash
cd ~/cli-wrappers

# Run any tool
uv run github.py list_issues --repo owner/repo

# Pipe results
uv run exa.py search "Python" | jq '.results[] | {title, url}'

# Save to file
uv run repomix.py pack_codebase ~/my-project > project.txt
```

### Option B: Use Custom Slash Commands
```bash
# Available after setup:
/scrape https://example.com
/search "your query"
/github-pr --repo owner/repo --title "Feature"
/analyze-repo ~/my-project
/think "complex question"
```

### Option C: Use in Conversations
Mention what you want:
- "Scrape https://example.com for me"
- "Search the docs for 'async patterns'"
- "Create a GitHub PR for this change"
- "Analyze this repository structure"
- "Help me think through this architecture"

---

## 7. Common Workflows (20 minutes)

### Scrape a Website
```bash
# Level 1: Quick help
uv run crawl4ai.py --help

# Level 2: Detailed docs
uv run crawl4ai.py info scrape

# Level 3: See examples
uv run crawl4ai.py example scrape

# Level 4: Full reference
uv run crawl4ai.py scrape --help

# Actually scrape
uv run crawl4ai.py scrape https://example.com
```

### Search Documentation
```bash
# Find something in docs
uv run ref.py search "async patterns"

# See the help
uv run ref.py --help
uv run ref.py list
uv run ref.py info search
```

### Analyze a Repository
```bash
# Pack local repository
uv run repomix.py pack_codebase ~/my-project > analysis.txt

# Pack GitHub repository
uv run repomix.py pack_remote_repository owner/repo > github_analysis.txt

# Generate skill documentation
uv run repomix.py generate_skill ~/my-project > SKILL.md
```

### Create GitHub PR
```bash
# See workflow
cat .claude/commands/github-pr.md

# Push files
uv run github.py push_files --repo owner/repo --branch feature/x --files "src/main.py"

# Create PR
uv run github.py create_pull_request --repo owner/repo --title "Feature X" --head feature/x --base main
```

### Solve Complex Problem
```bash
# Use extended thinking
uv run sequential-thinking.py sequentialthinking "Your complex question"

# Example
uv run sequential-thinking.py sequentialthinking "Design a system for 1M users"
```

---

## 8. API Keys You Might Need

```bash
# GitHub (for github.py)
export GITHUB_TOKEN="ghp_..."

# Firecrawl (for firecrawl.py)
export FIRECRAWL_API_KEY="fc-..."

# Exa (for exa.py)
export EXA_API_KEY="..."

# Ref Tools (for ref.py)
export REF_API_KEY="ref-..."

# Semly (for semly.py)
export SEMLY_API_KEY="..."
```

See `.claude/MCP_SETUP.md` for where to get each key.

---

## 9. Keyboard Shortcuts & Tips

### Terminal Efficiency
```bash
# Save frequently used commands as aliases
alias craw='uv run crawl4ai.py'
alias github='uv run github.py'
alias search='uv run ref.py search'
alias think='uv run sequential-thinking.py sequentialthinking'

# Then use
search "your query"
github list_issues --repo owner/repo
```

### Piping & Filtering
```bash
# Extract data from JSON responses
uv run github.py list_issues --repo owner/repo | jq '.[] | {number, title}'

# Count results
uv run exa.py search "machine learning" | jq '.results | length'

# Save results
uv run crawl4ai.py scrape https://example.com > output.json
```

### Batch Operations
```bash
# Scrape multiple sites
for url in https://site1.com https://site2.com https://site3.com; do
  echo "Scraping $url..."
  uv run crawl4ai.py scrape "$url" > "$(echo $url | sed 's/[^a-zA-Z0-9]/_/g').json"
done
```

---

## 10. Troubleshooting

### Tool Won't Run
```bash
# Check Python version
python3 --version  # Need 3.8+

# Check uv is installed
uv --version
# If not: curl -LsSf https://astral.sh/uv/install.sh | sh

# Test basic help
uv run crawl4ai.py --help
```

### Missing API Key
```bash
# Check what's set
env | grep -i api_key

# Export missing key
export GITHUB_TOKEN="your-token"

# Verify and retry
echo $GITHUB_TOKEN
uv run github.py list
```

### Invalid JSON Output
```bash
# Validate with jq
uv run github.py list | jq . > /dev/null && echo "Valid JSON"

# If fails, see raw output
uv run github.py list --format text
```

### Connection Issues
```bash
# Check network
timeout 5 ping google.com

# Check if API is down
# Visit status page for service (GitHub, Firecrawl, etc)

# Try with timeout
timeout 60 uv run firecrawl.py scrape https://example.com
```

---

## 11. Next Steps

1. **Explore one tool deeply**:
   ```bash
   uv run github.py list        # See all functions
   uv run github.py info create_pull_request  # Deep dive
   ```

2. **Set up a tool you need**:
   ```bash
   export GITHUB_TOKEN="your-token"
   uv run github.py search_repositories --query "test"
   ```

3. **Try a workflow**:
   ```bash
   # Read the workflow guide
   cat .claude/commands/scrape.md

   # Try it
   uv run crawl4ai.py scrape https://example.com | jq .
   ```

4. **Integrate with your project**:
   ```bash
   # Use from another directory
   ~/cli-wrappers/github.py list_issues --repo owner/repo
   ```

5. **Customize in Claude Code**:
   - Create custom commands in `.claude/commands/`
   - Set up hooks in `.claude/settings.json`
   - Configure MCP servers in `.mcp.json`

---

## 12. Documentation Map

```
Start here: QUICK_START.md (this file)
       ↓
Learn patterns: CLAUDE.md
       ↓
Explore tools: INDEX.md
       ↓
Set up MCPs: .claude/MCP_SETUP.md
       ↓
Use workflows: .claude/commands/*.md
    ├── /scrape.md (web scraping)
    ├── /search.md (documentation search)
    ├── /github-pr.md (GitHub workflows)
    ├── /analyze-repo.md (repository analysis)
    └── /think.md (complex problem solving)
```

---

## Cheat Sheet

```bash
# Quick help (any tool)
uv run TOOL.py --help

# Explore progressively
uv run TOOL.py list                    # All functions
uv run TOOL.py info FUNCTION           # Detailed docs
uv run TOOL.py example FUNCTION        # Working examples
uv run TOOL.py FUNCTION --help         # Full reference

# Common tasks
uv run crawl4ai.py scrape https://site.com          # Scrape
uv run ref.py search "query"                        # Search docs
uv run github.py list_issues --repo owner/repo      # List issues
uv run repomix.py pack_codebase ~/project           # Analyze repo
uv run exa.py search "topic"                        # Web search
uv run sequential-thinking.py sequentialthinking "q"  # Think

# Save results
uv run TOOL.py FUNCTION > output.json

# Filter JSON
uv run TOOL.py FUNCTION | jq '.results[] | {title, url}'
```

---

**You're ready to go!** Start with `uv run crawl4ai.py --help` and explore from there.

For detailed info, see `CLAUDE.md` and the workflow guides in `.claude/commands/`.

**Last Updated**: 2025-02-01
