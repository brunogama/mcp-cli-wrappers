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
Firecrawl CLI - Web Scraping and Crawling Tool

A production-ready CLI wrapper for the Firecrawl MCP server with
4-level progressive disclosure help system.

Run with: uv run cli.py [COMMAND] [ARGS]

Help Levels:
  1. --help              Quick overview (~30 tokens)
  2. list / info TOOL    Detailed documentation (~150 tokens)
  3. example TOOL        Working examples (~200 tokens)
  4. TOOL --help         Complete reference (~500 tokens)
"""

import argparse
import asyncio
import json
import os
import sys
from typing import Any

from fastmcp import Client
from fastmcp.client.transports import NpxStdioTransport

# ===== MCP CLIENT CONFIGURATION =====

NPX_PACKAGE = "@anthropics/firecrawl-mcp"
NPX_ARGS: list[str] = []

_transport = NpxStdioTransport(
    package=NPX_PACKAGE,
    args=NPX_ARGS,
    env_vars={
        "FIRECRAWL_API_KEY": os.environ.get("FIRECRAWL_API_KEY", ""),
    },
)


def get_client() -> Client:
    """Get MCP client for Firecrawl transport."""
    return Client(_transport)


# ===== LEVEL 1: QUICK HELP =====

QUICK_HELP = """Firecrawl CLI - Web Scraping & Crawling

Available commands:
  scrape      Scrape a single webpage and extract content
  crawl       Crawl an entire website recursively
  extract     Extract structured data using LLM
  map         Discover all URLs on a website
  search      Search the web for content

Quick start:
  uv run cli.py scrape --url https://example.com
  uv run cli.py crawl --url https://docs.example.com --limit 10
  uv run cli.py search --query "machine learning tutorials"

Help system (4 levels):
  uv run cli.py --help              # This overview
  uv run cli.py list                # All functions
  uv run cli.py info scrape         # Detailed docs
  uv run cli.py example scrape      # Working examples
  uv run cli.py scrape --help       # Complete reference

Environment:
  FIRECRAWL_API_KEY    Required. Get from https://firecrawl.dev
