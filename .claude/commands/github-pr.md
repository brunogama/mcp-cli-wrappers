# /github-pr - GitHub Pull Request Workflow

Create GitHub PRs with file pushing using progressive disclosure.

## Usage

```bash
/github-pr --repo owner/repo --title "Feature name"
/github-pr --repo owner/repo --title "Feature" --branch feature/xyz
/github-pr --help
```

## What This Command Does

1. Validate GitHub credentials and repository access
2. Create feature branch (if specified)
3. Push files to repository
4. Create pull request with description
5. Show PR URL for review

## Prerequisites

### GitHub Token Setup
```bash
# Generate at https://github.com/settings/tokens
export GITHUB_TOKEN="ghp_..."

# Verify it works
uv run github.py list
```

### Repository Configuration
```bash
export GITHUB_REPO="owner/repository"
```

## Progressive Disclosure Levels

### Level 1: Quick Help
```bash
uv run github.py --help
```

### Level 2: See All GitHub Functions
```bash
uv run github.py list

# Get detailed info about any function
uv run github.py info create_pull_request
uv run github.py info push_files
uv run github.py info create_issue
```

### Level 3: Working Examples
```bash
uv run github.py example create_pull_request
uv run github.py example push_files
uv run github.py example create_issue
```

### Level 4: Complete Reference
```bash
uv run github.py create_pull_request --help
uv run github.py push_files --help
uv run github.py create_issue --help
```

## Common GitHub Workflows

### Create a Pull Request

#### Step 1: View PR Documentation
```bash
# Quick overview
uv run github.py --help

# Detailed docs
uv run github.py info create_pull_request

# See working examples
uv run github.py example create_pull_request

# Complete reference
uv run github.py create_pull_request --help
```

#### Step 2: Push Files First
```bash
# See push documentation
uv run github.py info push_files

# Push your changes
uv run github.py push_files \
  --repo owner/repo \
  --branch feature/my-feature \
  --files "src/main.py" "tests/test_main.py"
```

#### Step 3: Create the PR
```bash
# Create PR after files are pushed
uv run github.py create_pull_request \
  --repo owner/repo \
  --title "Add new feature" \
  --body "This PR adds..." \
  --head feature/my-feature \
  --base main
```

### Manage GitHub Issues

#### Create an Issue
```bash
# View documentation
uv run github.py info create_issue

# Create issue
uv run github.py create_issue \
  --repo owner/repo \
  --title "Bug: X is broken" \
  --body "Description of the bug..."
```

#### List Issues
```bash
# View documentation
uv run github.py info list_issues

# List all open issues
uv run github.py list_issues --repo owner/repo

# Filter by state
uv run github.py list_issues --repo owner/repo --state open
```

#### Update Issue
```bash
# View documentation
uv run github.py info update_issue

# Update issue status
uv run github.py update_issue \
  --repo owner/repo \
  --issue-number 123 \
  --state closed
```

### View Repository Information

#### Search Repositories
```bash
# View documentation
uv run github.py info search_repositories

# Search for repositories
uv run github.py search_repositories --query "cli tools"
```

#### List Commits
```bash
# View documentation
uv run github.py info list_commits

# List repository commits
uv run github.py list_commits --repo owner/repo
```

#### Get File Contents
```bash
# View documentation
uv run github.py info get_file_contents

# Read a file from repository
uv run github.py get_file_contents \
  --repo owner/repo \
  --path "src/main.py"
```

## Detailed Workflow: From Code to PR

### 1. Prepare Your Changes
```bash
# Make changes locally
# Edit files, test locally, etc.

# Verify changes
git status
git diff
```

### 2. Push Files to Repository
```bash
# Get help on push_files
uv run github.py info push_files

# See an example
uv run github.py example push_files

# Push your changes
uv run github.py push_files \
  --repo owner/repo \
  --branch feature/my-feature \
  --files "src/main.py" "tests/test.py"
```

