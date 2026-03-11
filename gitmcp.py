#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "mcp>=1.0",
#     "httpx>=0.24.0",
#     "httpx-sse>=0.4.0",
#     "pydantic>=2.0",
#     "python-dotenv>=1.0.0",
# ]
# ///
"""
CLI Wrapper for GitMCP - Chat with GitHub Documentation
Auto-generated wrapper with 4-level progressive disclosure.

Run with: uv run gitmcp.py [COMMAND] [ARGS]

Levels:
  1. --help              Quick overview
  2. info TOOL           Detailed documentation
  3. example TOOL        Working examples
  4. TOOL [ARGS]         Execute function via MCP

Server: https://gitmcp.io/docs
"""

import argparse
import asyncio
import json
import os
import sys
from typing import Dict, Any, Optional
from contextlib import asynccontextmanager

import httpx
from dotenv import load_dotenv
from mcp import ClientSession
from mcp.client.sse import sse_client

# Load environment variables from script directory (.env first, then .env.local overrides)
_script_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(_script_dir, ".env"))
load_dotenv(os.path.join(_script_dir, ".env.local"), override=True)

# ===== MCP CLIENT CONFIGURATION =====

MCP_SERVER_URL = os.environ.get("GITMCP_URL", "https://gitmcp.io/docs")

@asynccontextmanager
async def get_client():
    """Get MCP client session for SSE transport."""
    async with sse_client(MCP_SERVER_URL) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            yield session

# ===== LEVEL 1: QUICK HELP =====

QUICK_HELP = """GitMCP - Chat with GitHub Documentation

Available functions:
  match_common_libs_owner_repo_mapping   Look up owner/repo from library name
  fetch_generic_documentation            Fetch docs for any GitHub repository
  search_generic_documentation           Semantic search in documentation
  search_generic_code                    Search code in a repository
  fetch_generic_url_content              Fetch content from any URL

Use:
  uv run gitmcp.py list
  uv run gitmcp.py info FUNCTION_NAME
  uv run gitmcp.py example FUNCTION_NAME
  uv run gitmcp.py FUNCTION_NAME [ARGS]

Environment:
  GITMCP_URL    Server URL (default: https://gitmcp.io/docs)

Options:
  --format json|text    Output format (default: text)
  --discover            Live introspection of available tools
"""

# ===== LEVEL 2: FUNCTION INFO =====

FUNCTION_INFO = {
    "match_common_libs_owner_repo_mapping": {
        "description": "Match a library name to an owner/repo. Use this first if only a library name was provided (e.g., 'fastmcp', 'langchain'). Returns owner and repo to use with other tools.",
        "parameters": [
            {
                "name": "library",
                "type": "string",
                "required": True,
                "description": "Library name to look up (e.g., 'fastmcp', 'react', 'langchain')"
            }
        ],
        "returns": "Dict[str, Any] - Owner and repo mapping if found"
    },
    "fetch_generic_documentation": {
        "description": "Fetch documentation for any GitHub repository. Prioritizes llms.txt, then AI-optimized docs, then README.md.",
        "parameters": [
            {
                "name": "owner",
                "type": "string",
                "required": True,
                "description": "GitHub repository owner (username or org)"
            },
            {
                "name": "repo",
                "type": "string",
                "required": True,
                "description": "GitHub repository name"
            }
        ],
        "returns": "Dict[str, Any] - Documentation content with metadata"
    },
    "search_generic_documentation": {
        "description": "Semantically search in documentation for any GitHub repository. Returns relevant excerpts matching the query. Useful for specific queries.",
        "parameters": [
            {
                "name": "owner",
                "type": "string",
                "required": True,
                "description": "GitHub repository owner"
            },
            {
                "name": "repo",
                "type": "string",
                "required": True,
                "description": "GitHub repository name"
            },
            {
                "name": "query",
                "type": "string",
                "required": True,
                "description": "Search query string"
            }
        ],
        "returns": "Dict[str, Any] - Search results with matching excerpts"
    },
    "search_generic_code": {
        "description": "Search for code in any GitHub repository. Returns matching files. Supports pagination with 30 results per page.",
        "parameters": [
            {
                "name": "owner",
                "type": "string",
                "required": True,
                "description": "GitHub repository owner"
            },
            {
                "name": "repo",
                "type": "string",
                "required": True,
                "description": "GitHub repository name"
            },
            {
                "name": "query",
                "type": "string",
                "required": True,
                "description": "Code search query"
            },
            {
                "name": "page",
                "type": "integer",
                "required": False,
                "description": "Page number for pagination (30 results per page)",
                "default": 1
            }
        ],
        "returns": "Dict[str, Any] - Code search results with file paths and snippets"
    },
    "fetch_generic_url_content": {
        "description": "Fetch content from any absolute URL, respecting robots.txt rules. Use to retrieve referenced URLs from previously fetched documentation.",
        "parameters": [
            {
                "name": "url",
                "type": "string",
                "required": True,
                "description": "Absolute URL to fetch content from"
            }
        ],
        "returns": "Dict[str, Any] - Converted content in markdown format"
    }
}