"""

# ===== LEVEL 2: FUNCTION INFO =====

FUNCTION_INFO = {
    "scrape": {
        "description": "Scrape a single webpage and extract its content",
        "parameters": [
            {
                "name": "url",
                "type": "string",
                "required": True,
                "description": "The URL of the webpage to scrape"
            },
            {
                "name": "formats",
                "type": "list[string]",
                "required": False,
                "description": "Output formats: markdown, html, rawHtml, links, screenshot",
                "default": "['markdown']"
            },
            {
                "name": "only-main-content",
                "type": "boolean",
                "required": False,
                "description": "Extract only the main content, removing navigation/ads",
                "default": "true"
            },
            {
                "name": "include-tags",
                "type": "list[string]",
                "required": False,
                "description": "HTML tags to include (e.g., article, main)"
            },
            {
                "name": "exclude-tags",
                "type": "list[string]",
                "required": False,
                "description": "HTML tags to exclude (e.g., nav, footer)"
            },
            {
                "name": "wait-for",
                "type": "integer",
                "required": False,
                "description": "Milliseconds to wait for dynamic content"
            }
        ],
        "returns": "Dict with markdown content, metadata, and optional formats"
    },
    "crawl": {
        "description": "Crawl an entire website recursively following links",
        "parameters": [
            {
                "name": "url",
                "type": "string",
                "required": True,
                "description": "The starting URL to crawl from"
            },
            {
                "name": "limit",
                "type": "integer",
                "required": False,
                "description": "Maximum number of pages to crawl",
                "default": "10"
            },
            {
                "name": "max-depth",
                "type": "integer",
                "required": False,
                "description": "Maximum crawl depth from starting URL",
                "default": "3"
            },
            {
                "name": "include-paths",
                "type": "list[string]",
                "required": False,
                "description": "URL paths to include (e.g., /docs/, /blog/)"
            },
            {
                "name": "exclude-paths",
                "type": "list[string]",
                "required": False,
                "description": "URL paths to exclude (e.g., /admin/, /login/)"
            },
            {
                "name": "allow-external",
                "type": "boolean",
                "required": False,
                "description": "Allow crawling external domains",
                "default": "false"
            }
        ],
        "returns": "Dict with list of crawled pages, each containing content and metadata"
    },
    "extract": {
        "description": "Extract structured data from a webpage using LLM",
        "parameters": [
            {
                "name": "url",
                "type": "string",
                "required": True,
                "description": "The URL to extract data from"
            },
            {
                "name": "schema",
                "type": "object",
                "required": True,
                "description": "JSON schema defining the structure to extract"
            },
            {
                "name": "prompt",
                "type": "string",
                "required": False,
                "description": "Additional extraction instructions for the LLM"
            }
        ],
        "returns": "Dict with structured data matching the provided schema"
    },
    "map": {
        "description": "Discover and list all URLs on a website",
        "parameters": [
            {
                "name": "url",
                "type": "string",
                "required": True,
                "description": "The website URL to map"
            },
            {
                "name": "search",
                "type": "string",
                "required": False,
                "description": "Filter URLs containing this search term"
            },
            {
                "name": "limit",
                "type": "integer",
                "required": False,
                "description": "Maximum number of URLs to return",
                "default": "100"
            }
        ],
        "returns": "Dict with list of discovered URLs"
    },
    "search": {
        "description": "Search the web and return relevant results",
        "parameters": [
            {
                "name": "query",
                "type": "string",
                "required": True,
                "description": "The search query"
            },
            {
                "name": "limit",
                "type": "integer",
                "required": False,
                "description": "Maximum number of results to return",
                "default": "10"
            },
            {
                "name": "lang",
                "type": "string",
                "required": False,
                "description": "Language code for results (e.g., en, es, fr)"
            },
            {
                "name": "country",
                "type": "string",
                "required": False,
                "description": "Country code for regional results (e.g., us, uk)"
            }
        ],
        "returns": "Dict with search results containing titles, URLs, and snippets"
    }
}

# ===== LEVEL 3: EXAMPLES =====

FUNCTION_EXAMPLES = {
    "scrape": [
        {
            "title": "Basic scrape",
            "command": "uv run cli.py scrape --url https://example.com",
            "description": "Scrape a webpage and get markdown content"
        },
        {
            "title": "Scrape with multiple formats",
            "command": "uv run cli.py scrape --url https://example.com --formats markdown,html,links",
            "description": "Get content in multiple formats simultaneously"
        },
        {
            "title": "Scrape with content filtering",
            "command": "uv run cli.py scrape --url https://news.example.com --only-main-content --exclude-tags nav,footer,aside",
            "description": "Extract only main article content"
        },
        {
            "title": "Scrape dynamic page",
            "command": "uv run cli.py scrape --url https://spa.example.com --wait-for 3000",
            "description": "Wait 3 seconds for JavaScript to render"
        }
    ],
    "crawl": [
        {
            "title": "Basic crawl",
            "command": "uv run cli.py crawl --url https://docs.example.com --limit 10",
            "description": "Crawl up to 10 pages from docs site"
        },
        {
            "title": "Crawl specific paths",
            "command": "uv run cli.py crawl --url https://example.com --include-paths /docs/,/api/ --limit 50",
            "description": "Only crawl documentation and API pages"
        },
        {
            "title": "Deep crawl",
            "command": "uv run cli.py crawl --url https://example.com --max-depth 5 --limit 100",
            "description": "Crawl deeply through site hierarchy"
        }
    ],
    "extract": [
        {
            "title": "Extract product data",
            "command": "uv run cli.py extract --url https://store.example.com/product/123 --schema '{\"name\": \"string\", \"price\": \"number\", \"description\": \"string\"}'",
            "description": "Extract structured product information"
        },
        {
            "title": "Extract with prompt",
            "command": "uv run cli.py extract --url https://blog.example.com/post --schema '{\"title\": \"string\", \"author\": \"string\"}' --prompt 'Extract blog metadata'",
            "description": "Guide extraction with additional instructions"
        }
    ],
    "map": [
        {
            "title": "Map entire site",
            "command": "uv run cli.py map --url https://example.com --limit 200",
            "description": "Discover all URLs on a website"
        },
        {
            "title": "Find specific pages",
            "command": "uv run cli.py map --url https://docs.example.com --search api",
            "description": "Find all URLs containing 'api'"
        }
    ],
    "search": [
        {
            "title": "Basic search",
            "command": "uv run cli.py search --query 'python web scraping tutorial'",
            "description": "Search the web for tutorials"
        },
        {
            "title": "Regional search",
            "command": "uv run cli.py search --query 'local restaurants' --country us --lang en --limit 20",
            "description": "Search with regional preferences"
        }
    ]
}

# ===== MCP TOOL CALLING =====


async def call_mcp_tool(tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    """Call an MCP tool and return the result."""
    # Map CLI tool names to MCP tool names
    tool_mapping = {
        "scrape": "firecrawl_scrape",
        "crawl": "firecrawl_crawl",
        "extract": "firecrawl_extract",
        "map": "firecrawl_map",
        "search": "firecrawl_search",
    }

    mcp_tool_name = tool_mapping.get(tool_name, tool_name)

    async with get_client() as client:
        try:
            result = await client.call_tool(mcp_tool_name, arguments)
            if hasattr(result, "data") and result.data is not None:
                return result.data
            elif hasattr(result, "content"):
                if isinstance(result.content, list):
                    text_content = []
                    for block in result.content:
                        if hasattr(block, "text"):
                            text_content.append(block.text)
                        elif isinstance(block, dict) and "text" in block:
                            text_content.append(block["text"])
                    combined = "\n".join(text_content)
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


# ===== UTILITIES =====


def format_output(data: Any, format_type: str = "text") -> None:
    """Format and print output based on requested format."""
    if format_type == "json":
        try:
            print(json.dumps(data, indent=2, default=str))
        except (TypeError, ValueError) as e:
            print(json.dumps({"error": f"JSON serialization failed: {e!s}"}, indent=2), file=sys.stderr)
            sys.exit(1)
    else:
        if isinstance(data, dict):
            if "error" in data:
                print(f"Error: {data['error']}", file=sys.stderr)
            else:
                for key, value in data.items():
                    if isinstance(value, (dict, list)):
                        print(f"{key}:")
                        print(json.dumps(value, indent=2, default=str))
                    else:
                        print(f"{key}: {value}")
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    print(json.dumps(item, indent=2, default=str))
                else:
                    print(f"  - {item}")
        else:
            print(data)


def validate_credentials() -> bool:
    """Validate required credentials are available."""
    api_key = os.environ.get("FIRECRAWL_API_KEY")
    if not api_key:
        print("Error: FIRECRAWL_API_KEY environment variable is required", file=sys.stderr)
        print("Get your API key from https://firecrawl.dev", file=sys.stderr)
        return False
    return True


def show_help(format_type: str = "text") -> None:
    """Level 1: --help"""
    if format_type == "json":
        format_output({
            "title": "Firecrawl CLI",
            "commands": ["list", "info", "example"],
            "functions": list(FUNCTION_INFO.keys()),
        }, "json")
    else:
        print(QUICK_HELP)


def show_function_list(format_type: str = "text") -> None:
    """Level 2: list all functions"""
    if format_type == "json":
        format_output({"functions": list(FUNCTION_INFO.keys()), "count": len(FUNCTION_INFO)}, "json")
    else:
        print(QUICK_HELP)


def show_function_info(func_name: str, format_type: str = "text") -> None:
    """Level 2: info COMMAND"""
    if func_name not in FUNCTION_INFO:
        error_msg = f"Unknown function: {func_name}"
        available = list(FUNCTION_INFO.keys())
        if format_type == "json":
            format_output({"error": error_msg, "available_functions": available}, "json")
        else:
            print(f"Error: {error_msg}", file=sys.stderr)
            print(f"Available: {', '.join(available)}")
        sys.exit(1)

    info = FUNCTION_INFO[func_name]

    if format_type == "json":
        format_output(info, "json")
    else:
        print(f"\n{'=' * 60}")
        print(f"Function: {func_name}")
        print(f"{'=' * 60}")
        print(f"Description: {info.get('description', 'N/A')}")

        if info.get("parameters"):
            print("\nParameters:")
            for param in info["parameters"]:
                param_name = param.get("name", "unknown")
                param_type = param.get("type", "Any")
                required = "required" if param.get("required") else "optional"
                default = f", default: {param['default']}" if param.get("default") else ""
                desc = param.get("description", "")
                print(f"  --{param_name:20} ({param_type}, {required}{default})")
                if desc:
                    print(f"      {desc}")

        if info.get("returns"):
            print(f"\nReturns: {info['returns']}")
        print()


def show_function_example(func_name: str, format_type: str = "text") -> None:
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
        format_output({"function": func_name, "examples": examples, "count": len(examples)}, "json")
    else:
        print(f"\n{'=' * 60}")
        print(f"Examples for: {func_name}")
        print(f"{'=' * 60}\n")
        for i, example in enumerate(examples, 1):
            print(f"Example {i}: {example.get('title', 'Untitled')}")
            print(f"  {example.get('description', '')}")
            print(f"  $ {example.get('command', 'N/A')}")
            if example.get("output"):
                print(f"  Output: {example['output']}")
            print()


def execute_function(func_name: str, args: argparse.Namespace, format_type: str = "text") -> None:
    """Level 4: Execute the function via MCP tool call."""
    if func_name not in FUNCTION_INFO:
        print(f"Error: Unknown function: {func_name}", file=sys.stderr)
        sys.exit(1)

    func_info = FUNCTION_INFO[func_name]
    arguments: dict[str, Any] = {}

    if func_info.get("parameters"):
        for param in func_info["parameters"]:
            param_name = param.get("name", "")
            if param_name:
                arg_name = param_name.replace("-", "_")
                value = getattr(args, arg_name, None)
                if value is not None:
                    if param.get("type", "").startswith("list"):
                        if isinstance(value, str):
                            value = [v.strip() for v in value.split(",")]
                    arguments[param_name] = value
                elif param.get("required"):
                    print(f"Error: Missing required argument: --{param_name}", file=sys.stderr)
                    sys.exit(1)

    result = run_tool(func_name, arguments)
    format_output(result, format_type)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="firecrawl",
        description="Firecrawl CLI - Web Scraping & Crawling",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=True,
        epilog="""
