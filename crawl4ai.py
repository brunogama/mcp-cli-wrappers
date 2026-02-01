#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "fastmcp>=2.0",
#     "httpx>=0.24.0",
#     "pydantic>=2.0",
#     "click>=8.0",
#     "rich>=13.0",
# ]
# ///
"""
CLI Wrapper for Crawl4AI MCP Server
Production-ready wrapper with 4-level progressive disclosure.

Run with: uv run crawl4ai.py [COMMAND] [ARGS]

Levels:
  1. --help              Quick overview (~30 tokens)
  2. list / info TOOL    Detailed documentation (~150 tokens)
  3. example TOOL        Working examples (~200 tokens)
  4. TOOL --help         Complete reference (~500 tokens)

MCP Server: ~/Developer/crawl4ai-mcp (stdio transport)
"""

import argparse
import asyncio
import json
import os
import sys
from enum import Enum
from typing import Any

from fastmcp import Client


# ===== DETAIL LEVEL ENUM =====

class DetailLevel(str, Enum):
    """Control response verbosity for token optimization."""
    MINIMAL = "minimal"    # URL and success status only
    STANDARD = "standard"  # URL, success, markdown preview (first 500 chars)
    FULL = "full"          # Complete markdown content


# ===== MCP CLIENT CONFIGURATION =====

# Crawl4AI runs as stdio transport, not HTTP
MCP_SERVER_DIR = os.environ.get(
    "CRAWL4AI_MCP_DIR",
    os.path.expanduser("~/Developer/crawl4ai-mcp")
)


def get_client():
    """Get MCP client for Crawl4AI stdio transport."""
    # FastMCP Client can accept a command list for stdio transport
    return Client(["uv", "--directory", MCP_SERVER_DIR, "run", "main.py"])


# ===== MCP TOOL NAME MAPPING =====
# CLI command -> actual MCP tool name
TOOL_MAPPING = {
    "scrape": "scrape_webpage",
    "crawl": "crawl_website",
}


# ===== LEVEL 1: QUICK HELP =====

QUICK_HELP = """Crawl4AI MCP - Web scraping and crawling

Functions:
  scrape    Scrape content from a single webpage
  crawl     Crawl multiple pages with depth control

Use:
  uv run crawl4ai.py list
  uv run crawl4ai.py info FUNCTION
  uv run crawl4ai.py example FUNCTION
  uv run crawl4ai.py FUNCTION [ARGS]

Options:
  --format json|text   Output format (default: text)
  --detail LEVEL       Response detail: minimal|standard|full (default: full)

Environment:
  CRAWL4AI_MCP_DIR     Path to crawl4ai-mcp server (default: ~/Developer/crawl4ai-mcp)
"""


# ===== LEVEL 2: FUNCTION INFO =====

FUNCTION_INFO = {
    "scrape": {
        "mcp_tool": "scrape_webpage",
        "description": "Scrape content and metadata from a single webpage using Crawl4AI",
        "parameters": [
            {
                "name": "url",
                "type": "str",
                "required": True,
                "description": "The URL of the webpage to scrape (https:// added if missing)"
            }
        ],
        "returns": "Dict with 'markdown' (str) on success, or 'error' (str) on failure",
        "timeout": "30 seconds per page",
        "related": ["crawl"]
    },
    "crawl": {
        "mcp_tool": "crawl_website",
        "description": "Crawl a website starting from URL up to specified depth and page limit",
        "parameters": [
            {
                "name": "url",
                "type": "str",
                "required": True,
                "description": "The starting URL to crawl (https:// added if missing)"
            },
            {
                "name": "crawl-depth",
                "type": "int",
                "required": False,
                "default": 1,
                "description": "Maximum depth to crawl relative to starting URL"
            },
            {
                "name": "max-pages",
                "type": "int",
                "required": False,
                "default": 5,
                "description": "Maximum number of pages to scrape during crawl"
            }
        ],
        "returns": "Dict with 'results' array of {url, success, markdown|error}",
        "timeout": "300 seconds (5 minutes) for entire crawl operation",
        "related": ["scrape"]
    }
}


# ===== LEVEL 3: EXAMPLES =====