# ===== LEVEL 3: EXAMPLES =====

FUNCTION_EXAMPLES = {
    "match_common_libs_owner_repo_mapping": [
        {
            "title": "Look up FastMCP repository",
            "command": "uv run gitmcp.py match_common_libs_owner_repo_mapping --library fastmcp",
            "output": '{"owner": "jlowin", "repo": "fastmcp"}'
        },
        {
            "title": "Look up React repository",
            "command": "uv run gitmcp.py match_common_libs_owner_repo_mapping --library react",
            "output": '{"owner": "facebook", "repo": "react"}'
        }
    ],
    "fetch_generic_documentation": [
        {
            "title": "Fetch FastMCP documentation",
            "command": "uv run gitmcp.py fetch_generic_documentation --owner jlowin --repo fastmcp",
            "output": '{"content": "# FastMCP\\n\\nThe fast, Pythonic way to build MCP servers...", "source": "README.md"}'
        },
        {
            "title": "Fetch Anthropic Claude documentation",
            "command": "uv run gitmcp.py fetch_generic_documentation --owner anthropics --repo claude-code",
            "output": '{"content": "# Claude Code\\n\\nClaude Code is...", "source": "llms.txt"}'
        }
    ],
    "search_generic_documentation": [
        {
            "title": "Search for installation instructions",
            "command": "uv run gitmcp.py search_generic_documentation --owner jlowin --repo fastmcp --query 'how to install'",
            "output": '{"results": [{"excerpt": "pip install fastmcp", "file": "README.md"}]}'
        },
        {
            "title": "Search for API documentation",
            "command": "uv run gitmcp.py search_generic_documentation --owner anthropics --repo anthropic-sdk-python --query 'streaming responses'",
            "output": '{"results": [{"excerpt": "Use client.messages.stream()...", "file": "docs/streaming.md"}]}'
        }
    ],
    "search_generic_code": [
        {
            "title": "Search for function implementation",
            "command": "uv run gitmcp.py search_generic_code --owner jlowin --repo fastmcp --query 'def tool'",
            "output": '{"results": [{"file": "src/fastmcp/tools.py", "snippet": "@app.tool()\\ndef my_tool():..."}]}'
        },
        {
            "title": "Search with pagination",
            "command": "uv run gitmcp.py search_generic_code --owner anthropics --repo anthropic-sdk-python --query 'class' --page 2",
            "output": '{"results": [...], "page": 2, "total_pages": 5}'
        }
    ],
    "fetch_generic_url_content": [
        {
            "title": "Fetch external documentation page",
            "command": "uv run gitmcp.py fetch_generic_url_content --url 'https://docs.anthropic.com/en/docs/overview'",
            "output": '{"content": "# Anthropic API Overview\\n\\n...", "format": "markdown"}'
        },
        {
            "title": "Fetch referenced URL from docs",
            "command": "uv run gitmcp.py fetch_generic_url_content --url 'https://github.com/jlowin/fastmcp/blob/main/docs/quickstart.md'",
            "output": '{"content": "# Quick Start Guide\\n\\n..."}'
        }
    ]
}

# ===== MCP TOOL CALLING =====

