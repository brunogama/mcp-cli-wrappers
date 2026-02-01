#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "httpx>=0.24.0",
#     "pydantic>=2.0",
#     "click>=8.0",
#     "rich>=13.0",
#     "python-dotenv>=1.0.0",
# ]
# ///
"""
GitHub MCP CLI Wrapper
Production-ready wrapper with 4-level progressive disclosure.

Run with: uv run cli.py [COMMAND] [ARGS]

Levels:
  1. --help           Quick overview (~30 tokens)
  2. list             All functions
     info TOOL        Detailed documentation (~150 tokens)
  3. example TOOL     Working examples (~200 tokens)
  4. TOOL --help      Complete reference (~500 tokens)
"""

import json
import os
import sys
from enum import Enum
from typing import Any, Optional

import click
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

load_dotenv()

console = Console()

# ============================================================================
# DETAIL LEVELS
# ============================================================================

class DetailLevel(str, Enum):
    SUMMARY = "summary"      # counts, IDs only
    NORMAL = "normal"        # key fields (default)
    DETAILED = "detailed"    # all fields + relationships
    DEBUG = "debug"          # include timing, metadata


# ============================================================================
# LEVEL 1: QUICK HELP (~30 tokens)
# ============================================================================

QUICK_HELP = """GitHub MCP CLI - Repository operations, issues, PRs, actions

Namespaces:
  repo.*      Repository operations (files, branches, commits)
  issue.*     Issue management (create, update, search)
  pr.*        Pull request operations
  actions.*   GitHub Actions control
  security.*  Code scanning, dependabot alerts
  user.*      User and organization operations

Quick start:
  uv run cli.py list                    # See all functions
  uv run cli.py info create_pull_request  # Detailed docs
  uv run cli.py example list_issues     # Working examples

Options:
  --format json|text|table    Output format (default: text)
  --detail summary|normal|detailed|debug
"""

# ============================================================================
# LEVEL 2: FUNCTION INFO (~150 tokens each)
# ============================================================================