FUNCTION_EXAMPLES = {
    "scrape": [
        {
            "title": "Basic webpage scrape",
            "command": "uv run crawl4ai.py scrape --url https://example.com",
            "output": '{"markdown": "# Example Domain\\n\\nThis domain is for use..."}'
        },
        {
            "title": "Scrape documentation page",
            "command": "uv run crawl4ai.py scrape --url https://docs.python.org/3/",
            "output": '{"markdown": "# Python 3 Documentation..."}'
        },
        {
            "title": "JSON output with jq filtering",
            "command": "uv run crawl4ai.py scrape --url https://httpbin.org/html --format json | jq '.markdown[:200]'"
        },
        {
            "title": "Minimal detail (URL validation only)",
            "command": "uv run crawl4ai.py scrape --url https://example.com --detail minimal"
        }
    ],
    "crawl": [
        {
            "title": "Default shallow crawl (depth=1, max=5 pages)",
            "command": "uv run crawl4ai.py crawl --url https://example.com",
            "output": '{"results": [{"url": "https://example.com", "success": true, "markdown": "..."}]}'
        },
        {
            "title": "Deep crawl with custom limits",
            "command": "uv run crawl4ai.py crawl --url https://docs.example.com --crawl-depth 2 --max-pages 10"
        },
        {
            "title": "Filter successful results with jq",
            "command": "uv run crawl4ai.py crawl --url https://blog.example.com --format json | jq '.results[] | select(.success) | .url'"
        },
        {
            "title": "Standard detail (preview only)",
            "command": "uv run crawl4ai.py crawl --url https://example.com --detail standard"
        }
    ]
}


# ===== MCP TOOL CALLING =====