### 3. Create Pull Request
```bash
# Get help on create_pull_request
uv run github.py info create_pull_request

# See working example
uv run github.py example create_pull_request

# Create PR
uv run github.py create_pull_request \
  --repo owner/repo \
  --title "Add awesome feature" \
  --body "## Changes\n- Added X\n- Fixed Y" \
  --head feature/my-feature \
  --base main
```

### 4. Add Comments to PR
```bash
# Get help on add_issue_comment
uv run github.py info add_issue_comment

# Add comment to PR (PRs are issues)
uv run github.py add_issue_comment \
  --repo owner/repo \
  --issue-number 456 \
  --body "Ready for review"
```

## Output Formats

### JSON Response
```bash
# All operations return JSON
uv run github.py create_pull_request ... | jq .

# Extract PR URL
uv run github.py create_pull_request ... | jq '.html_url'

# Get issue number
uv run github.py create_issue ... | jq '.number'
```

### Human-Readable
```bash
# Convert to text
uv run github.py create_pull_request ... --format text
```

## Integration Examples

### Automated PR Creation
```bash
#!/bin/bash
REPO="owner/repo"
BRANCH="feature/$(date +%s)"
TITLE="Auto-generated fix: $(date)"

# Push files
uv run github.py push_files \
  --repo "$REPO" \
  --branch "$BRANCH" \
  --files "src/fix.py"

# Create PR
uv run github.py create_pull_request \
  --repo "$REPO" \
  --title "$TITLE" \
  --head "$BRANCH" \
  --base main
```

### Extract PR Information
```bash
# Get all open PRs
uv run github.py list_issues --repo owner/repo --state open | jq '.[] | {number, title, url}'

# Get specific PR details
uv run github.py list_commits --repo owner/repo | jq '.[0:3] | .[] | {sha, message, author}'
```

### Update Multiple Issues
```bash
# Close old issues
for issue_num in 123 124 125; do
  uv run github.py update_issue \
    --repo owner/repo \
    --issue-number "$issue_num" \
    --state closed
done
```

## Security & Safety

### Required Scopes for GitHub Token
```
- repo (full control of repositories)
- issues (read/write issues)
- pull-requests (read/write PRs)
- contents (read/write repository contents)
```

### Before Running

✓ Verify repository URL is correct
✓ Check branch names (don't push to main by default)
✓ Review files being pushed
✓ Test locally before pushing
✓ Get approval for sensitive changes

### Safety Checks
```bash
# Always test locally first
git status
git diff

# Verify token has correct scopes
# Verify repository is correct
echo $GITHUB_REPO

# Dry-run operations when possible
uv run github.py --dry-run ...
```

## Troubleshooting

### Authentication Failed
```bash
# Check token is set
echo $GITHUB_TOKEN

# Verify token has correct scopes
# Visit: https://github.com/settings/tokens

# Generate new token if needed
# https://github.com/settings/tokens/new
```

### Repository Not Found
```bash
# Verify repository name
echo $GITHUB_REPO

# Check you have access
uv run github.py search_repositories --query "your-repo"

# Use correct format: owner/repo
uv run github.py list_issues --repo owner/repo
```

### Files Not Pushed
```bash
# Verify file paths are correct
ls -la src/main.py tests/test.py

# Check branch name is valid
git branch -a

# Try again with explicit paths
uv run github.py push_files --repo owner/repo --branch feature/x --files "$(pwd)/src/main.py"
```

### PR Creation Failed
```bash
# Verify branch was pushed first
uv run github.py list_commits --repo owner/repo | head

# Check base branch exists
uv run github.py list_issues --repo owner/repo

# Try with full details
uv run github.py create_pull_request \
  --repo owner/repo \
  --title "Title" \
  --body "Description" \
  --head feature/branch \
  --base main
```

## See Also

- GitHub documentation: `uv run github.py --help`
- Push files: `uv run github.py info push_files`
- Create PR: `uv run github.py info create_pull_request`
- Create issue: `uv run github.py info create_issue`
- Full reference: `uv run github.py create_pull_request --help`