FUNCTION_INFO = {
    # === REPOSITORY NAMESPACE ===
    "get_file_contents": {
        "namespace": "repo",
        "description": "Retrieve file or directory contents from a repository",
        "parameters": [
            {"name": "owner", "type": "string", "required": True, "description": "Repository owner"},
            {"name": "repo", "type": "string", "required": True, "description": "Repository name"},
            {"name": "path", "type": "string", "required": False, "description": "File/directory path (default: /)"},
            {"name": "ref", "type": "string", "required": False, "description": "Git ref (branch, tag, commit)"},
            {"name": "sha", "type": "string", "required": False, "description": "Specific commit SHA"},
        ],
        "returns": "File content or directory listing",
        "related": ["create_or_update_file", "delete_file", "push_files"],
    },
    "search_code": {
        "namespace": "repo",
        "description": "Search code using GitHub's code search syntax",
        "parameters": [
            {"name": "query", "type": "string", "required": True, "description": "Search query (e.g., 'content:Skill language:Java')"},
            {"name": "sort", "type": "string", "required": False, "description": "Sort by: indexed"},
            {"name": "order", "type": "string", "required": False, "description": "Order: asc or desc"},
        ],
        "returns": "List of matching code files with snippets",
        "related": ["search_repositories", "get_file_contents"],
    },
    "search_repositories": {
        "namespace": "repo",
        "description": "Search repositories with advanced filtering",
        "parameters": [
            {"name": "query", "type": "string", "required": True, "description": "Search query (e.g., 'machine learning stars:>1000')"},
            {"name": "sort", "type": "string", "required": False, "description": "Sort: stars, forks, updated"},
            {"name": "order", "type": "string", "required": False, "description": "Order: asc or desc"},
            {"name": "minimal_output", "type": "boolean", "required": False, "description": "Return minimal info (default: true)"},
        ],
        "returns": "List of matching repositories",
        "related": ["create_repository", "fork_repository"],
    },
    "create_repository": {
        "namespace": "repo",
        "description": "Create a new repository",
        "parameters": [
            {"name": "name", "type": "string", "required": True, "description": "Repository name"},
            {"name": "description", "type": "string", "required": False, "description": "Repository description"},
            {"name": "organization", "type": "string", "required": False, "description": "Organization to create in"},
            {"name": "private", "type": "boolean", "required": False, "description": "Make repository private"},
            {"name": "auto_init", "type": "boolean", "required": False, "description": "Initialize with README"},
        ],
        "returns": "Created repository object",
        "related": ["fork_repository", "search_repositories"],
    },
    "fork_repository": {
        "namespace": "repo",
        "description": "Fork a repository to your account or organization",
        "parameters": [
            {"name": "owner", "type": "string", "required": True, "description": "Repository owner"},
            {"name": "repo", "type": "string", "required": True, "description": "Repository name"},
            {"name": "organization", "type": "string", "required": False, "description": "Organization to fork into"},
        ],
        "returns": "Forked repository object",
        "related": ["create_repository", "create_branch"],
    },
    "create_branch": {
        "namespace": "repo",
        "description": "Create a new branch in a repository",
        "parameters": [
            {"name": "owner", "type": "string", "required": True, "description": "Repository owner"},
            {"name": "repo", "type": "string", "required": True, "description": "Repository name"},
            {"name": "branch", "type": "string", "required": True, "description": "New branch name"},
            {"name": "from_branch", "type": "string", "required": False, "description": "Source branch (default: repo default)"},
        ],
        "returns": "Branch reference object",
        "related": ["list_branches", "list_commits"],
    },
    "list_branches": {
        "namespace": "repo",
        "description": "List all branches in a repository",
        "parameters": [
            {"name": "owner", "type": "string", "required": True, "description": "Repository owner"},
            {"name": "repo", "type": "string", "required": True, "description": "Repository name"},
            {"name": "page", "type": "integer", "required": False, "description": "Page number"},
            {"name": "per_page", "type": "integer", "required": False, "description": "Results per page (max 100)"},
        ],
        "returns": "List of branch objects",
        "related": ["create_branch", "list_commits"],
    },
    "list_commits": {
        "namespace": "repo",
        "description": "List commits in a repository",
        "parameters": [
            {"name": "owner", "type": "string", "required": True, "description": "Repository owner"},
            {"name": "repo", "type": "string", "required": True, "description": "Repository name"},
            {"name": "sha", "type": "string", "required": False, "description": "Branch/tag/SHA to list from"},
            {"name": "author", "type": "string", "required": False, "description": "Filter by author"},
            {"name": "page", "type": "integer", "required": False, "description": "Page number"},
            {"name": "per_page", "type": "integer", "required": False, "description": "Results per page"},
        ],
        "returns": "List of commit objects",
        "related": ["get_commit", "list_branches"],
    },
    "get_commit": {
        "namespace": "repo",
        "description": "Get detailed commit information including diff",
        "parameters": [
            {"name": "owner", "type": "string", "required": True, "description": "Repository owner"},
            {"name": "repo", "type": "string", "required": True, "description": "Repository name"},
            {"name": "sha", "type": "string", "required": True, "description": "Commit SHA"},
            {"name": "include_diff", "type": "boolean", "required": False, "description": "Include file diffs (default: true)"},
        ],
        "returns": "Commit object with files and stats",
        "related": ["list_commits", "create_or_update_file"],
    },

    # === FILE OPERATIONS ===
    "create_or_update_file": {
        "namespace": "file",
        "description": "Create or update a file in a repository",
        "parameters": [
            {"name": "owner", "type": "string", "required": True, "description": "Repository owner"},
            {"name": "repo", "type": "string", "required": True, "description": "Repository name"},
            {"name": "path", "type": "string", "required": True, "description": "File path"},
            {"name": "content", "type": "string", "required": True, "description": "File content"},
            {"name": "message", "type": "string", "required": True, "description": "Commit message"},
            {"name": "branch", "type": "string", "required": True, "description": "Target branch"},
            {"name": "sha", "type": "string", "required": False, "description": "Blob SHA (required for updates)"},
        ],
        "returns": "Commit object with file info",
        "related": ["get_file_contents", "delete_file", "push_files"],
    },
    "delete_file": {
        "namespace": "file",
        "description": "Delete a file from a repository",
        "parameters": [
            {"name": "owner", "type": "string", "required": True, "description": "Repository owner"},
            {"name": "repo", "type": "string", "required": True, "description": "Repository name"},
            {"name": "path", "type": "string", "required": True, "description": "File path to delete"},
            {"name": "message", "type": "string", "required": True, "description": "Commit message"},
            {"name": "branch", "type": "string", "required": True, "description": "Target branch"},
        ],
        "returns": "Commit object",
        "related": ["create_or_update_file", "get_file_contents"],
    },
    "push_files": {
        "namespace": "file",
        "description": "Push multiple files in a single commit",
        "parameters": [
            {"name": "owner", "type": "string", "required": True, "description": "Repository owner"},
            {"name": "repo", "type": "string", "required": True, "description": "Repository name"},
            {"name": "branch", "type": "string", "required": True, "description": "Target branch"},
            {"name": "files", "type": "array", "required": True, "description": "Array of {path, content} objects"},
            {"name": "message", "type": "string", "required": True, "description": "Commit message"},
        ],
        "returns": "Commit object",
        "related": ["create_or_update_file", "get_file_contents"],
    },

    # === ISSUES NAMESPACE ===
    "list_issues": {
        "namespace": "issue",
        "description": "List issues in a repository",
        "parameters": [
            {"name": "owner", "type": "string", "required": True, "description": "Repository owner"},
            {"name": "repo", "type": "string", "required": True, "description": "Repository name"},
            {"name": "state", "type": "string", "required": False, "description": "Filter: OPEN, CLOSED"},
            {"name": "labels", "type": "array", "required": False, "description": "Filter by label names"},
            {"name": "order_by", "type": "string", "required": False, "description": "Sort: CREATED_AT, UPDATED_AT, COMMENTS"},
            {"name": "direction", "type": "string", "required": False, "description": "Direction: ASC, DESC"},
            {"name": "per_page", "type": "integer", "required": False, "description": "Results per page"},
        ],
        "returns": "List of issue objects",
        "related": ["search_issues", "create_issue", "get_issue"],
    },
    "search_issues": {
        "namespace": "issue",
        "description": "Search issues with GitHub query syntax",
        "parameters": [
            {"name": "query", "type": "string", "required": True, "description": "Search query (e.g., 'is:open label:bug')"},
            {"name": "owner", "type": "string", "required": False, "description": "Limit to repository owner"},
            {"name": "repo", "type": "string", "required": False, "description": "Limit to repository"},
            {"name": "sort", "type": "string", "required": False, "description": "Sort: comments, reactions, created, updated"},
            {"name": "order", "type": "string", "required": False, "description": "Order: asc, desc"},
        ],
        "returns": "List of matching issues",
        "related": ["list_issues", "create_issue"],
    },
    "get_issue": {
        "namespace": "issue",
        "description": "Get issue details, comments, labels, or sub-issues",
        "parameters": [
            {"name": "method", "type": "string", "required": True, "description": "Operation: get, get_comments, get_sub_issues, get_labels"},
            {"name": "owner", "type": "string", "required": True, "description": "Repository owner"},
            {"name": "repo", "type": "string", "required": True, "description": "Repository name"},
            {"name": "issue_number", "type": "integer", "required": True, "description": "Issue number"},
            {"name": "page", "type": "integer", "required": False, "description": "Page for paginated results"},
        ],
        "returns": "Issue object or list of comments/labels",
        "related": ["list_issues", "update_issue", "add_issue_comment"],
    },
    "create_issue": {
        "namespace": "issue",
        "description": "Create a new issue",
        "parameters": [
            {"name": "owner", "type": "string", "required": True, "description": "Repository owner"},
            {"name": "repo", "type": "string", "required": True, "description": "Repository name"},
            {"name": "title", "type": "string", "required": True, "description": "Issue title"},
            {"name": "body", "type": "string", "required": False, "description": "Issue description"},
            {"name": "assignees", "type": "array", "required": False, "description": "Usernames to assign"},
            {"name": "labels", "type": "array", "required": False, "description": "Label names"},
            {"name": "milestone", "type": "integer", "required": False, "description": "Milestone number"},
        ],
        "returns": "Created issue object",
        "related": ["list_issues", "update_issue"],
    },
    "update_issue": {
        "namespace": "issue",
        "description": "Update an existing issue",
        "parameters": [
            {"name": "owner", "type": "string", "required": True, "description": "Repository owner"},
            {"name": "repo", "type": "string", "required": True, "description": "Repository name"},
            {"name": "issue_number", "type": "integer", "required": True, "description": "Issue number"},
            {"name": "title", "type": "string", "required": False, "description": "New title"},
            {"name": "body", "type": "string", "required": False, "description": "New description"},
            {"name": "state", "type": "string", "required": False, "description": "State: open, closed"},
            {"name": "state_reason", "type": "string", "required": False, "description": "Reason: completed, not_planned, duplicate"},
            {"name": "labels", "type": "array", "required": False, "description": "Label names"},
            {"name": "assignees", "type": "array", "required": False, "description": "Usernames to assign"},
        ],
        "returns": "Updated issue object",
        "related": ["get_issue", "create_issue"],
    },
    "add_issue_comment": {
        "namespace": "issue",
        "description": "Add a comment to an issue",
        "parameters": [
            {"name": "owner", "type": "string", "required": True, "description": "Repository owner"},
            {"name": "repo", "type": "string", "required": True, "description": "Repository name"},
            {"name": "issue_number", "type": "integer", "required": True, "description": "Issue number"},
            {"name": "body", "type": "string", "required": True, "description": "Comment content"},
        ],
        "returns": "Created comment object",
        "related": ["get_issue", "update_issue"],
    },

    # === PULL REQUESTS NAMESPACE ===
    "list_pull_requests": {
        "namespace": "pr",
        "description": "List pull requests in a repository",
        "parameters": [
            {"name": "owner", "type": "string", "required": True, "description": "Repository owner"},
            {"name": "repo", "type": "string", "required": True, "description": "Repository name"},
            {"name": "state", "type": "string", "required": False, "description": "Filter: open, closed, all"},
            {"name": "head", "type": "string", "required": False, "description": "Filter by head user:branch"},
            {"name": "base", "type": "string", "required": False, "description": "Filter by base branch"},
            {"name": "sort", "type": "string", "required": False, "description": "Sort: created, updated, popularity"},
            {"name": "direction", "type": "string", "required": False, "description": "Direction: asc, desc"},
        ],
        "returns": "List of PR objects",
        "related": ["create_pull_request", "get_pull_request"],
    },
    "create_pull_request": {
        "namespace": "pr",
        "description": "Create a new pull request",
        "parameters": [
            {"name": "owner", "type": "string", "required": True, "description": "Repository owner"},
            {"name": "repo", "type": "string", "required": True, "description": "Repository name"},
            {"name": "title", "type": "string", "required": True, "description": "PR title"},
            {"name": "head", "type": "string", "required": True, "description": "Branch containing changes"},
            {"name": "base", "type": "string", "required": True, "description": "Branch to merge into"},
            {"name": "body", "type": "string", "required": False, "description": "PR description"},
            {"name": "draft", "type": "boolean", "required": False, "description": "Create as draft PR"},
            {"name": "maintainer_can_modify", "type": "boolean", "required": False, "description": "Allow maintainer edits"},
        ],
        "returns": "Created PR object with URL",
        "related": ["list_pull_requests", "merge_pull_request", "update_pull_request"],
    },
    "get_pull_request": {
        "namespace": "pr",
        "description": "Get PR details, diffs, reviews, or comments",
        "parameters": [
            {"name": "owner", "type": "string", "required": True, "description": "Repository owner"},
            {"name": "repo", "type": "string", "required": True, "description": "Repository name"},
            {"name": "pull_number", "type": "integer", "required": True, "description": "PR number"},
        ],
        "returns": "PR object with full details",
        "related": ["list_pull_requests", "update_pull_request"],
    },
    "update_pull_request": {
        "namespace": "pr",
        "description": "Update an existing pull request",
        "parameters": [
            {"name": "owner", "type": "string", "required": True, "description": "Repository owner"},
            {"name": "repo", "type": "string", "required": True, "description": "Repository name"},
            {"name": "pull_number", "type": "integer", "required": True, "description": "PR number"},
            {"name": "title", "type": "string", "required": False, "description": "New title"},
            {"name": "body", "type": "string", "required": False, "description": "New description"},
            {"name": "state", "type": "string", "required": False, "description": "State: open, closed"},
            {"name": "base", "type": "string", "required": False, "description": "New base branch"},
            {"name": "draft", "type": "boolean", "required": False, "description": "Convert to/from draft"},
            {"name": "reviewers", "type": "array", "required": False, "description": "Usernames to request review"},
        ],
        "returns": "Updated PR object",
        "related": ["get_pull_request", "merge_pull_request"],
    },
    "merge_pull_request": {
        "namespace": "pr",
        "description": "Merge a pull request",
        "parameters": [
            {"name": "owner", "type": "string", "required": True, "description": "Repository owner"},
            {"name": "repo", "type": "string", "required": True, "description": "Repository name"},
            {"name": "pull_number", "type": "integer", "required": True, "description": "PR number"},
            {"name": "commit_title", "type": "string", "required": False, "description": "Merge commit title"},
            {"name": "commit_message", "type": "string", "required": False, "description": "Merge commit message"},
            {"name": "merge_method", "type": "string", "required": False, "description": "Method: merge, squash, rebase"},
        ],
        "returns": "Merge result with SHA",
        "related": ["get_pull_request", "update_pull_request"],
    },

    # === GITHUB ACTIONS NAMESPACE ===
    "list_workflows": {
        "namespace": "actions",
        "description": "List workflows in a repository",
        "parameters": [
            {"name": "owner", "type": "string", "required": True, "description": "Repository owner"},
            {"name": "repo", "type": "string", "required": True, "description": "Repository name"},
            {"name": "page", "type": "integer", "required": False, "description": "Page number"},
            {"name": "per_page", "type": "integer", "required": False, "description": "Results per page"},
        ],
        "returns": "List of workflow objects",
        "related": ["list_workflow_runs", "run_workflow"],
    },
    "list_workflow_runs": {
        "namespace": "actions",
        "description": "List workflow runs",
        "parameters": [
            {"name": "owner", "type": "string", "required": True, "description": "Repository owner"},
            {"name": "repo", "type": "string", "required": True, "description": "Repository name"},
            {"name": "workflow_id", "type": "string", "required": False, "description": "Filter by workflow ID"},
            {"name": "actor", "type": "string", "required": False, "description": "Filter by actor"},
            {"name": "branch", "type": "string", "required": False, "description": "Filter by branch"},
            {"name": "event", "type": "string", "required": False, "description": "Filter by event type"},
            {"name": "status", "type": "string", "required": False, "description": "Filter by status"},
        ],
        "returns": "List of workflow run objects",
        "related": ["list_workflows", "get_workflow_run", "run_workflow"],
    },
    "get_workflow_run": {
        "namespace": "actions",
        "description": "Get details of a workflow run",
        "parameters": [
            {"name": "owner", "type": "string", "required": True, "description": "Repository owner"},
            {"name": "repo", "type": "string", "required": True, "description": "Repository name"},
            {"name": "run_id", "type": "integer", "required": True, "description": "Workflow run ID"},
        ],
        "returns": "Workflow run object with jobs",
        "related": ["list_workflow_runs", "get_job_logs"],
    },
    "run_workflow": {
        "namespace": "actions",
        "description": "Trigger a workflow dispatch event",
        "parameters": [
            {"name": "owner", "type": "string", "required": True, "description": "Repository owner"},
            {"name": "repo", "type": "string", "required": True, "description": "Repository name"},
            {"name": "workflow_id", "type": "string", "required": True, "description": "Workflow file name or ID"},
            {"name": "ref", "type": "string", "required": True, "description": "Git ref to run on"},
            {"name": "inputs", "type": "object", "required": False, "description": "Workflow input parameters"},
        ],
        "returns": "Workflow dispatch result",
        "related": ["list_workflows", "list_workflow_runs"],
    },
    "get_job_logs": {
        "namespace": "actions",
        "description": "Get logs from a workflow job",
        "parameters": [
            {"name": "owner", "type": "string", "required": True, "description": "Repository owner"},
            {"name": "repo", "type": "string", "required": True, "description": "Repository name"},
            {"name": "job_id", "type": "integer", "required": False, "description": "Job ID (required if failed_only=false)"},
            {"name": "run_id", "type": "integer", "required": False, "description": "Run ID (required if failed_only=true)"},
            {"name": "failed_only", "type": "boolean", "required": False, "description": "Get all failed jobs in run"},
            {"name": "tail_lines", "type": "integer", "required": False, "description": "Lines from end (default: 500)"},
        ],
        "returns": "Job log content",
        "related": ["get_workflow_run", "list_workflow_runs"],
    },

    # === USER/ORG NAMESPACE ===
    "get_me": {
        "namespace": "user",
        "description": "Get authenticated user profile",
        "parameters": [],
        "returns": "User object with profile details",
        "related": ["search_users"],
    },
    "search_users": {
        "namespace": "user",
        "description": "Search for GitHub users",
        "parameters": [
            {"name": "query", "type": "string", "required": True, "description": "Search query (e.g., 'location:seattle followers:>100')"},
            {"name": "sort", "type": "string", "required": False, "description": "Sort: followers, repositories, joined"},
            {"name": "order", "type": "string", "required": False, "description": "Order: asc, desc"},
        ],
        "returns": "List of user objects",
        "related": ["get_me", "search_orgs"],
    },
    "search_orgs": {
        "namespace": "org",
        "description": "Search for GitHub organizations",
        "parameters": [
            {"name": "query", "type": "string", "required": True, "description": "Search query (e.g., 'microsoft location:california')"},
            {"name": "sort", "type": "string", "required": False, "description": "Sort: followers, repositories, joined"},
            {"name": "order", "type": "string", "required": False, "description": "Order: asc, desc"},
        ],
        "returns": "List of organization objects",
        "related": ["search_users"],
    },

    # === RELEASES ===
    "list_releases": {
        "namespace": "release",
        "description": "List releases in a repository",
        "parameters": [
            {"name": "owner", "type": "string", "required": True, "description": "Repository owner"},
            {"name": "repo", "type": "string", "required": True, "description": "Repository name"},
            {"name": "page", "type": "integer", "required": False, "description": "Page number"},
            {"name": "per_page", "type": "integer", "required": False, "description": "Results per page"},
        ],
        "returns": "List of release objects",
        "related": ["get_latest_release", "get_release_by_tag"],
    },
    "get_latest_release": {
        "namespace": "release",
        "description": "Get the latest release",
        "parameters": [
            {"name": "owner", "type": "string", "required": True, "description": "Repository owner"},
            {"name": "repo", "type": "string", "required": True, "description": "Repository name"},
        ],
        "returns": "Latest release object",
        "related": ["list_releases", "get_release_by_tag"],
    },
    "get_release_by_tag": {
        "namespace": "release",
        "description": "Get a release by tag name",
        "parameters": [
            {"name": "owner", "type": "string", "required": True, "description": "Repository owner"},
            {"name": "repo", "type": "string", "required": True, "description": "Repository name"},
            {"name": "tag", "type": "string", "required": True, "description": "Tag name (e.g., v1.0.0)"},
        ],
        "returns": "Release object",
        "related": ["list_releases", "get_latest_release"],
    },

    # === LABELS ===
    "list_labels": {
        "namespace": "label",
        "description": "List labels in a repository",
        "parameters": [
            {"name": "owner", "type": "string", "required": True, "description": "Repository owner"},
            {"name": "repo", "type": "string", "required": True, "description": "Repository name"},
        ],
        "returns": "List of label objects",
        "related": ["create_label", "update_label"],
    },
    "create_label": {
        "namespace": "label",
        "description": "Create a new label",
        "parameters": [
            {"name": "owner", "type": "string", "required": True, "description": "Repository owner"},
            {"name": "repo", "type": "string", "required": True, "description": "Repository name"},
            {"name": "name", "type": "string", "required": True, "description": "Label name"},
            {"name": "color", "type": "string", "required": True, "description": "Hex color without # (e.g., 'd73a4a')"},
            {"name": "description", "type": "string", "required": False, "description": "Label description"},
        ],
        "returns": "Created label object",
        "related": ["list_labels", "update_label"],
    },
}


