#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "click>=8.0",
#     "rich>=13.0",
# ]
# ///
"""
Apple DocSet RAG CLI Wrapper

A CLI for querying Apple/Xcode DocSets for LLM/RAG workflows.
Wraps the apple-docset-rag Swift CLI for local documentation access.

Run with: uv run cli.py [COMMAND] [ARGS]

4-Level Progressive Disclosure:
  Level 1: --help              Quick overview (~30 tokens)
  Level 2: list                All functions
           info FUNCTION       Detailed docs (~150 tokens)
  Level 3: example FUNCTION    Working examples (~200 tokens)
  Level 4: FUNCTION --help     Complete reference (~500 tokens)
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.syntax import Syntax
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Run: uv run cli.py --help")
    sys.exit(1)

console = Console()

# ===== CONFIGURATION =====

# Path to the apple-docset-rag executable
# Try release build first, then debug, then swift run
APPLE_DOCSET_RAG_PATH = os.environ.get("APPLE_DOCSET_RAG_PATH", "")
APPLE_DOCSET_RAG_PROJECT = os.environ.get(
    "APPLE_DOCSET_RAG_PROJECT",
    os.path.expanduser("~/Developer/Inbox/AppleDocsetRAG")
)
DEFAULT_TIMEOUT = int(os.environ.get("APPLE_DOCSET_TIMEOUT", "60"))

# ===== LEVEL 1: QUICK HELP =====

QUICK_HELP = """Apple DocSet RAG CLI

Query Apple/Xcode documentation locally for LLM/RAG workflows.

Available functions:
  list-docsets        List all available Apple docsets
  search              Search documentation by symbol name
  fetch               Fetch full documentation for a specific path
  export              Export docset symbols to JSONL

Quick start:
  uv run cli.py list                          # See all functions
  uv run cli.py info search                   # Detailed docs for search
  uv run cli.py example search                # Working examples
  uv run cli.py search "NSView" --limit 5     # Execute search

Options:
  --format json|text    Output format (default: json)
  --timeout SECONDS     Command timeout (default: 60)

Requirements:
  - macOS with Xcode installed
  - AppleDocsetRAG Swift CLI built

Environment:
  APPLE_DOCSET_RAG_PATH     Path to built executable
  APPLE_DOCSET_RAG_PROJECT  Path to Swift project (default: ~/Developer/Inbox/AppleDocsetRAG)
  APPLE_DOCSET_TIMEOUT      Request timeout in seconds (default: 60)
"""

# ===== LEVEL 2: FUNCTION INFO =====

FUNCTION_INFO: Dict[str, Dict[str, Any]] = {
    "list-docsets": {
        "name": "list-docsets",
        "description": "List all available Apple/Xcode docsets on this system",
        "long_description": """
List all installed documentation sets from Xcode and user-installed sources.
Discovers docsets from:
  - Active Xcode's Developer directory
  - /Applications/Xcode.app/Contents/Developer/Documentation/DocSets
  - ~/Library/Developer/Shared/Documentation/DocSets
        """.strip(),
        "parameters": [],
        "returns": "Array of docset objects with name, version, and path",
    },
    "search": {
        "name": "search",
        "description": "Search documentation by symbol name prefix",
        "long_description": """
Search the docset SQLite index for symbols matching a query.
Uses prefix matching on symbol names (case-insensitive).
Returns symbol name, type, and documentation path.
Results are ordered by name length (shorter = more relevant).
        """.strip(),
        "parameters": [
            {"name": "query", "type": "string", "required": True,
             "description": "Symbol name to search for (prefix match)"},
            {"name": "--docset", "type": "string", "required": False,
             "description": "Specific docset name to search (default: Apple API Reference)"},
            {"name": "--limit", "type": "integer", "required": False,
             "description": "Maximum results to return (default: 20)"},
            {"name": "--json", "type": "flag", "required": False,
             "description": "Output as JSON (default: true for wrapper)"},
        ],
        "returns": "Array of search results with name, type, and path",
    },
    "fetch": {
        "name": "fetch",
        "description": "Fetch full documentation text for a specific path",
        "long_description": """
