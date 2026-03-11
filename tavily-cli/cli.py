#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "fastmcp>=2.0",
#     "httpx>=0.24.0",
#     "pydantic>=2.0",
#     "click>=8.0",
#     "rich>=13.0",
#     "python-dotenv>=1.0.0",
# ]
# ///
"""
CLI Wrapper for Tavily MCP Server
Production-ready wrapper with 4-level progressive disclosure.

Run with: uv run cli.py [COMMAND] [ARGS]

Levels:
  1. --help              Quick overview (~30 tokens)
  2. list / info TOOL    Detailed documentation (~150 tokens)
  3. example TOOL        Working examples (~200 tokens)
  4. TOOL --help         Complete reference (~500 tokens)

MCP Server: npx tavily-mcp@latest (stdio transport)
"""

import argparse
import asyncio
import json
import os
import sys
from enum import Enum
from typing import Any

from dotenv import load_dotenv
from fastmcp import Client

# Load environment variables from script directory (.env first, then .env.local overrides)
_script_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(_script_dir, ".env"))
load_dotenv(os.path.join(_script_dir, ".env.local"), override=True)
from fastmcp.client.transports import NpxStdioTransport


# ===== DETAIL LEVEL ENUM =====

class DetailLevel(str, Enum):
    """Control response verbosity for token optimization."""
    MINIMAL = "minimal"    # URL and success status only
    STANDARD = "standard"  # URL, success, content preview (first 500 chars)
    FULL = "full"          # Complete content


# ===== MCP CLIENT CONFIGURATION =====

TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY", "")

_transport = NpxStdioTransport(
    package="tavily-mcp@latest",
    args=[],
    env_vars={
        "TAVILY_API_KEY": TAVILY_API_KEY,
    },
)


def get_client():
    """Get MCP client for Tavily npx transport."""
    return Client(_transport)


# ===== MCP TOOL NAME MAPPING =====
# CLI command -> actual MCP tool name
TOOL_MAPPING = {
    "search": "tavily-search",
    "extract": "tavily-extract",
    "map": "tavily-map",
    "crawl": "tavily-crawl",
}


# ===== LEVEL 1: QUICK HELP =====

QUICK_HELP = """Tavily MCP - AI-Powered Web Search & Extraction

Functions:
  search    Real-time web search with AI ranking
  extract   Extract structured data from web pages
  map       Create structured sitemap of a website
  crawl     Systematically crawl and explore websites

Use:
  uv run cli.py list
  uv run cli.py info FUNCTION
  uv run cli.py example FUNCTION
  uv run cli.py FUNCTION [ARGS]

Options:
  --format json|text   Output format (default: text)
  --detail LEVEL       Response detail: minimal|standard|full (default: full)

Environment:
  TAVILY_API_KEY       Your Tavily API key (required)
                       Get one at https://tavily.com
"""


# ===== LEVEL 2: FUNCTION INFO =====

FUNCTION_INFO = {
    "search": {
        "mcp_tool": "tavily-search",
        "description": "Real-time web search with AI-powered ranking and relevance scoring",
        "parameters": [
            {
                "name": "query",
                "type": "str",
                "required": True,
                "description": "Search query string"
            },
            {
                "name": "search-depth",
                "type": "str",
                "required": False,
                "default": "basic",
                "description": "Search depth: 'basic' (fast) or 'advanced' (thorough)"
            },
            {
                "name": "max-results",
                "type": "int",
                "required": False,
                "default": 5,
                "description": "Maximum number of results to return (1-20)"
            },
            {
                "name": "include-images",
                "type": "bool",
                "required": False,
                "default": False,
                "description": "Include image results"
            },
            {
                "name": "include-answer",
                "type": "bool",
                "required": False,
                "default": True,
                "description": "Include AI-generated answer summary"
            }
        ],
        "returns": "Dict with 'results' array of {title, url, content, score} and optional 'answer'",
        "timeout": "30 seconds",
        "related": ["extract", "crawl"]
    },
    "extract": {
        "mcp_tool": "tavily-extract",
        "description": "Extract structured data and content from web pages using AI",
        "parameters": [
            {
                "name": "urls",
                "type": "str",
                "required": True,
                "description": "URL(s) to extract from (comma-separated for multiple)"
            }
        ],
        "returns": "Dict with extracted content, metadata, and structured data",
        "timeout": "60 seconds",
        "related": ["search", "crawl"]
    },
    "map": {
        "mcp_tool": "tavily-map",
        "description": "Create a structured sitemap of a website, discovering all accessible pages",
        "parameters": [
            {
                "name": "url",
                "type": "str",
                "required": True,
                "description": "Base URL of the website to map"
            }
        ],
        "returns": "Dict with 'pages' array containing discovered URLs and structure",
        "timeout": "120 seconds",
        "related": ["crawl", "extract"]
    },
    "crawl": {
        "mcp_tool": "tavily-crawl",
        "description": "Systematically crawl a website, following links and extracting content",
        "parameters": [
            {
                "name": "url",
                "type": "str",
                "required": True,
                "description": "Starting URL for the crawl"
            },
            {
                "name": "max-depth",
                "type": "int",
                "required": False,
                "default": 2,
                "description": "Maximum depth to crawl from starting URL"
            },
            {
                "name": "max-pages",
                "type": "int",
                "required": False,
                "default": 10,
                "description": "Maximum number of pages to crawl"
            }
        ],
        "returns": "Dict with 'pages' array of {url, content, links, metadata}",
        "timeout": "300 seconds (5 minutes)",
        "related": ["map", "extract", "search"]
    }
}