# ============================================================================
# LEVEL 3: EXAMPLES (~200 tokens each)
# ============================================================================

FUNCTION_EXAMPLES = {
    "get_file_contents": [
        {
            "title": "Get file from main branch",
            "command": "uv run cli.py get_file_contents --owner anthropics --repo claude-code --path README.md",
        },
        {
            "title": "Get file from specific branch",
            "command": "uv run cli.py get_file_contents --owner myorg --repo myrepo --path src/main.py --ref feature-branch",
        },
        {
            "title": "List directory contents",
            "command": "uv run cli.py get_file_contents --owner myorg --repo myrepo --path src/",
        },
    ],
    "search_repositories": [
        {
            "title": "Search popular ML repos",
            "command": "uv run cli.py search_repositories --query 'machine learning stars:>1000 language:python'",
        },
        {
            "title": "Find repos by topic",
            "command": "uv run cli.py search_repositories --query 'topic:cli-tool' --sort stars",
        },
    ],
    "create_pull_request": [
        {
            "title": "Create feature PR",
            "command": "uv run cli.py create_pull_request --owner myorg --repo myrepo --title 'Add dark mode' --head feature/dark-mode --base main --body 'Implements dark mode toggle'",
        },
        {
            "title": "Create draft PR",
            "command": "uv run cli.py create_pull_request --owner myorg --repo myrepo --title 'WIP: Refactor auth' --head refactor/auth --base main --draft",
        },
    ],
    "list_issues": [
        {
            "title": "List open bugs",
            "command": "uv run cli.py list_issues --owner myorg --repo myrepo --state OPEN --labels bug",
        },
        {
            "title": "List issues with detail levels",
            "command": "uv run cli.py list_issues --owner myorg --repo myrepo --detail summary",
        },
    ],
    "create_issue": [
        {
            "title": "Create bug report",
            "command": "uv run cli.py create_issue --owner myorg --repo myrepo --title 'Auth bug on mobile' --body 'Steps to reproduce...' --labels bug,priority-high",
        },
    ],
    "search_issues": [
        {
            "title": "Search open bugs",
            "command": "uv run cli.py search_issues --query 'is:open label:bug' --owner myorg --repo myrepo",
        },
        {
            "title": "Find assigned issues",
            "command": "uv run cli.py search_issues --query 'assignee:myuser is:open'",
        },
    ],
    "merge_pull_request": [
        {
            "title": "Squash merge",
            "command": "uv run cli.py merge_pull_request --owner myorg --repo myrepo --pull_number 123 --merge_method squash",
        },
    ],
    "list_workflow_runs": [
        {
            "title": "List failed runs",
            "command": "uv run cli.py list_workflow_runs --owner myorg --repo myrepo --status failure",
        },
        {
            "title": "List runs on branch",
            "command": "uv run cli.py list_workflow_runs --owner myorg --repo myrepo --branch main",
        },
    ],
    "run_workflow": [
        {
            "title": "Trigger deployment",
            "command": "uv run cli.py run_workflow --owner myorg --repo myrepo --workflow_id deploy.yml --ref main --inputs '{\"environment\": \"staging\"}'",
        },
    ],
    "get_job_logs": [
        {
            "title": "Get failed job logs",
            "command": "uv run cli.py get_job_logs --owner myorg --repo myrepo --run_id 12345 --failed_only --tail_lines 100",
        },
    ],
    "push_files": [
        {
            "title": "Push multiple files",
            "command": """uv run cli.py push_files --owner myorg --repo myrepo --branch main --message "Update configs" --files '[{"path": "config.json", "content": "{}"}, {"path": "README.md", "content": "# Project"}]'""",
        },
    ],
}


