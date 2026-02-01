# /analyze-repo - Repository Analysis & Packing

Analyze and consolidate repositories for documentation and AI understanding.

## Usage

```bash
/analyze-repo /path/to/repo
/analyze-repo --repo owner/repo
/analyze-repo --help
```

## What This Command Does

1. Accept repository path or GitHub URL
2. Analyze codebase structure
3. Pack repository content for AI consumption
4. Generate optional skill documentation
5. Show analysis summary

## Progressive Disclosure Levels

### Level 1: Quick Help
```bash
uv run repomix.py --help
```

### Level 2: See All Functions
```bash
uv run repomix.py list

# Get detailed info
uv run repomix.py info pack_codebase
uv run repomix.py info pack_remote_repository
uv run repomix.py info generate_skill
```

### Level 3: Working Examples
```bash
uv run repomix.py example pack_codebase
uv run repomix.py example pack_remote_repository
uv run repomix.py example generate_skill
```

### Level 4: Complete Reference
```bash
uv run repomix.py pack_codebase --help
uv run repomix.py pack_remote_repository --help
uv run repomix.py generate_skill --help
```

## Local Repository Analysis

### Pack a Local Repository
```bash
# Quick overview
uv run repomix.py --help

# See detailed documentation
uv run repomix.py info pack_codebase

# View working examples
uv run repomix.py example pack_codebase

# Run the packing
uv run repomix.py pack_codebase ~/my-project
```

### Common Local Packing Tasks

#### Pack Entire Project
```bash
# Default: packs everything
uv run repomix.py pack_codebase ~/my-project > project_pack.txt

# Save to file
uv run repomix.py pack_codebase ~/my-project --output ~/packed_project.txt
```

#### Pack Specific Directory
```bash
# Pack just the source code
uv run repomix.py pack_codebase ~/my-project/src

# Pack just tests
uv run repomix.py pack_codebase ~/my-project/tests

# Pack single file
uv run repomix.py pack_codebase ~/my-project/main.py
```

#### Include/Exclude Patterns
```bash
# Exclude node_modules, .git, etc
uv run repomix.py pack_codebase ~/my-project \
  --exclude "node_modules" \
  --exclude ".git" \
  --exclude "__pycache__"

# Include only Python files
uv run repomix.py pack_codebase ~/my-project \
  --include "*.py"

# Include multiple patterns
uv run repomix.py pack_codebase ~/my-project \
  --include "*.py" \
  --include "*.md"
```

#### Custom Output Formats
```bash
# Default text format
uv run repomix.py pack_codebase ~/my-project

# JSON output for parsing
uv run repomix.py pack_codebase ~/my-project --format json

# Save as markdown
uv run repomix.py pack_codebase ~/my-project --format markdown
```

## Remote Repository Analysis

### Pack a GitHub Repository
```bash
# Quick help
uv run repomix.py info pack_remote_repository

# See examples
uv run repomix.py example pack_remote_repository

# Pack a repository
uv run repomix.py pack_remote_repository anthropic/anthropic-sdk-python
```

### Common Remote Tasks

#### Pack Popular Projects
```bash
# Pack any public repository
uv run repomix.py pack_remote_repository owner/repo

# Pack specific branch
uv run repomix.py pack_remote_repository owner/repo --branch main

# Pack specific tag/release
uv run repomix.py pack_remote_repository owner/repo --ref v1.0.0
```

#### Analyze Frameworks
```bash
# Django
uv run repomix.py pack_remote_repository django/django

# FastAPI
uv run repomix.py pack_remote_repository tiangolo/fastapi

# Vue.js
uv run repomix.py pack_remote_repository vuejs/vue

# React
uv run repomix.py pack_remote_repository facebook/react
```

#### Study Open Source Projects
```bash
# Linux kernel
uv run repomix.py pack_remote_repository torvalds/linux --include "*.c"

# Python standard library
uv run repomix.py pack_remote_repository python/cpython

# LLMs
uv run repomix.py pack_remote_repository openai/gpt-3.5-turbo-examples
```

## Generate Skill Documentation

### Create Claude Skills from Repository
```bash
# Quick help
uv run repomix.py info generate_skill

# See examples
uv run repomix.py example generate_skill

# Generate skill from repository
uv run repomix.py generate_skill ~/my-project --output skill.md
```

### Skill Generation Examples

#### Convert Project to Skill
```bash
# Generate comprehensive skill documentation
uv run repomix.py generate_skill ~/my-project > SKILL.md

# Generate for specific module
uv run repomix.py generate_skill ~/my-project/src/core --output core_skill.md

# Include examples in skill
uv run repomix.py generate_skill ~/my-project --include-examples
```

#### Skills for Different Purposes
```bash
# Skill for using the library
uv run repomix.py generate_skill ~/my-project --type usage

# Skill for contributing to project
uv run repomix.py generate_skill ~/my-project --type development

# Skill for API documentation
uv run repomix.py generate_skill ~/my-project --type api
```