async def call_mcp_tool(tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    """Call an MCP tool and return the result."""
    async with get_client() as client:
        try:
            result = await client.call_tool(tool_name, arguments)
            # Handle different result formats
            if hasattr(result, 'data') and result.data is not None:
                return result.data
            elif hasattr(result, 'content'):
                # Parse content if it's a list of content blocks
                if isinstance(result.content, list):
                    text_content = []
                    for block in result.content:
                        if hasattr(block, 'text'):
                            text_content.append(block.text)
                        elif isinstance(block, dict) and 'text' in block:
                            text_content.append(block['text'])
                    combined = '\n'.join(text_content)
                    # Try to parse as JSON
                    try:
                        return json.loads(combined)
                    except json.JSONDecodeError:
                        return {"result": combined}
                return {"content": result.content}
            else:
                return {"result": str(result)}
        except Exception as e:
            return {"error": str(e), "tool": tool_name, "arguments": arguments}


async def list_mcp_tools() -> list:
    """Discover available tools from the MCP server."""
    async with get_client() as client:
        tools = await client.list_tools()
        return [{"name": t.name, "description": t.description} for t in tools]


def run_tool(tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    """Synchronous wrapper for calling MCP tools."""
    return asyncio.run(call_mcp_tool(tool_name, arguments))


def discover_tools() -> list:
    """Synchronous wrapper for discovering MCP tools."""
    return asyncio.run(list_mcp_tools())


# ===== DETAIL LEVEL PROCESSING =====

def apply_detail_level(data: dict[str, Any], level: str) -> dict[str, Any]:
    """Apply detail level filtering to response data."""
    if level == DetailLevel.FULL:
        return data

    if level == DetailLevel.MINIMAL:
        # Strip markdown content, keep only status
        if "markdown" in data:
            return {"success": True, "url": data.get("url", "N/A")}
        if "results" in data:
            return {
                "results": [
                    {"url": r.get("url"), "success": r.get("success", False)}
                    for r in data.get("results", [])
                ],
                "count": len(data.get("results", []))
            }
        if "error" in data:
            return {"success": False, "error": data["error"]}
        return data

    if level == DetailLevel.STANDARD:
        # Truncate markdown to first 500 chars
        if "markdown" in data:
            md = data["markdown"]
            preview = md[:500] + "..." if len(md) > 500 else md
            return {"success": True, "markdown_preview": preview, "full_length": len(md)}
        if "results" in data:
            return {
                "results": [
                    {
                        "url": r.get("url"),
                        "success": r.get("success", False),
                        "markdown_preview": (r.get("markdown", "")[:500] + "...")
                        if r.get("markdown") and len(r.get("markdown", "")) > 500
                        else r.get("markdown", r.get("error", ""))
                    }
                    for r in data.get("results", [])
                ],
                "count": len(data.get("results", []))
            }
        return data

    return data


# ===== UTILITIES =====

def format_output(data: Any, format_type: str = "text") -> None:
    """Format and print output based on requested format."""
    if format_type == "json":
        try:
            print(json.dumps(data, indent=2, default=str, ensure_ascii=False))
        except (TypeError, ValueError) as e:
            print(json.dumps({"error": f"JSON serialization failed: {e!s}"}, indent=2), file=sys.stderr)
            sys.exit(1)
    else:  # text format
        if isinstance(data, dict):
            if "error" in data:
                print(f"Error: {data['error']}", file=sys.stderr)
            else:
                for key, value in data.items():
                    if isinstance(value, (dict, list)):
                        print(f"{key}:")
                        print(json.dumps(value, indent=2, default=str, ensure_ascii=False))
                    else:
                        print(f"{key}: {value}")
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    print(json.dumps(item, indent=2, default=str, ensure_ascii=False))
                else:
                    print(f"  - {item}")
        else:
            print(data)


def validate_url(url: str) -> str | None:
    """Validate and normalize URL. Returns normalized URL or None if invalid."""
    import re
    # Allow domains, subdomains, IPs, localhost with optional paths
    url_pattern = re.compile(
        r"^(?:https?://)?(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"
        r"localhost|"
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
        r"(?::\d+)?"
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )
    if not url_pattern.match(url):
        return None
    # Add https:// if missing
    if not url.startswith("http://") and not url.startswith("https://"):
        return f"https://{url}"
    return url


def validate_mcp_server() -> bool:
    """Check if MCP server directory exists."""
    if not os.path.isdir(MCP_SERVER_DIR):
        print(f"Error: Crawl4AI MCP server not found at: {MCP_SERVER_DIR}", file=sys.stderr)
        print("Set CRAWL4AI_MCP_DIR environment variable to correct path.", file=sys.stderr)
        return False
    main_py = os.path.join(MCP_SERVER_DIR, "main.py")
    if not os.path.isfile(main_py):
        print(f"Error: main.py not found in {MCP_SERVER_DIR}", file=sys.stderr)
        return False
    return True


def show_help(format_type: str = "text"):
    """Level 1: --help"""
    if format_type == "json":
        format_output({
            "title": "Crawl4AI MCP",
            "description": "Web scraping and crawling via Crawl4AI",
            "commands": ["list", "info", "example"],
            "functions": list(FUNCTION_INFO.keys()),
            "mcp_server": MCP_SERVER_DIR
        }, "json")
    else:
        print(QUICK_HELP)


def show_function_list(format_type: str = "text"):
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
        print(QUICK_HELP)


def show_function_info(func_name: str, format_type: str = "text"):
    """Level 2: info COMMAND"""
    if func_name not in FUNCTION_INFO:
        error_msg = f"Unknown function: {func_name}"
        available = list(FUNCTION_INFO.keys())
        if format_type == "json":
            format_output({
                "error": error_msg,
                "available_functions": available
            }, "json")
        else:
            print(f"Error: {error_msg}", file=sys.stderr)
            print(f"Available: {', '.join(available)}")
        sys.exit(1)

    info = FUNCTION_INFO[func_name]

    if format_type == "json":
        format_output(info, "json")
    else:
        print(f"\n{'='*60}")
        print(f"Function: {func_name}")
        print(f"{'='*60}")
        print(f"Description: {info.get('description', 'N/A')}")
        print(f"MCP Tool: {info.get('mcp_tool', func_name)}")

        if info.get('parameters'):
            print("\nParameters:")
            for param in info['parameters']:
                param_name = param.get('name', 'unknown')
                param_type = param.get('type', 'Any')
                required = "required" if param.get('required') else "optional"
                default = f", default: {param['default']}" if 'default' in param else ""
                desc = param.get('description', '')
                print(f"  --{param_name:20} ({param_type}, {required}{default})")
                if desc:
                    print(f"      {desc}")

        if info.get('returns'):
            print(f"\nReturns: {info['returns']}")
        if info.get('timeout'):
            print(f"Timeout: {info['timeout']}")
        if info.get('related'):
            print(f"Related: {', '.join(info['related'])}")
        print()


def show_function_example(func_name: str, format_type: str = "text"):
    """Level 3: example COMMAND"""
    if func_name not in FUNCTION_EXAMPLES:
        error_msg = f"No examples for: {func_name}"
        if format_type == "json":
            format_output({"error": error_msg}, "json")
        else:
            print(f"Error: {error_msg}", file=sys.stderr)
        sys.exit(1)

    examples = FUNCTION_EXAMPLES[func_name]

    if format_type == "json":
        format_output({
            "function": func_name,
            "examples": examples,
            "count": len(examples)
        }, "json")
    else:
        print(f"\n{'='*60}")
        print(f"Examples for: {func_name}")
        print(f"{'='*60}\n")
        for i, example in enumerate(examples, 1):
            print(f"Example {i}: {example.get('title', 'Untitled')}")
            print(f"  Command: {example.get('command', 'N/A')}")
            if example.get('output'):
                print(f"  Output: {example['output']}")
            print()


def execute_function(func_name: str, args: argparse.Namespace, format_type: str = "text"):
    """Level 4: Execute the function via MCP tool call."""
    if func_name not in FUNCTION_INFO:
        print(f"Error: Unknown function: {func_name}", file=sys.stderr)
        sys.exit(1)

    # Validate MCP server exists
    if not validate_mcp_server():
        sys.exit(1)

    # Build arguments dict from parsed args
    func_info = FUNCTION_INFO[func_name]
    arguments: dict[str, Any] = {}

    if func_info.get('parameters'):
        for param in func_info['parameters']:
            param_name = param.get('name', '')
            if param_name:
                # Get value from args (argparse converts - to _)
                arg_name = param_name.replace('-', '_')
                value = getattr(args, arg_name, None)
                if value is not None:
                    # Validate URL parameter
                    if param_name == "url":
                        normalized = validate_url(value)
                        if not normalized:
                            print(f"Error: Invalid URL format: {value}", file=sys.stderr)
                            sys.exit(1)
                        value = normalized
                    # Map parameter names for MCP (crawl-depth -> crawl_depth)
                    mcp_param_name = param_name.replace('-', '_')
                    arguments[mcp_param_name] = value
                elif param.get('required'):
                    print(f"Error: Missing required argument: --{param_name}", file=sys.stderr)
                    sys.exit(1)

    # Get actual MCP tool name
    mcp_tool_name = TOOL_MAPPING.get(func_name, func_name)

    # Call the MCP tool
    try:
        result = run_tool(mcp_tool_name, arguments)
    except Exception as e:
        print(f"Error calling MCP tool: {e}", file=sys.stderr)
        sys.exit(1)

    # Apply detail level filtering
    detail_level = getattr(args, 'detail', DetailLevel.FULL)
    result = apply_detail_level(result, detail_level)

    format_output(result, format_type)


def main():
    parser = argparse.ArgumentParser(
        prog="crawl4ai",
        description="Crawl4AI MCP CLI Wrapper - Web scraping and crawling",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=True,
        epilog="""
PROGRESSIVE HELP LEVELS:
  Level 1: --help                    Quick overview (~30 tokens)
  Level 2: list                      List all functions
           info FUNCTION             Full documentation (~150 tokens)
  Level 3: example FUNCTION          Working examples (~200 tokens)
  Level 4: FUNCTION [ARGS]           Execute function via MCP

EXAMPLES:
  uv run crawl4ai.py --help
  uv run crawl4ai.py list
  uv run crawl4ai.py info scrape
  uv run crawl4ai.py example crawl
  uv run crawl4ai.py scrape --url https://example.com
  uv run crawl4ai.py crawl --url https://docs.python.org --crawl-depth 2 --max-pages 10

DETAIL LEVELS (for token optimization):
  --detail minimal    URL and success status only (~50 tokens/page)
  --detail standard   Preview of content, first 500 chars (~150 tokens/page)
  --detail full       Complete content (default, varies by page size)

OUTPUT FORMATS:
  --format text       Human-readable (default)
  --format json       Machine-readable (pipe to jq for filtering)

ENVIRONMENT:
  CRAWL4AI_MCP_DIR    Path to crawl4ai-mcp server directory
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
        "--detail",
        choices=["minimal", "standard", "full"],
        default="full",
        help="Response detail level for token optimization (default: full)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output with stack traces"
    )
    parser.add_argument(
        "--discover",
        action="store_true",
        help="Discover tools from MCP server (live introspection)"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Level 2: list
    subparsers.add_parser("list", help="List all available functions")

    # Level 2: info
    info_parser = subparsers.add_parser("info", help="Show detailed function documentation")
    info_parser.add_argument("function", help="Function name (scrape or crawl)")

    # Level 3: example
    example_parser = subparsers.add_parser("example", help="Show working examples")
    example_parser.add_argument("function", help="Function name (scrape or crawl)")

    # Level 4: Dynamic function subparsers (actual execution)
    for func_name, func_info in FUNCTION_INFO.items():
        func_parser = subparsers.add_parser(
            func_name,
            help=func_info.get('description', ''),
            add_help=True
        )
        # Add function-specific arguments from FUNCTION_INFO
        if func_info.get('parameters'):
            for param in func_info['parameters']:
                param_name = param.get('name', '')
                if param_name:
                    param_type = param.get('type', 'str')
                    # Convert type string to actual type
                    type_map = {'str': str, 'int': int, 'float': float, 'bool': bool}
                    arg_type = type_map.get(param_type, str)

                    func_parser.add_argument(
                        f"--{param_name}",
                        type=arg_type,
                        help=param.get('description', ''),
                        required=param.get('required', False),
                        default=param.get('default'),
                    )

    args = parser.parse_args()

    # Handle --discover flag
    if args.discover:
        if not validate_mcp_server():
            sys.exit(1)
        try:
            tools = discover_tools()
            format_output({"tools": tools, "count": len(tools)}, args.format)
        except Exception as e:
            if args.verbose:
                import traceback
                traceback.print_exc()
            print(f"Error discovering tools: {e}", file=sys.stderr)
            sys.exit(1)
        return

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
            # Level 4: Execute the function via MCP
            execute_function(args.command, args, args.format)
        else:
            parser.print_help()
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nInterrupted", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        if args.verbose:
            import traceback
            traceback.print_exc()
        print(f"Error: {e!s}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