# ============================================================================
# CLI IMPLEMENTATION
# ============================================================================

def validate_credentials() -> bool:
    """Check if GITHUB_TOKEN is set."""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        console.print("[red]Error: GITHUB_TOKEN not set[/red]")
        console.print("Set it with: export GITHUB_TOKEN='ghp_...'")
        return False
    return True


def format_output(data: Any, fmt: str = "text", detail: str = "normal") -> None:
    """Format and print output based on format and detail level."""
    if fmt == "json":
        console.print_json(json.dumps(data, indent=2, default=str))
    elif fmt == "table" and isinstance(data, list) and data:
        table = Table()
        if isinstance(data[0], dict):
            for key in data[0].keys():
                table.add_column(key)
            for item in data:
                table.add_row(*[str(v) for v in item.values()])
        console.print(table)
    else:
        if isinstance(data, dict):
            for key, value in data.items():
                console.print(f"[bold]{key}[/bold]: {value}")
        elif isinstance(data, list):
            for item in data:
                console.print(f"  - {item}")
        else:
            console.print(data)


@click.group(invoke_without_command=True)
@click.option("--format", "fmt", type=click.Choice(["text", "json", "table"]), default="text", help="Output format")
@click.option("--detail", type=click.Choice(["summary", "normal", "detailed", "debug"]), default="normal", help="Detail level")
@click.pass_context
def cli(ctx: click.Context, fmt: str, detail: str) -> None:
    """GitHub MCP CLI - Repository operations, issues, PRs, actions."""
    ctx.ensure_object(dict)
    ctx.obj["format"] = fmt
    ctx.obj["detail"] = detail

    if ctx.invoked_subcommand is None:
        console.print(QUICK_HELP)