Retrieve the full documentation content for a specific documentation path.
Extracts plain text from the underlying HTML, suitable for LLM context.
Use paths returned from the search command.
        """.strip(),
        "parameters": [
            {"name": "--docset", "type": "string", "required": True,
             "description": "Docset name containing the documentation"},
            {"name": "--path", "type": "string", "required": True,
             "description": "Documentation path (from search results)"},
            {"name": "--maxChars", "type": "integer", "required": False,
             "description": "Maximum characters to return (default: 80000)"},
            {"name": "--json", "type": "flag", "required": False,
             "description": "Output as JSON (default: true for wrapper)"},
        ],
        "returns": "Documentation object with title and extracted text content",
    },
    "export": {
        "name": "export",
        "description": "Export entire docset to JSONL for vector DB ingestion",
        "long_description": """
Bulk export all symbols and their documentation text to JSONL format.
Each line contains a JSON object with symbol name, type, path, and content.
Suitable for importing into vector databases for semantic search.
        """.strip(),
        "parameters": [
            {"name": "--docset", "type": "string", "required": True,
             "description": "Docset name to export"},
            {"name": "--out", "type": "string", "required": True,
             "description": "Output file path (JSONL format)"},
            {"name": "--max", "type": "integer", "required": False,
             "description": "Maximum symbols to export"},
            {"name": "--maxChars", "type": "integer", "required": False,
             "description": "Maximum characters per document (default: 30000)"},
        ],
        "returns": "Status message with export statistics",
    },
}

# ===== LEVEL 3: EXAMPLES =====

EXAMPLES: Dict[str, str] = {
    "list-docsets": """# List all available docsets
uv run cli.py list-docsets

# Output (JSON):
[
  {
    "name": "Apple API Reference",
    "version": "1.0",
    "path": "/Applications/Xcode.app/.../Apple_API_Reference.docset"
  }
]

# List in text format
uv run cli.py list-docsets --format text
""",
    "search": """# Search for NSView-related symbols
uv run cli.py search "NSView" --limit 10

# Search in specific docset
uv run cli.py search "CloudKit" --docset "Apple API Reference" --limit 5

# Search SwiftUI symbols
uv run cli.py search "SwiftUI" --limit 20

# Output (JSON):
[
  {"name": "NSView", "type": "Class", "path": "documentation/appkit/nsview"},
  {"name": "NSViewAnimation", "type": "Class", "path": "documentation/appkit/nsviewanimation"},
  ...
]
""",
    "fetch": """# Fetch documentation for a specific path
uv run cli.py fetch --docset "Apple API Reference" --path "documentation/appkit/nsview"

# Limit content size for LLM context
uv run cli.py fetch --docset "Apple API Reference" --path "documentation/swiftui/view" --maxChars 30000

# Output (JSON):
{
  "title": "NSView",
  "path": "documentation/appkit/nsview",
  "content": "The infrastructure for drawing, printing, and handling events in an app..."
}
""",
    "export": """# Export entire docset to JSONL
uv run cli.py export --docset "Apple API Reference" --out ~/docs/apple-api.jsonl

# Export with limits for testing
uv run cli.py export --docset "Apple API Reference" --out test.jsonl --max 100 --maxChars 10000