## Combined Workflow: Full Analysis

### Complete Repository Understanding
```bash
#!/bin/bash
REPO="~/my-project"

echo "=== Step 1: Quick Analysis ==="
uv run repomix.py pack_codebase "$REPO" --format json > analysis.json

echo "=== Step 2: Generate Documentation ==="
uv run repomix.py generate_skill "$REPO" --output SKILL.md

echo "=== Step 3: Create Markdown Version ==="
uv run repomix.py pack_codebase "$REPO" --format markdown > README_PACKED.md

echo "=== Complete! ==="
echo "Files created:"
echo "  - analysis.json (machine-readable)"
echo "  - SKILL.md (for Claude)"
echo "  - README_PACKED.md (human-readable)"
```

### Consolidate for Claude
```bash
# Create comprehensive knowledge base
uv run repomix.py pack_codebase ~/my-project \
  --exclude "node_modules" \
  --exclude ".git" \
  --exclude "dist" \
  --output consolidated.txt

# Use in Claude conversation
# "Here's my project: [paste consolidated.txt]"
```

## Integration Examples

### Analyze Multiple Projects
```bash
# Compare two repositories
for repo in ~/project1 ~/project2; do
  echo "=== $(basename $repo) ==="
  uv run repomix.py pack_codebase "$repo" > "${repo}_analysis.txt"
done
```

### Archive Projects for Documentation
```bash
# Create dated archive
DATE=$(date +%Y-%m-%d)
uv run repomix.py pack_codebase ~/my-project \
  > "archives/project_${DATE}.txt"
```

### Extract Metrics
```bash
# Get file count and structure
uv run repomix.py pack_codebase ~/my-project --format json | jq '.file_count'

# Get language distribution
uv run repomix.py pack_codebase ~/my-project --format json | jq '.languages'
```

## Output Formats

### Text Format (Default)
```bash
# Human-readable with all code
uv run repomix.py pack_codebase ~/my-project

# Best for: Reading, understanding, sharing with humans
```

### JSON Format
```bash
# Machine-readable for processing
uv run repomix.py pack_codebase ~/my-project --format json

# Parse with jq
uv run repomix.py pack_codebase ~/my-project --format json | jq '.files | length'
```

### Markdown Format
```bash
# Formatted for documentation
uv run repomix.py pack_codebase ~/my-project --format markdown

# Best for: Creating wiki, documentation, sharing
```

## Advanced Options

### Exclude Common Directories
```bash
# Exclude multiple patterns
uv run repomix.py pack_codebase ~/my-project \
  --exclude "node_modules" \
  --exclude ".git" \
  --exclude ".env" \
  --exclude "__pycache__" \
  --exclude "dist" \
  --exclude "build"
```

### Include Only Specific Files
```bash
# Only Python files
uv run repomix.py pack_codebase ~/my-project --include "*.py"

# Python + markdown
uv run repomix.py pack_codebase ~/my-project \
  --include "*.py" \
  --include "*.md"

# Source code only (no tests)
uv run repomix.py pack_codebase ~/my-project \
  --include "src/**/*.py"
```

### Limit Output Size
```bash
# Create summary (fewer files)
uv run repomix.py pack_codebase ~/my-project --max-files 50

# Create comprehensive (all files)
uv run repomix.py pack_codebase ~/my-project --max-files unlimited
```

## Troubleshooting

### Too Much Output
```bash
# Exclude unnecessary directories
uv run repomix.py pack_codebase ~/project \
  --exclude "node_modules" \
  --exclude ".git"

# Use include instead of exclude
uv run repomix.py pack_codebase ~/project --include "src/**/*.py"
```

### Remote Repository Not Found
```bash
# Verify repository name
uv run repomix.py pack_remote_repository owner/repo

# Check GitHub accessibility
# Repositories must be public or you need GitHub token
export GITHUB_TOKEN="ghp_..."
uv run repomix.py pack_remote_repository owner/repo
```

### Generation Takes Too Long
```bash
# Limit to specific directory
uv run repomix.py pack_codebase ~/project/src

# Limit file count
uv run repomix.py pack_codebase ~/project --max-files 100

# Exclude large directories
uv run repomix.py pack_codebase ~/project --exclude "node_modules"
```

### Output File Too Large
```bash
# Use include for specific files
uv run repomix.py pack_codebase ~/project --include "*.py"

# Compress to save space
uv run repomix.py pack_codebase ~/project > packed.txt && gzip packed.txt
```

## See Also

- Repomix documentation: `uv run repomix.py --help`
- Pack local: `uv run repomix.py info pack_codebase`
- Pack remote: `uv run repomix.py info pack_remote_repository`
- Generate skill: `uv run repomix.py info generate_skill`
- Full reference: `uv run repomix.py pack_codebase --help`