@cli.command()
@click.pass_context
def list(ctx: click.Context) -> None:
    """List all available functions organized by namespace."""
    fmt = ctx.obj.get("format", "text")

    namespaces: dict[str, list[str]] = {}
    for func_name, info in FUNCTION_INFO.items():
        ns = info.get("namespace", "other")
        if ns not in namespaces:
            namespaces[ns] = []
        namespaces[ns].append(func_name)

    if fmt == "json":
        console.print_json(json.dumps(namespaces, indent=2))
    else:
        console.print("\n[bold]Available Functions by Namespace[/bold]\n")
        for ns, funcs in sorted(namespaces.items()):
            console.print(f"[cyan]{ns}.*[/cyan]")
            for func in sorted(funcs):
                desc = FUNCTION_INFO[func].get("description", "")[:50]
                console.print(f"  {func:30} {desc}")
            console.print()


@cli.command()
@click.argument("function_name")
@click.pass_context
def info(ctx: click.Context, function_name: str) -> None:
    """Show detailed documentation for a function."""
    fmt = ctx.obj.get("format", "text")

    if function_name not in FUNCTION_INFO:
        console.print(f"[red]Unknown function: {function_name}[/red]")
        console.print(f"Available: {', '.join(sorted(FUNCTION_INFO.keys())[:10])}...")
        sys.exit(1)

    func_info = FUNCTION_INFO[function_name]

    if fmt == "json":
        console.print_json(json.dumps(func_info, indent=2))
    else:
        console.print(f"\n{'='*60}")
        console.print(f"[bold]Function: {function_name}[/bold]")
        console.print(f"[dim]Namespace: {func_info.get('namespace', 'other')}[/dim]")
        console.print(f"{'='*60}\n")

        console.print(f"[bold]Description:[/bold]\n  {func_info.get('description', 'N/A')}\n")

        if func_info.get("parameters"):
            console.print("[bold]Parameters:[/bold]")
            for param in func_info["parameters"]:
                req = "[red]*[/red]" if param.get("required") else ""
                console.print(f"  --{param['name']:20} ({param['type']}) {req}")
                console.print(f"      {param.get('description', '')}")
            console.print()

        console.print(f"[bold]Returns:[/bold]\n  {func_info.get('returns', 'Dict[str, Any]')}\n")

        if func_info.get("related"):
            console.print(f"[bold]Related:[/bold] {', '.join(func_info['related'])}\n")