# ===== LEVEL 3: EXAMPLES =====

FUNCTION_EXAMPLES = {
    "search": [
        {
            "title": "Basic web search",
            "command": 'uv run cli.py search --query "Python async best practices"',
            "output": '{"results": [{"title": "...", "url": "...", "content": "...", "score": 0.95}], "answer": "..."}'
        },
        {
            "title": "Advanced search with more results",
            "command": 'uv run cli.py search --query "machine learning frameworks 2024" --search-depth advanced --max-results 10',
            "output": '{"results": [...], "answer": "Based on the search results..."}'
        },
        {
            "title": "Search with images",
            "command": 'uv run cli.py search --query "data visualization examples" --include-images',
            "output": '{"results": [...], "images": [{"url": "...", "description": "..."}]}'
        },
        {
            "title": "JSON output with jq filtering",
            "command": 'uv run cli.py search --query "API design" --format json | jq \'.results[] | {title, url}\'',
        }
    ],
    "extract": [
        {
            "title": "Extract from single URL",
            "command": "uv run cli.py extract --urls https://example.com/article",
            "output": '{"content": "...", "metadata": {"title": "...", "author": "..."}}'
        },
        {
            "title": "Extract from multiple URLs",
            "command": "uv run cli.py extract --urls 'https://site1.com,https://site2.com'",
            "output": '{"results": [{"url": "...", "content": "..."}, ...]}'
        },
        {
            "title": "Extract and save to file",
            "command": "uv run cli.py extract --urls https://docs.example.com --format json > extracted.json",
        }
    ],
    "map": [
        {
            "title": "Map a website structure",
            "command": "uv run cli.py map --url https://docs.python.org",
            "output": '{"pages": [{"url": "...", "title": "..."}, ...]}'
        },
        {
            "title": "Map and extract URLs only",
            "command": "uv run cli.py map --url https://example.com --format json | jq '.pages[].url'",
        }
    ],
    "crawl": [
        {
            "title": "Basic crawl",
            "command": "uv run cli.py crawl --url https://blog.example.com",
            "output": '{"pages": [{"url": "...", "content": "...", "links": [...]}]}'
        },
        {
            "title": "Deep crawl with limits",
            "command": "uv run cli.py crawl --url https://docs.example.com --max-depth 3 --max-pages 20",
        },
        {
            "title": "Crawl with minimal output",
            "command": "uv run cli.py crawl --url https://example.com --detail minimal",
            "output": '{"pages": [{"url": "...", "success": true}]}'
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
        # Strip content, keep only URLs and success status
        if "results" in data:
            return {
                "results": [
                    {"url": r.get("url"), "title": r.get("title", ""), "score": r.get("score")}
                    for r in data.get("results", [])
                ],
                "count": len(data.get("results", []))
            }
        if "pages" in data:
            return {
                "pages": [
                    {"url": p.get("url"), "success": True}
                    for p in data.get("pages", [])
                ],
                "count": len(data.get("pages", []))
            }
        if "content" in data:
            return {"success": True, "content_length": len(str(data.get("content", "")))}
        if "error" in data:
            return {"success": False, "error": data["error"]}
        return data

    if level == DetailLevel.STANDARD:
        # Truncate content to first 500 chars
        if "results" in data:
            return {
                "results": [
                    {
                        "url": r.get("url"),
                        "title": r.get("title", ""),
                        "content_preview": (r.get("content", "")[:500] + "...")
                        if r.get("content") and len(r.get("content", "")) > 500
                        else r.get("content", ""),
                        "score": r.get("score")
                    }
                    for r in data.get("results", [])
                ],
                "answer": data.get("answer"),
                "count": len(data.get("results", []))
            }
        if "pages" in data:
            return {
                "pages": [
                    {
                        "url": p.get("url"),
                        "title": p.get("title", ""),
                        "content_preview": (p.get("content", "")[:500] + "...")
                        if p.get("content") and len(p.get("content", "")) > 500
                        else p.get("content", "")
                    }
                    for p in data.get("pages", [])
                ],
                "count": len(data.get("pages", []))
            }
        if "content" in data:
            content = str(data.get("content", ""))
            return {
                "content_preview": content[:500] + "..." if len(content) > 500 else content,
                "full_length": len(content),
                "metadata": data.get("metadata")
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
    if not url.startswith("http://") and not url.startswith("https://"):
        return f"https://{url}"
    return url


def validate_credentials() -> bool:
    """Check if TAVILY_API_KEY is set."""
    if not TAVILY_API_KEY:
        print("Error: TAVILY_API_KEY environment variable is not set.", file=sys.stderr)
        print("Get your API key at https://tavily.com", file=sys.stderr)
        print("Then: export TAVILY_API_KEY='your-key'", file=sys.stderr)
        return False
    return True


def show_help(format_type: str = "text"):
    """Level 1: --help"""
    if format_type == "json":
        format_output({
            "title": "Tavily MCP",
            "description": "AI-powered web search and extraction",
            "commands": ["list", "info", "example"],
            "functions": list(FUNCTION_INFO.keys()),
            "api_key_required": True,
            "api_key_url": "https://tavily.com"
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

    # Validate credentials
    if not validate_credentials():
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
                    # Validate URL parameters
                    if param_name in ["url", "urls"]:
                        if param_name == "urls":
                            # Handle comma-separated URLs
                            urls = [u.strip() for u in value.split(',')]
                            validated_urls = []
                            for u in urls:
                                normalized = validate_url(u)
                                if not normalized:
                                    print(f"Error: Invalid URL format: {u}", file=sys.stderr)
                                    sys.exit(1)
                                validated_urls.append(normalized)
                            value = validated_urls
                        else:
                            normalized = validate_url(value)
                            if not normalized:
                                print(f"Error: Invalid URL format: {value}", file=sys.stderr)
                                sys.exit(1)
                            value = normalized
                    # Map parameter names for MCP
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
        prog="tavily",
        description="Tavily MCP CLI - AI-Powered Web Search & Extraction",
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
  uv run cli.py --help
  uv run cli.py list
  uv run cli.py info search
  uv run cli.py example search
  uv run cli.py search --query "Python best practices"
  uv run cli.py extract --urls https://example.com
  uv run cli.py map --url https://docs.example.com
  uv run cli.py crawl --url https://blog.example.com --max-depth 2

DETAIL LEVELS (for token optimization):
  --detail minimal    URLs and status only (~50 tokens/result)
  --detail standard   Content preview, first 500 chars (~150 tokens/result)
  --detail full       Complete content (default, varies by response)

OUTPUT FORMATS:
  --format text       Human-readable (default)
  --format json       Machine-readable (pipe to jq for filtering)

ENVIRONMENT:
  TAVILY_API_KEY      Your Tavily API key (required)
                      Get one at https://tavily.com
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
    info_parser.add_argument("function", help="Function name")

    # Level 3: example
    example_parser = subparsers.add_parser("example", help="Show working examples")
    example_parser.add_argument("function", help="Function name")

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

                    # Handle boolean flags
                    if param_type == 'bool':
                        func_parser.add_argument(
                            f"--{param_name}",
                            action="store_true",
                            help=param.get('description', ''),
                            default=param.get('default', False),
                        )
                    else:
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
        if not validate_credentials():
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