async def call_mcp_tool(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Call an MCP tool and return the result."""
    async with get_client() as session:
        try:
            result = await session.call_tool(tool_name, arguments)
            # Handle different result formats
            if hasattr(result, 'content') and result.content:
                content_list = result.content
                text_parts = []
                for block in content_list:
                    if hasattr(block, 'text'):
                        text_parts.append(block.text)
                    elif isinstance(block, dict) and 'text' in block:
                        text_parts.append(block['text'])
                combined = '\n'.join(text_parts)
                # Try to parse as JSON
                try:
                    return json.loads(combined)
                except json.JSONDecodeError:
                    return {"result": combined}
            return {"result": str(result)}
        except Exception as e:
            return {"error": str(e), "tool": tool_name, "arguments": arguments}

async def list_mcp_tools() -> list:
    """Discover available tools from the MCP server."""
    async with get_client() as session:
        result = await session.list_tools()
        tools = result.tools if hasattr(result, 'tools') else result
        return [{"name": t.name, "description": t.description} for t in tools]

def run_tool(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
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
            print(json.dumps({"error": f"JSON serialization failed: {str(e)}"}, indent=2), file=sys.stderr)
            sys.exit(1)
    else:  # text format
        if isinstance(data, dict):
            if "error" in data:
                print(f"Error: {data['error']}", file=sys.stderr)
            elif "result" in data:
                result = data["result"]
                if isinstance(result, str) and len(result) > 200:
                    # Truncate long results for text display
                    print(result[:2000] + "..." if len(result) > 2000 else result)
                else:
                    print(result)
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

def show_help(format_type: str = "text"):
    """Level 1: --help"""
    if format_type == "json":
        format_output({
            "title": "GitMCP",
            "server": MCP_SERVER_URL,
            "commands": ["list", "info", "example"],
            "functions": list(FUNCTION_INFO.keys())
        }, "json")
    else:
        print(QUICK_HELP)

def show_function_list(format_type: str = "text"):
    """Level 2: list all functions"""
    if format_type == "json":
        format_output({
            "functions": list(FUNCTION_INFO.keys()),
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

        if info.get('parameters'):
            print("\nParameters:")
            for param in info['parameters']:
                param_name = param.get('name', 'unknown')
                param_type = param.get('type', 'Any')
                required = "required" if param.get('required') else "optional"
                desc = param.get('description', '')
                print(f"  --{param_name:20} ({param_type}, {required})")
                if desc:
                    print(f"      {desc}")

        if info.get('returns'):
            print(f"\nReturns: {info['returns']}")
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

    # Build arguments dict from parsed args
    func_info = FUNCTION_INFO[func_name]
    arguments = {}

    if func_info.get('parameters'):
        for param in func_info['parameters']:
            param_name = param.get('name', '')
            if param_name:
                # Get value from args (argparse converts - to _)
                arg_name = param_name.replace('-', '_')
                value = getattr(args, arg_name, None)
                if value is not None:
                    arguments[param_name] = value
                elif param.get('required'):
                    print(f"Error: Missing required argument: --{param_name}", file=sys.stderr)
                    sys.exit(1)

    # Call the MCP tool
    result = run_tool(func_name, arguments)
    format_output(result, format_type)

def main():
    parser = argparse.ArgumentParser(
        prog="gitmcp",
        description="GitMCP - Chat with GitHub Documentation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=True,
        epilog="""
PROGRESSIVE HELP LEVELS:
  Level 1: --help                    Quick overview
  Level 2: list                      List all functions
           info FUNCTION             Full documentation
           example FUNCTION          Working examples
  Level 3: FUNCTION [ARGS]           Execute function via MCP

EXAMPLES:
  uv run gitmcp.py --help
  uv run gitmcp.py --discover
  uv run gitmcp.py list
  uv run gitmcp.py info fetch_generic_documentation
  uv run gitmcp.py example search_generic_code
  uv run gitmcp.py fetch_generic_documentation --owner anthropics --repo claude-code
  uv run gitmcp.py search_generic_code --owner jlowin --repo fastmcp --query "def tool"

OUTPUT FORMATS:
  --format text                      Human-readable (default)
  --format json                      Machine-readable
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
    parser.add_argument(
        "--discover",
        action="store_true",
        help="Discover tools from MCP server (live introspection)"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Level 2: list
    subparsers.add_parser("list", help="List all functions")

    # Level 2: info
    info_parser = subparsers.add_parser("info", help="Show function info")
    info_parser.add_argument("function", help="Function name")

    # Level 2/3: example
    example_parser = subparsers.add_parser("example", help="Show examples")
    example_parser.add_argument("function", help="Function name")

    # Level 4: Dynamic function subparsers (actual execution)
    for func_name in FUNCTION_INFO.keys():
        func_info = FUNCTION_INFO[func_name]
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
                    func_parser.add_argument(
                        f"--{param_name}",
                        help=param.get('description', ''),
                        required=param.get('required', False),
                        default=param.get('default'),
                    )

    args = parser.parse_args()

    # Handle --discover flag
    if args.discover:
        print(f"Discovering tools from {MCP_SERVER_URL}...")
        try:
            tools = discover_tools()
            format_output({"tools": tools, "count": len(tools)}, args.format)
        except Exception as e:
            print(f"Error discovering tools: {e}", file=sys.stderr)
            if args.verbose:
                import traceback
                traceback.print_exc()
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
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
