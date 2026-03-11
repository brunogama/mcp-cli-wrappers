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
Ref Tools MCP CLI Wrapper

A comprehensive CLI for interacting with the ref-tools-mcp documentation server.
Provides search and read capabilities for technical documentation.

Run with: uv run cli.py [COMMAND] [ARGS]

4-Level Progressive Disclosure:
  Level 1: --help              Quick overview (~30 tokens)
  Level 2: list                All functions
           info FUNCTION       Detailed docs (~150 tokens)
  Level 3: example FUNCTION    Working examples (~200 tokens)
  Level 4: FUNCTION --help     Complete reference (~500 tokens)
"""

import argparse
import json
import os
import sys
from typing import Any, Dict, List, Optional

try:
    import httpx
    from dotenv import load_dotenv
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Run: uv run cli.py --help")
    sys.exit(1)

# Load environment variables from script directory (.env first, then .env.local overrides)
_script_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(_script_dir, ".env"))
load_dotenv(os.path.join(_script_dir, ".env.local"), override=True)

console = Console()

# ===== CONFIGURATION =====

REF_API_KEY = os.environ.get("REF_API_KEY", "")
REF_API_URL = os.environ.get("REF_API_URL", "https://api.ref.tools")
DEFAULT_TIMEOUT = int(os.environ.get("REF_TIMEOUT", "30"))

# ===== LEVEL 1: QUICK HELP =====

QUICK_HELP = """Ref Tools MCP CLI

Search and read technical documentation via ref-tools-mcp server.

Available functions:
  search              Search documentation by query
  read_url            Read content from a documentation URL
  check               Validate a file against ref-tools rules
  analyze             Analyze a directory or file
  info                Show server information
  version             Display version information
  config              Show current configuration

Quick start:
  uv run cli.py list                     # See all functions
  uv run cli.py info search              # Detailed docs for search
  uv run cli.py example search           # Working examples
  uv run cli.py search --query "async"   # Execute search

Options:
  --format json|text    Output format (default: text)
  --verbose             Enable verbose output