PROGRESSIVE HELP LEVELS:
  Level 1: --help                    Quick overview
  Level 2: list                      List all functions
           info FUNCTION              Full documentation
           example FUNCTION           Working examples
  Level 3: FUNCTION [ARGS]           Execute function via MCP

QUICK START:
  uv run cli.py scrape --url https://example.com
  uv run cli.py crawl --url https://docs.example.com --limit 10
  uv run cli.py search --query "web scraping tutorial"

ENVIRONMENT:
  FIRECRAWL_API_KEY                  Required API key from firecrawl.dev

OUTPUT FORMATS:
  --format text                      Human-readable (default)
  --format json                      Machine-readable
        """,
    )

    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format (default: text)")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--discover", action="store_true", help="Discover tools from MCP server (live introspection)")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    subparsers.add_parser("list", help="List all functions")

    info_parser = subparsers.add_parser("info", help="Show function info")
    info_parser.add_argument("function", help="Function name")

    example_parser = subparsers.add_parser("example", help="Show examples")
    example_parser.add_argument("function", help="Function name")

    for func_name, func_info in FUNCTION_INFO.items():
        func_parser = subparsers.add_parser(func_name, help=func_info.get("description", ""), add_help=True)
        if func_info.get("parameters"):
            for param in func_info["parameters"]:
                param_name = param.get("name", "")
                if param_name:
                    func_parser.add_argument(
                        f"--{param_name}",
                        help=param.get("description", ""),
                        required=param.get("required", False),
                        default=param.get("default"),
                    )

    args = parser.parse_args()

    if args.discover:
        if not validate_credentials():
            sys.exit(1)
        try:
            tools = discover_tools()
            format_output({"tools": tools, "count": len(tools)}, args.format)
        except Exception as e:
            print(f"Error discovering tools: {e}", file=sys.stderr)
            sys.exit(1)
        return

    if args.command and args.command in FUNCTION_INFO:
        if not validate_credentials():
            sys.exit(1)

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