@cli.command()
@click.argument("function_name")
@click.pass_context
def example(ctx: click.Context, function_name: str) -> None:
    """Show working examples for a function."""
    fmt = ctx.obj.get("format", "text")

    if function_name not in FUNCTION_EXAMPLES:
        console.print(f"[yellow]No examples for: {function_name}[/yellow]")
        if function_name in FUNCTION_INFO:
            console.print("Try: uv run cli.py info " + function_name)
        sys.exit(1)

    examples = FUNCTION_EXAMPLES[function_name]

    if fmt == "json":
        console.print_json(json.dumps({"function": function_name, "examples": examples}, indent=2))
    else:
        console.print(f"\n{'='*60}")
        console.print(f"[bold]Examples for: {function_name}[/bold]")
        console.print(f"{'='*60}\n")

        for i, ex in enumerate(examples, 1):
            console.print(f"[cyan]Example {i}: {ex.get('title', 'Untitled')}[/cyan]")
            console.print(f"  $ {ex.get('command', 'N/A')}")
            if ex.get("output"):
                console.print(f"  Output: {ex['output']}")
            console.print()


# ============================================================================
# STUB COMMANDS (to be connected to actual MCP server)
# ============================================================================

@cli.command()
@click.option("--owner", required=True, help="Repository owner")
@click.option("--repo", required=True, help="Repository name")
@click.option("--path", default="/", help="File or directory path")
@click.option("--ref", help="Git ref (branch, tag, commit)")
@click.pass_context
def get_file_contents(ctx: click.Context, owner: str, repo: str, path: str, ref: Optional[str]) -> None:
    """Retrieve file or directory contents from a repository."""
    if not validate_credentials():
        sys.exit(1)

    # Stub: Replace with actual MCP call
    result = {
        "status": "stub",
        "message": f"Would fetch {path} from {owner}/{repo}",
        "params": {"owner": owner, "repo": repo, "path": path, "ref": ref},
    }
    format_output(result, ctx.obj.get("format", "text"))