# Each line in output:
{"name": "NSView", "type": "Class", "path": "...", "content": "..."}
""",
}


def _find_executable() -> List[str]:
    """Find the apple-docset-rag executable or fallback to swift run."""
    # Check explicit path from environment
    if APPLE_DOCSET_RAG_PATH and os.path.isfile(APPLE_DOCSET_RAG_PATH):
        return [APPLE_DOCSET_RAG_PATH]

    project_path = Path(APPLE_DOCSET_RAG_PROJECT)

    # Try release build
    release_path = project_path / ".build" / "release" / "apple-docset-rag"
    if release_path.is_file():
        return [str(release_path)]

    # Try debug build
    debug_path = project_path / ".build" / "debug" / "apple-docset-rag"
    if debug_path.is_file():
        return [str(debug_path)]

    # Fallback to swift run
    return ["swift", "run", "--package-path", str(project_path), "apple-docset-rag"]


def _run_command(args: List[str], timeout: int = DEFAULT_TIMEOUT) -> Dict[str, Any]:
    """Execute the apple-docset-rag command and return parsed output."""
    cmd = _find_executable() + args

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=APPLE_DOCSET_RAG_PROJECT,
        )

        if result.returncode != 0:
            return {
                "error": True,
                "message": result.stderr.strip() or f"Command failed with code {result.returncode}",
                "stdout": result.stdout.strip(),
            }

        output = result.stdout.strip()

        # Try to parse as JSON
        try:
            return {"success": True, "data": json.loads(output)}
        except json.JSONDecodeError:
            return {"success": True, "data": output}

    except subprocess.TimeoutExpired:
        return {"error": True, "message": f"Command timed out after {timeout} seconds"}
    except FileNotFoundError:
        return {
            "error": True,
            "message": "apple-docset-rag not found. Build with: swift build -c release",
        }
    except Exception as e:
        return {"error": True, "message": str(e)}


def _format_output(data: Any, format_type: str = "json") -> None:
    """Format and print output based on format type."""
    if format_type == "json":
        console.print(json.dumps(data, indent=2))
    else:
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    for key, value in item.items():
                        console.print(f"[bold]{key}:[/bold] {value}")
                    console.print()
                else:
                    console.print(item)
        elif isinstance(data, dict):
            for key, value in data.items():
                if key == "content":
                    console.print(f"\n[bold]{key}:[/bold]")
                    console.print(value[:2000] + "..." if len(str(value)) > 2000 else value)
                else:
                    console.print(f"[bold]{key}:[/bold] {value}")
        else:
            console.print(data)


def show_quick_help():
    """Show level 1 quick help."""
    console.print(QUICK_HELP)


def show_list():
    """Show all available functions (level 2)."""
    table = Table(title="Available Functions")
    table.add_column("Function", style="cyan")
    table.add_column("Description")

    for name, info in FUNCTION_INFO.items():
        table.add_row(name, info["description"])

    console.print(table)
    console.print("\nUse 'uv run cli.py info FUNCTION' for detailed documentation")


def show_info(function_name: str):
    """Show detailed info for a function (level 2)."""
    if function_name not in FUNCTION_INFO:
        console.print(f"[red]Unknown function: {function_name}[/red]")
        console.print(f"Available: {', '.join(FUNCTION_INFO.keys())}")
        return

    info = FUNCTION_INFO[function_name]

    console.print(Panel(f"[bold cyan]{info['name']}[/bold cyan]"))
    console.print(f"\n[bold]Description:[/bold]\n{info['long_description']}\n")

    if info["parameters"]:
        console.print("[bold]Parameters:[/bold]")
        for param in info["parameters"]:
            req = "[red](required)[/red]" if param.get("required") else "[dim](optional)[/dim]"
            console.print(f"  {param['name']} {req}")
            console.print(f"    Type: {param['type']}")
            console.print(f"    {param['description']}")

    console.print(f"\n[bold]Returns:[/bold] {info['returns']}")
    console.print(f"\nUse 'uv run cli.py example {function_name}' for examples")


def show_example(function_name: str):
    """Show examples for a function (level 3)."""
    if function_name not in EXAMPLES:
        console.print(f"[red]No examples for: {function_name}[/red]")
        return

    console.print(Panel(f"[bold]Examples: {function_name}[/bold]"))
    console.print(Syntax(EXAMPLES[function_name], "bash", theme="monokai"))


# ===== COMMAND IMPLEMENTATIONS =====

def cmd_list_docsets(format_type: str = "json"):
    """List all available docsets."""
    result = _run_command(["list", "--json"])

    if result.get("error"):
        console.print(f"[red]Error:[/red] {result['message']}")
        return

    _format_output(result["data"], format_type)


def cmd_search(
    query: str,
    docset: Optional[str] = None,
    limit: int = 20,
    format_type: str = "json"
):
    """Search for symbols in docsets."""
    args = ["search", query, "--limit", str(limit), "--json"]

    if docset:
        args.extend(["--docset", docset])

    result = _run_command(args)

    if result.get("error"):
        console.print(f"[red]Error:[/red] {result['message']}")
        return

    _format_output(result["data"], format_type)


def cmd_fetch(
    docset: str,
    path: str,
    max_chars: int = 80000,
    format_type: str = "json"
):
    """Fetch documentation for a specific path."""
    args = ["fetch", "--docset", docset, "--path", path, "--max-chars", str(max_chars), "--json"]

    result = _run_command(args)

    if result.get("error"):
        console.print(f"[red]Error:[/red] {result['message']}")
        return

    _format_output(result["data"], format_type)


def cmd_export(
    docset: str,
    out: str,
    max_items: Optional[int] = None,
    max_chars: int = 30000,
):
    """Export docset to JSONL."""
    args = ["export", "--docset", docset, "--out", out, "--max-chars", str(max_chars)]

    if max_items:
        args.extend(["--max", str(max_items)])

    result = _run_command(args, timeout=600)  # Long timeout for export

    if result.get("error"):
        console.print(f"[red]Error:[/red] {result['message']}")
        return

    console.print(f"[green]Export complete:[/green] {out}")


def main():
    """Main entry point with argument parsing."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Apple DocSet RAG CLI - Query Apple documentation locally",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  uv run cli.py list                              # List all functions
  uv run cli.py search "NSView" --limit 10        # Search symbols
  uv run cli.py fetch --docset "Apple API Reference" --path "documentation/appkit/nsview"
        """
    )

    parser.add_argument("--format", choices=["json", "text"], default="json",
                        help="Output format (default: json)")

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Level 2: list and info commands
    subparsers.add_parser("list", help="List all available functions")

    info_parser = subparsers.add_parser("info", help="Show detailed info for a function")
    info_parser.add_argument("function", help="Function name")

    example_parser = subparsers.add_parser("example", help="Show examples for a function")
    example_parser.add_argument("function", help="Function name")

    # list-docsets command
    subparsers.add_parser("list-docsets", help="List all available docsets")

    # search command
    search_parser = subparsers.add_parser("search", help="Search documentation by symbol name")
    search_parser.add_argument("query", help="Symbol name to search for")
    search_parser.add_argument("--docset", help="Specific docset to search")
    search_parser.add_argument("--limit", type=int, default=20, help="Maximum results")

    # fetch command
    fetch_parser = subparsers.add_parser("fetch", help="Fetch documentation for a path")
    fetch_parser.add_argument("--docset", required=True, help="Docset name")
    fetch_parser.add_argument("--path", required=True, help="Documentation path")
    fetch_parser.add_argument("--maxChars", type=int, default=80000, help="Max characters")

    # export command
    export_parser = subparsers.add_parser("export", help="Export docset to JSONL")
    export_parser.add_argument("--docset", required=True, help="Docset name")
    export_parser.add_argument("--out", required=True, help="Output file path")
    export_parser.add_argument("--max", type=int, help="Maximum items to export")
    export_parser.add_argument("--maxChars", type=int, default=30000, help="Max chars per doc")

    args = parser.parse_args()

    if not args.command:
        show_quick_help()
        return

    if args.command == "list":
        show_list()
    elif args.command == "info":
        show_info(args.function)
    elif args.command == "example":
        show_example(args.function)
    elif args.command == "list-docsets":
        cmd_list_docsets(args.format)
    elif args.command == "search":
        cmd_search(args.query, args.docset, args.limit, args.format)
    elif args.command == "fetch":
        cmd_fetch(args.docset, args.path, args.maxChars, args.format)
    elif args.command == "export":
        cmd_export(args.docset, args.out, args.max, args.maxChars)


if __name__ == "__main__":
    main()