Environment:
  REF_API_KEY           API key for authentication (required)
  REF_API_URL           API endpoint (default: https://api.ref.tools)
  REF_TIMEOUT           Request timeout in seconds (default: 30)
"""

# ===== LEVEL 2: FUNCTION INFO =====

FUNCTION_INFO: Dict[str, Dict[str, Any]] = {
    "search": {
        "name": "search",
        "description": "Search technical documentation by query string",
        "long_description": """
Search the ref-tools documentation database for relevant content.
Supports natural language queries and technical terms.
Returns ranked results with snippets and source URLs.
        """.strip(),
        "parameters": [
            {
                "name": "query",
                "type": "string",
                "required": True,
                "description": "Search query string (natural language or technical terms)"
            },
            {
                "name": "limit",
                "type": "integer",
                "required": False,
                "default": 10,
                "description": "Maximum number of results to return (1-100)"
            },
            {
                "name": "filter",
                "type": "string",
                "required": False,
                "description": "Filter results by category (e.g., 'python', 'javascript')"
            }
        ],
        "returns": "List of documentation results with title, snippet, URL, and relevance score",
        "related": ["read_url"]
    },
    "read_url": {
        "name": "read_url",
        "description": "Read and extract content from a documentation URL",
        "long_description": """
Fetch and parse content from a documentation URL.
Extracts clean text, code blocks, and metadata.
Handles various documentation formats (HTML, Markdown, RST).
        """.strip(),
        "parameters": [
            {
                "name": "url",
                "type": "string",
                "required": True,
                "description": "Full URL to the documentation page"
            },
            {
                "name": "extract_code",
                "type": "boolean",
                "required": False,
                "default": True,
                "description": "Extract code blocks separately"
            },
            {
                "name": "include_metadata",
                "type": "boolean",
                "required": False,
                "default": False,
                "description": "Include page metadata (title, author, date)"
            }
        ],
        "returns": "Extracted documentation content with text, code blocks, and optional metadata",
        "related": ["search"]
    },
    "check": {
        "name": "check",
        "description": "Validate a file against ref-tools rules",
        "long_description": """
Check a local file for compliance with ref-tools standards.
Validates syntax, structure, and documentation quality.
Returns detailed feedback with suggestions for improvement.
        """.strip(),
        "parameters": [
            {
                "name": "filepath",
                "type": "string",
                "required": True,
                "description": "Path to the file to check"
            },
            {
                "name": "strict",
                "type": "boolean",
                "required": False,
                "default": False,
                "description": "Enable strict checking mode"
            }
        ],
        "returns": "Validation results with issues, warnings, and suggestions",
        "related": ["analyze"]
    },
    "analyze": {
        "name": "analyze",
        "description": "Analyze a directory or file structure",
        "long_description": """
Perform comprehensive analysis of a directory or file.
Scans for documentation quality, code patterns, and structure.
Supports recursive analysis with include/exclude filters.
        """.strip(),
        "parameters": [
            {
                "name": "path",
                "type": "string",
                "required": True,
                "description": "Path to directory or file to analyze"
            },
            {
                "name": "recursive",
                "type": "boolean",
                "required": False,
                "default": False,
                "description": "Analyze directories recursively"
            },
            {
                "name": "include",
                "type": "string",
                "required": False,
                "description": "File patterns to include (e.g., '*.py')"
            },
            {
                "name": "exclude",
                "type": "string",
                "required": False,
                "description": "File patterns to exclude (e.g., '__pycache__')"
            }
        ],
        "returns": "Analysis report with metrics, issues, and recommendations",
        "related": ["check"]
    },
    "info": {
        "name": "info",
        "description": "Show server information and capabilities",
        "long_description": """
Display information about the ref-tools-mcp server.
Shows available features, API version, and rate limits.
Useful for debugging connection issues.
        """.strip(),
        "parameters": [],
        "returns": "Server information including version, features, and limits",
        "related": ["version", "config"]
    },
    "version": {
        "name": "version",
        "description": "Display ref-tools-mcp version",
        "long_description": """
Show the current version of the ref-tools-mcp server.
Includes client library version for compatibility checking.
        """.strip(),
        "parameters": [],
        "returns": "Version information for server and client",
        "related": ["info"]
    },
    "config": {
        "name": "config",
        "description": "Show current configuration",
        "long_description": """
Display the current CLI configuration settings.
Shows API endpoint, timeout, and masked API key.
Useful for verifying environment setup.
        """.strip(),
        "parameters": [],
        "returns": "Current configuration with masked sensitive values",
        "related": ["info"]
    }
}

# ===== LEVEL 3: EXAMPLES =====

FUNCTION_EXAMPLES: Dict[str, List[Dict[str, str]]] = {
    "search": [
        {
            "title": "Basic search",
            "command": 'uv run cli.py search --query "async await python"',
            "description": "Search for async/await documentation in Python"
        },
        {
            "title": "Search with limit",
            "command": 'uv run cli.py search --query "react hooks" --limit 5',
            "description": "Get top 5 results for React hooks"
        },
        {
            "title": "Filtered search",
            "command": 'uv run cli.py search --query "type hints" --filter python --format json',
            "description": "Search Python type hints with JSON output"
        }
    ],
    "read_url": [
        {
            "title": "Read documentation page",
            "command": 'uv run cli.py read_url --url "https://docs.python.org/3/library/asyncio.html"',
            "description": "Extract content from Python asyncio docs"
        },
        {
            "title": "Read with code extraction",
            "command": 'uv run cli.py read_url --url "https://example.com/docs" --extract-code',
            "description": "Read page and separately extract code blocks"
        },
        {
            "title": "Read with metadata",
            "command": 'uv run cli.py read_url --url "https://example.com/api" --include-metadata --format json',
            "description": "Get full content with metadata as JSON"
        }
    ],
    "check": [
        {
            "title": "Check a Python file",
            "command": "uv run cli.py check --filepath src/main.py",
            "description": "Validate main.py against ref-tools rules"
        },
        {
            "title": "Strict checking",
            "command": "uv run cli.py check --filepath README.md --strict",
            "description": "Check README with strict validation"
        }
    ],
    "analyze": [
        {
            "title": "Analyze current directory",
            "command": "uv run cli.py analyze --path .",
            "description": "Analyze files in current directory"
        },
        {
            "title": "Recursive analysis",
            "command": 'uv run cli.py analyze --path ./src --recursive --include "*.py"',
            "description": "Recursively analyze Python files in src/"
        },
        {
            "title": "Analysis with exclusions",
            "command": 'uv run cli.py analyze --path . -r --include "*.py" --exclude "__pycache__"',
            "description": "Analyze Python files excluding cache directories"
        }
    ],
    "info": [
        {
            "title": "Show server info",
            "command": "uv run cli.py info",
            "description": "Display ref-tools-mcp server information"
        }
    ],
    "version": [
        {
            "title": "Show version",
            "command": "uv run cli.py version",
            "description": "Display current version"
        }
    ],
    "config": [
        {
            "title": "Show configuration",
            "command": "uv run cli.py config",
            "description": "Display current settings (API key masked)"
        }
    ]
}

# ===== API CLIENT =====


class RefToolsClient:
    """Client for interacting with ref-tools-mcp server."""

    def __init__(self, api_key: str, base_url: str, timeout: int = 30):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._client: Optional[httpx.Client] = None

    def _get_client(self) -> httpx.Client:
        if self._client is None:
            self._client = httpx.Client(
                base_url=self.base_url,
                timeout=self.timeout,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "User-Agent": "ref-cli/1.0.0"
                }
            )
        return self._client

    def close(self) -> None:
        if self._client:
            self._client.close()
            self._client = None

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make an HTTP request to the API."""
        client = self._get_client()
        try:
            response = client.request(method, endpoint, **kwargs)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {
                "error": f"HTTP {e.response.status_code}: {e.response.text}",
                "status_code": e.response.status_code
            }
        except httpx.RequestError as e:
            return {"error": f"Request failed: {str(e)}"}
        except json.JSONDecodeError:
            return {"error": "Invalid JSON response from server"}

    def search(self, query: str, limit: int = 10, filter_category: Optional[str] = None) -> Dict[str, Any]:
        """Search documentation."""
        params = {"q": query, "limit": limit}
        if filter_category:
            params["filter"] = filter_category
        return self._request("GET", "/search", params=params)

    def read_url(self, url: str, extract_code: bool = True, include_metadata: bool = False) -> Dict[str, Any]:
        """Read content from a URL."""
        return self._request("POST", "/read", json={
            "url": url,
            "extract_code": extract_code,
            "include_metadata": include_metadata
        })

    def check(self, filepath: str, strict: bool = False) -> Dict[str, Any]:
        """Check a file."""
        # Read file content
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except FileNotFoundError:
            return {"error": f"File not found: {filepath}"}
        except IOError as e:
            return {"error": f"Cannot read file: {e}"}

        return self._request("POST", "/check", json={
            "content": content,
            "filename": os.path.basename(filepath),
            "strict": strict
        })

    def analyze(
        self,
        path: str,
        recursive: bool = False,
        include: Optional[str] = None,
        exclude: Optional[str] = None
    ) -> Dict[str, Any]:
        """Analyze a path."""
        if not os.path.exists(path):
            return {"error": f"Path not found: {path}"}

        return self._request("POST", "/analyze", json={
            "path": os.path.abspath(path),
            "recursive": recursive,
            "include": include,
            "exclude": exclude
        })

    def get_info(self) -> Dict[str, Any]:
        """Get server info."""
        return self._request("GET", "/info")

    def get_version(self) -> Dict[str, Any]:
        """Get version."""
        return self._request("GET", "/version")


# ===== OUTPUT FORMATTING =====


def format_output(data: Any, format_type: str = "text") -> None:
    """Format and print output based on requested format."""
    if format_type == "json":
        try:
            console.print_json(json.dumps(data, indent=2, default=str))
        except (TypeError, ValueError) as e:
            console.print(f"[red]JSON serialization failed: {e}[/red]", file=sys.stderr)
            sys.exit(1)
    else:
        if isinstance(data, dict):
            if "error" in data:
                console.print(Panel(f"[red]{data['error']}[/red]", title="Error"))
            else:
                _format_dict(data)
        elif isinstance(data, list):
            _format_list(data)
        else:
            console.print(data)


def _format_dict(data: Dict[str, Any]) -> None:
    """Format a dictionary for text output."""
    table = Table(show_header=True, header_style="bold")
    table.add_column("Key", style="cyan")
    table.add_column("Value")

    for key, value in data.items():
        if isinstance(value, (dict, list)):
            value_str = json.dumps(value, indent=2, default=str)
        else:
            value_str = str(value)
        table.add_row(key, value_str)

    console.print(table)


def _format_list(data: List[Any]) -> None:
    """Format a list for text output."""
    for i, item in enumerate(data, 1):
        if isinstance(item, dict):
            console.print(f"\n[bold]Result {i}:[/bold]")
            _format_dict(item)
        else:
            console.print(f"  {i}. {item}")


# ===== CREDENTIAL VALIDATION =====


def validate_credentials() -> bool:
    """Validate required credentials are available."""
    if not REF_API_KEY:
        console.print(Panel(
            "[red]REF_API_KEY environment variable is not set.[/red]\n\n"
            "Set it with:\n"
            "  export REF_API_KEY='your-api-key'\n\n"
            "Or create a .env file:\n"
            "  REF_API_KEY=your-api-key",
            title="Missing API Key"
        ))
        return False
    return True


# ===== HELP DISPLAY FUNCTIONS =====


def show_help(format_type: str = "text") -> None:
    """Level 1: --help"""
    if format_type == "json":
        format_output({
            "title": "Ref Tools MCP CLI",
            "commands": ["list", "info", "example"],
            "functions": list(FUNCTION_INFO.keys())
        }, "json")
    else:
        console.print(QUICK_HELP)


def show_function_list(format_type: str = "text") -> None:
    """Level 2: list all functions"""
    if format_type == "json":
        format_output({
            "functions": [
                {"name": k, "description": v["description"]}
                for k, v in FUNCTION_INFO.items()
            ],
            "count": len(FUNCTION_INFO)
        }, "json")
    else:
        table = Table(title="Available Functions", show_header=True, header_style="bold")
        table.add_column("Function", style="cyan")
        table.add_column("Description")

        for name, info in FUNCTION_INFO.items():
            table.add_row(name, info["description"])

        console.print(table)
        console.print("\n[dim]Use 'uv run cli.py info FUNCTION' for detailed docs[/dim]")


def show_function_info(func_name: str, format_type: str = "text") -> None:
    """Level 2: info COMMAND"""
    if func_name not in FUNCTION_INFO:
        available = list(FUNCTION_INFO.keys())
        if format_type == "json":
            format_output({
                "error": f"Unknown function: {func_name}",
                "available_functions": available
            }, "json")
        else:
            console.print(f"[red]Error: Unknown function: {func_name}[/red]", file=sys.stderr)
            console.print(f"Available: {', '.join(available)}")
        sys.exit(1)

    info = FUNCTION_INFO[func_name]

    if format_type == "json":
        format_output(info, "json")
    else:
        console.print(Panel(
            f"[bold]{info.get('description', 'N/A')}[/bold]\n\n"
            f"{info.get('long_description', '')}",
            title=f"Function: {func_name}"
        ))

        if info.get('parameters'):
            table = Table(title="Parameters", show_header=True, header_style="bold")
            table.add_column("Name", style="cyan")
            table.add_column("Type")
            table.add_column("Required")
            table.add_column("Description")

            for param in info['parameters']:
                required = "Yes" if param.get('required') else "No"
                default = f" (default: {param.get('default')})" if 'default' in param else ""
                table.add_row(
                    f"--{param['name']}",
                    param.get('type', 'Any'),
                    required,
                    f"{param.get('description', '')}{default}"
                )

            console.print(table)

        if info.get('returns'):
            console.print(f"\n[bold]Returns:[/bold] {info['returns']}")

        if info.get('related'):
            console.print(f"\n[dim]Related: {', '.join(info['related'])}[/dim]")


def show_function_example(func_name: str, format_type: str = "text") -> None:
    """Level 3: example COMMAND"""
    if func_name not in FUNCTION_EXAMPLES:
        if format_type == "json":
            format_output({"error": f"No examples for: {func_name}"}, "json")
        else:
            console.print(f"[red]Error: No examples for: {func_name}[/red]", file=sys.stderr)
        sys.exit(1)

    examples = FUNCTION_EXAMPLES[func_name]

    if format_type == "json":
        format_output({
            "function": func_name,
            "examples": examples,
            "count": len(examples)
        }, "json")
    else:
        console.print(Panel(f"Examples for [bold]{func_name}[/bold]", title="Examples"))

        for i, example in enumerate(examples, 1):
            console.print(f"\n[bold]Example {i}: {example.get('title', 'Untitled')}[/bold]")
            if example.get('description'):
                console.print(f"  {example['description']}")
            console.print(f"\n  [cyan]$ {example.get('command', 'N/A')}[/cyan]\n")


# ===== FUNCTION EXECUTION =====


def execute_function(func_name: str, args: argparse.Namespace, format_type: str = "text") -> None:
    """Level 4: Execute the function."""
    if func_name not in FUNCTION_INFO:
        console.print(f"[red]Error: Unknown function: {func_name}[/red]", file=sys.stderr)
        sys.exit(1)

    # Config doesn't need API key validation
    if func_name == "config":
        masked_key = f"{REF_API_KEY[:4]}...{REF_API_KEY[-4:]}" if len(REF_API_KEY) > 8 else "***"
        result = {
            "api_key": masked_key if REF_API_KEY else "(not set)",
            "api_url": REF_API_URL,
            "timeout": DEFAULT_TIMEOUT
        }
        format_output(result, format_type)
        return

    # Other functions need validation
    if not validate_credentials():
        sys.exit(1)

    client = RefToolsClient(REF_API_KEY, REF_API_URL, DEFAULT_TIMEOUT)

    try:
        if func_name == "search":
            result = client.search(
                query=args.query,
                limit=getattr(args, 'limit', 10),
                filter_category=getattr(args, 'filter', None)
            )
        elif func_name == "read_url":
            result = client.read_url(
                url=args.url,
                extract_code=getattr(args, 'extract_code', True),
                include_metadata=getattr(args, 'include_metadata', False)
            )
        elif func_name == "check":
            result = client.check(
                filepath=args.filepath,
                strict=getattr(args, 'strict', False)
            )
        elif func_name == "analyze":
            result = client.analyze(
                path=args.path,
                recursive=getattr(args, 'recursive', False),
                include=getattr(args, 'include', None),
                exclude=getattr(args, 'exclude', None)
            )
        elif func_name == "info":
            result = client.get_info()
        elif func_name == "version":
            result = client.get_version()
        else:
            result = {"error": f"Function not implemented: {func_name}"}

        format_output(result, format_type)
    finally:
        client.close()


# ===== MAIN =====


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="ref",
        description="Ref Tools MCP CLI - Search and read technical documentation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=True,
        epilog="""
PROGRESSIVE HELP LEVELS:
  Level 1: --help              Quick overview
  Level 2: list                List all functions
           info FUNCTION       Full documentation
  Level 3: example FUNCTION    Working examples
  Level 4: FUNCTION [ARGS]     Execute function

EXAMPLES:
  uv run cli.py --help
  uv run cli.py list
  uv run cli.py info search
  uv run cli.py example search
  uv run cli.py search --query "async python"

ENVIRONMENT:
  REF_API_KEY                  API key (required)
  REF_API_URL                  API endpoint (default: https://api.ref.tools)
  REF_TIMEOUT                  Request timeout in seconds (default: 30)
        """
    )

    # Global options
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Level 2: list
    subparsers.add_parser("list", help="List all functions")

    # Level 2: info
    info_parser = subparsers.add_parser("info", help="Show function info")
    info_parser.add_argument("function", help="Function name")

    # Level 3: example
    example_parser = subparsers.add_parser("example", help="Show examples")
    example_parser.add_argument("function", help="Function name")

    # Level 4: Function subparsers

    # search
    search_parser = subparsers.add_parser("search", help="Search documentation")
    search_parser.add_argument("--query", "-q", required=True, help="Search query string")
    search_parser.add_argument("--limit", "-l", type=int, default=10, help="Max results (1-100)")
    search_parser.add_argument("--filter", "-f", help="Filter by category")

    # read_url
    read_parser = subparsers.add_parser("read_url", help="Read documentation URL")
    read_parser.add_argument("--url", "-u", required=True, help="URL to read")
    read_parser.add_argument("--extract-code", action="store_true", default=True, help="Extract code blocks")
    read_parser.add_argument("--include-metadata", action="store_true", help="Include page metadata")

    # check
    check_parser = subparsers.add_parser("check", help="Check a file")
    check_parser.add_argument("--filepath", "-f", required=True, help="File to check")
    check_parser.add_argument("--strict", action="store_true", help="Enable strict mode")

    # analyze
    analyze_parser = subparsers.add_parser("analyze", help="Analyze directory/file")
    analyze_parser.add_argument("--path", "-p", required=True, help="Path to analyze")
    analyze_parser.add_argument("--recursive", "-r", action="store_true", help="Recursive analysis")
    analyze_parser.add_argument("--include", "-i", help="Include pattern (e.g., '*.py')")
    analyze_parser.add_argument("--exclude", "-e", help="Exclude pattern")

    # info (server info)
    subparsers.add_parser("info_server", help="Show server information").set_defaults(func="info")

    # version
    subparsers.add_parser("version", help="Show version")

    # config
    subparsers.add_parser("config", help="Show configuration")

    args = parser.parse_args()

    # Route to correct handler
    try:
        if not args.command:
            show_help(args.format)
        elif args.command == "list":
            show_function_list(args.format)
        elif args.command == "info":
            show_function_info(args.function, args.format)
        elif args.command == "example":
            show_function_example(args.function, args.format)
        elif args.command in FUNCTION_INFO:
            execute_function(args.command, args, args.format)
        elif args.command == "info_server":
            execute_function("info", args, args.format)
        else:
            parser.print_help()
            sys.exit(1)
    except KeyboardInterrupt:
        console.print("\n[dim]Interrupted[/dim]", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        if args.verbose:
            import traceback
            traceback.print_exc()
        console.print(f"[red]Error: {e}[/red]", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