@cli.command()
@click.option("--query", required=True, help="Search query")
@click.option("--sort", type=click.Choice(["stars", "forks", "updated"]), help="Sort field")
@click.option("--order", type=click.Choice(["asc", "desc"]), help="Sort order")
@click.pass_context
def search_repositories(ctx: click.Context, query: str, sort: Optional[str], order: Optional[str]) -> None:
    """Search repositories with advanced filtering."""
    if not validate_credentials():
        sys.exit(1)

    result = {
        "status": "stub",
        "message": f"Would search repos: {query}",
        "params": {"query": query, "sort": sort, "order": order},
    }
    format_output(result, ctx.obj.get("format", "text"))


@cli.command()
@click.option("--owner", required=True, help="Repository owner")
@click.option("--repo", required=True, help="Repository name")
@click.option("--title", required=True, help="PR title")
@click.option("--head", required=True, help="Branch containing changes")
@click.option("--base", required=True, help="Target branch")
@click.option("--body", help="PR description")
@click.option("--draft", is_flag=True, help="Create as draft PR")
@click.pass_context
def create_pull_request(ctx: click.Context, owner: str, repo: str, title: str, head: str, base: str, body: Optional[str], draft: bool) -> None:
    """Create a new pull request."""
    if not validate_credentials():
        sys.exit(1)

    result = {
        "status": "stub",
        "message": f"Would create PR: {title}",
        "params": {"owner": owner, "repo": repo, "title": title, "head": head, "base": base, "body": body, "draft": draft},
    }
    format_output(result, ctx.obj.get("format", "text"))


@cli.command()
@click.option("--owner", required=True, help="Repository owner")
@click.option("--repo", required=True, help="Repository name")
@click.option("--state", type=click.Choice(["OPEN", "CLOSED"]), help="Filter by state")
@click.option("--labels", help="Comma-separated labels")
@click.pass_context
def list_issues(ctx: click.Context, owner: str, repo: str, state: Optional[str], labels: Optional[str]) -> None:
    """List issues in a repository."""
    if not validate_credentials():
        sys.exit(1)

    labels_list = labels.split(",") if labels else None
    result = {
        "status": "stub",
        "message": f"Would list issues for {owner}/{repo}",
        "params": {"owner": owner, "repo": repo, "state": state, "labels": labels_list},
    }
    format_output(result, ctx.obj.get("format", "text"))


@cli.command()
@click.option("--owner", required=True, help="Repository owner")
@click.option("--repo", required=True, help="Repository name")
@click.option("--title", required=True, help="Issue title")
@click.option("--body", help="Issue description")
@click.option("--labels", help="Comma-separated labels")
@click.option("--assignees", help="Comma-separated usernames")
@click.pass_context
def create_issue(ctx: click.Context, owner: str, repo: str, title: str, body: Optional[str], labels: Optional[str], assignees: Optional[str]) -> None:
    """Create a new issue."""
    if not validate_credentials():
        sys.exit(1)

    result = {
        "status": "stub",
        "message": f"Would create issue: {title}",
        "params": {
            "owner": owner,
            "repo": repo,
            "title": title,
            "body": body,
            "labels": labels.split(",") if labels else None,
            "assignees": assignees.split(",") if assignees else None,
        },
    }
    format_output(result, ctx.obj.get("format", "text"))


@cli.command()
@click.option("--query", required=True, help="Search query")
@click.option("--owner", help="Limit to repository owner")
@click.option("--repo", help="Limit to repository")
@click.pass_context
def search_issues(ctx: click.Context, query: str, owner: Optional[str], repo: Optional[str]) -> None:
    """Search issues with GitHub query syntax."""
    if not validate_credentials():
        sys.exit(1)

    result = {
        "status": "stub",
        "message": f"Would search issues: {query}",
        "params": {"query": query, "owner": owner, "repo": repo},
    }
    format_output(result, ctx.obj.get("format", "text"))


@cli.command()
@click.option("--owner", required=True, help="Repository owner")
@click.option("--repo", required=True, help="Repository name")
@click.option("--pull_number", required=True, type=int, help="PR number")
@click.option("--merge_method", type=click.Choice(["merge", "squash", "rebase"]), default="merge", help="Merge method")
@click.pass_context
def merge_pull_request(ctx: click.Context, owner: str, repo: str, pull_number: int, merge_method: str) -> None:
    """Merge a pull request."""
    if not validate_credentials():
        sys.exit(1)

    result = {
        "status": "stub",
        "message": f"Would merge PR #{pull_number}",
        "params": {"owner": owner, "repo": repo, "pull_number": pull_number, "merge_method": merge_method},
    }
    format_output(result, ctx.obj.get("format", "text"))


@cli.command()
@click.option("--owner", required=True, help="Repository owner")
@click.option("--repo", required=True, help="Repository name")
@click.option("--status", type=click.Choice(["completed", "action_required", "cancelled", "failure", "neutral", "skipped", "stale", "success", "timed_out", "in_progress", "queued", "requested", "waiting", "pending"]), help="Filter by status")
@click.option("--branch", help="Filter by branch")
@click.pass_context
def list_workflow_runs(ctx: click.Context, owner: str, repo: str, status: Optional[str], branch: Optional[str]) -> None:
    """List workflow runs."""
    if not validate_credentials():
        sys.exit(1)

    result = {
        "status": "stub",
        "message": f"Would list workflow runs for {owner}/{repo}",
        "params": {"owner": owner, "repo": repo, "status": status, "branch": branch},
    }
    format_output(result, ctx.obj.get("format", "text"))


@cli.command()
@click.option("--owner", required=True, help="Repository owner")
@click.option("--repo", required=True, help="Repository name")
@click.option("--workflow_id", required=True, help="Workflow file or ID")
@click.option("--ref", required=True, help="Git ref to run on")
@click.option("--inputs", help="JSON object of workflow inputs")
@click.pass_context
def run_workflow(ctx: click.Context, owner: str, repo: str, workflow_id: str, ref: str, inputs: Optional[str]) -> None:
    """Trigger a workflow dispatch event."""
    if not validate_credentials():
        sys.exit(1)

    inputs_dict = json.loads(inputs) if inputs else None
    result = {
        "status": "stub",
        "message": f"Would trigger workflow {workflow_id}",
        "params": {"owner": owner, "repo": repo, "workflow_id": workflow_id, "ref": ref, "inputs": inputs_dict},
    }
    format_output(result, ctx.obj.get("format", "text"))


@cli.command()
@click.pass_context
def get_me(ctx: click.Context) -> None:
    """Get authenticated user profile."""
    if not validate_credentials():
        sys.exit(1)

    result = {
        "status": "stub",
        "message": "Would return authenticated user profile",
    }
    format_output(result, ctx.obj.get("format", "text"))


if __name__ == "__main__":
    cli()
