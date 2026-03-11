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
CLI Wrapper for DeepWiki MCP Server
Production-ready wrapper with 4-level progressive disclosure.

Run with: uv run deepwiki.py [COMMAND] [ARGS]

Levels:
  1. --help              Quick overview (~30 tokens)
  2. list / info TOOL    Detailed documentation (~150 tokens)
  3. example TOOL        Working examples (~250 tokens)
  4. TOOL --help         Complete reference (~500 tokens)

MCP Server: https://mcp.deepwiki.com/mcp (HTTP with SSE)
Authentication: None required (free, open access)
"""

import argparse
import json
import re
import sys
from enum import Enum
from typing import Any

import httpx
from dotenv import load_dotenv

# Load environment variables from script directory (.env first, then .env.local overrides)
_script_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(_script_dir, ".env"))
load_dotenv(os.path.join(_script_dir, ".env.local"), override=True)


# ===== DETAIL LEVEL ENUM =====

class DetailLevel(str, Enum):
    """Control response verbosity for token optimization."""
    MINIMAL = "minimal"    # Success status only (~20 tokens)
    STANDARD = "standard"  # First 1000 chars (~300 tokens)
    FULL = "full"          # Complete response (varies)


# ===== MCP CLIENT CONFIGURATION =====

MCP_SERVER_URL = "https://mcp.deepwiki.com/mcp"
DEFAULT_TIMEOUT = 60.0  # seconds


# ===== MCP TOOL NAME MAPPING =====
# CLI command -> actual MCP tool name
TOOL_MAPPING = {
    "structure": "read_wiki_structure",
    "contents": "read_wiki_contents",
    "ask": "ask_question",
}


# ===== LEVEL 1: QUICK HELP =====

QUICK_HELP = """DeepWiki MCP - AI-powered GitHub repository documentation

Functions:
  structure    Get documentation topics for a repo
  contents     Read full documentation for a repo
  ask          Ask AI questions about a repo

Use:
  uv run deepwiki.py list
  uv run deepwiki.py info FUNCTION
  uv run deepwiki.py example FUNCTION
  uv run deepwiki.py FUNCTION [ARGS]

Options:
  --format json|text   Output format (default: text)
  --detail LEVEL       Response detail: minimal|standard|full (default: full)

Server: https://mcp.deepwiki.com/mcp (free, no auth required)
"""


# ===== LEVEL 2: FUNCTION INFO =====

FUNCTION_INFO = {
    "structure": {
        "mcp_tool": "read_wiki_structure",
        "description": "Get a list of documentation topics for a GitHub repository",
        "parameters": [
            {
                "name": "repo",
                "type": "str",
                "required": True,
                "description": "GitHub repository in owner/repo format (e.g. 'facebook/react')"
            }
        ],
        "returns": "String listing available documentation pages with hierarchy",
        "notes": "Use this first to discover what documentation is available",
        "related": ["contents", "ask"]
    },
    "contents": {
        "mcp_tool": "read_wiki_contents",
        "description": "View full documentation about a GitHub repository",
        "parameters": [
            {
                "name": "repo",
                "type": "str",
                "required": True,
                "description": "GitHub repository in owner/repo format (e.g. 'facebook/react')"
            }
        ],
        "returns": "String with complete documentation content",
        "notes": "Use 'structure' first to see available topics",
        "related": ["structure", "ask"]
    },
    "ask": {
        "mcp_tool": "ask_question",
        "description": "Ask any question about GitHub repository(ies) with AI-powered response",
        "parameters": [
            {
                "name": "repo",
                "type": "str",
                "required": True,
                "description": "GitHub repo(s) in owner/repo format. Multiple repos comma-separated (max 10)"
            },
            {
                "name": "question",
                "type": "str",
                "required": True,
                "description": "The question to ask about the repository"
            }
        ],
        "returns": "AI-generated answer grounded in repository context",
        "notes": "Can compare up to 10 repositories in a single query",
        "related": ["structure", "contents"]
    }
}


# ===== LEVEL 3: EXAMPLES =====

FUNCTION_EXAMPLES = {
    "structure": [
        {
            "title": "Get React documentation structure",
            "command": "uv run deepwiki.py structure --repo facebook/react",
            "output": "Available pages for facebook/react:\n- 1 React Overview\n  - 1.1 Core Concepts..."
        },
        {
            "title": "Get Claude Code documentation topics",
            "command": "uv run deepwiki.py structure --repo anthropics/claude-code"
        },
        {
            "title": "JSON output for parsing",
            "command": "uv run deepwiki.py --format json structure --repo langchain-ai/langchain"
        },
        {
            "title": "Minimal output (just success status)",
            "command": "uv run deepwiki.py --detail minimal structure --repo vercel/next.js"
        }
    ],
    "contents": [
        {
            "title": "Read React documentation",
            "command": "uv run deepwiki.py contents --repo facebook/react"
        },
        {
            "title": "Read and save to file",
            "command": "uv run deepwiki.py contents --repo vercel/next.js > nextjs-docs.md"
        },
        {
            "title": "Standard detail (preview only)",
            "command": "uv run deepwiki.py --detail standard contents --repo tensorflow/tensorflow"
        }
    ],
    "ask": [
        {
            "title": "Ask about React hooks",
            "command": "uv run deepwiki.py ask --repo facebook/react --question \"How do I use useState?\""
        },
        {
            "title": "Compare multiple repositories",
            "command": "uv run deepwiki.py ask --repo \"langchain-ai/langchain,llama-index/llama_index\" --question \"What are the key differences?\""
        },
        {
            "title": "Architecture question",
            "command": "uv run deepwiki.py ask --repo anthropics/claude-code --question \"How does the plugin system work?\""
        },
        {
            "title": "Get JSON response",
            "command": "uv run deepwiki.py --format json ask --repo pytorch/pytorch --question \"How do I create a custom layer?\""
        }
    ]
}


# ===== MCP HTTP CLIENT =====

def call_mcp_tool(tool_name: str, arguments: dict[str, Any], timeout: float = DEFAULT_TIMEOUT) -> dict[str, Any]:
    """Call an MCP tool via HTTP with SSE response handling."""
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        },
        "id": 1
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"
    }

    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.post(MCP_SERVER_URL, json=payload, headers=headers)
            response.raise_for_status()

            # Parse SSE response
            content = response.text
            result = parse_sse_response(content)
            return result

    except httpx.TimeoutException:
        return {"error": f"Request timed out after {timeout} seconds", "tool": tool_name}
    except httpx.HTTPStatusError as e:
        return {"error": f"HTTP error {e.response.status_code}: {e.response.text}", "tool": tool_name}
    except Exception as e:
        return {"error": str(e), "tool": tool_name, "arguments": arguments}


def parse_sse_response(content: str) -> dict[str, Any]:
    """Parse SSE (Server-Sent Events) response from MCP server."""
    # SSE format: "event: message\ndata: {...json...}"
    lines = content.strip().split("\n")
    json_data = None

    for line in lines:
        if line.startswith("data: "):
            json_str = line[6:]  # Remove "data: " prefix
            try:
                json_data = json.loads(json_str)
                break
            except json.JSONDecodeError:
                continue

    if json_data is None:
        # Try parsing entire content as JSON
        try:
            json_data = json.loads(content)
        except json.JSONDecodeError:
            return {"error": "Failed to parse SSE response", "raw": content[:500]}

    # Extract result from JSON-RPC response
    if "result" in json_data:
        result = json_data["result"]
        # Handle content array format
        if isinstance(result, dict) and "content" in result:
            content_items = result["content"]
            if isinstance(content_items, list):
                texts = []
                for item in content_items:
                    if isinstance(item, dict) and "text" in item:
                        texts.append(item["text"])
                if texts:
                    return {"result": "\n".join(texts), "success": True}
        # Handle structuredContent format
        if isinstance(result, dict) and "structuredContent" in result:
            structured = result["structuredContent"]
            if isinstance(structured, dict) and "result" in structured:
                return {"result": structured["result"], "success": True}
        return {"result": result, "success": True}

    if "error" in json_data:
        error = json_data["error"]
        msg = error.get("message", str(error)) if isinstance(error, dict) else str(error)
        return {"error": msg, "success": False}

    return {"result": json_data, "success": True}


def list_mcp_tools(timeout: float = DEFAULT_TIMEOUT) -> list:
    """Discover available tools from the MCP server."""
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/list",
        "id": 1
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"
    }

    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.post(MCP_SERVER_URL, json=payload, headers=headers)
            response.raise_for_status()

            result = parse_sse_response(response.text)
            if "result" in result and isinstance(result["result"], dict):
                tools = result["result"].get("tools", [])
                return [{"name": t.get("name"), "description": t.get("description")} for t in tools]
            return []

    except Exception as e:
        return [{"error": str(e)}]


# ===== DETAIL LEVEL PROCESSING =====

def apply_detail_level(data: dict[str, Any], level: str) -> dict[str, Any]:
    """Apply detail level filtering to response data."""
    if level == DetailLevel.FULL:
        return data

    if level == DetailLevel.MINIMAL:
        if "error" in data:
            return {"success": False, "error": data["error"]}
        return {"success": True}

    if level == DetailLevel.STANDARD:
        if "error" in data:
            return {"success": False, "error": data["error"]}
        if "result" in data:
            result = data["result"]
            if isinstance(result, str) and len(result) > 1000:
                return {
                    "success": True,
                    "result_preview": result[:1000] + "...",
                    "full_length": len(result)
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
            elif "result" in data:
                print(data["result"])
            elif "result_preview" in data:
                print(data["result_preview"])
                print(f"\n[Truncated - full response: {data.get('full_length', 'unknown')} chars]")
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


def validate_repo_format(repo: str) -> bool:
    """Validate GitHub repository format (owner/repo or comma-separated list)."""
    # Split by comma for multiple repos
    repos = [r.strip() for r in repo.split(",")]
    if len(repos) > 10:
        return False

    pattern = re.compile(r"^[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+$")
    return all(pattern.match(r) for r in repos)


def parse_repo_argument(repo: str) -> str | list[str]:
    """Parse repo argument into single string or list for MCP call."""
    repos = [r.strip() for r in repo.split(",")]
    if len(repos) == 1:
        return repos[0]
    return repos


def show_help(format_type: str = "text"):
    """Level 1: --help"""
    if format_type == "json":
        format_output({
            "title": "DeepWiki MCP",
            "description": "AI-powered GitHub repository documentation",
            "commands": ["list", "info", "example"],
            "functions": list(FUNCTION_INFO.keys()),
            "server": MCP_SERVER_URL
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
                desc = param.get('description', '')
                print(f"  --{param_name:20} ({param_type}, {required})")
                if desc:
                    print(f"      {desc}")

        if info.get('returns'):
            print(f"\nReturns: {info['returns']}")
        if info.get('notes'):
            print(f"Notes: {info['notes']}")
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

    func_info = FUNCTION_INFO[func_name]
    arguments: dict[str, Any] = {}

    # Build arguments from parsed args
    if func_info.get('parameters'):
        for param in func_info['parameters']:
            param_name = param.get('name', '')
            if param_name:
                arg_name = param_name.replace('-', '_')
                value = getattr(args, arg_name, None)
                if value is not None:
                    # Validate repo format
                    if param_name == "repo":
                        if not validate_repo_format(value):
                            print(f"Error: Invalid repo format: {value}", file=sys.stderr)
                            print("Use owner/repo format (e.g. 'facebook/react')", file=sys.stderr)
                            print("Multiple repos: comma-separated (max 10)", file=sys.stderr)
                            sys.exit(1)
                        # Map 'repo' to 'repoName' for MCP
                        arguments["repoName"] = parse_repo_argument(value)
                    else:
                        arguments[param_name] = value
                elif param.get('required'):
                    print(f"Error: Missing required argument: --{param_name}", file=sys.stderr)
                    sys.exit(1)

    # Get actual MCP tool name
    mcp_tool_name = TOOL_MAPPING.get(func_name, func_name)

    # Get timeout from args
    timeout = getattr(args, 'timeout', DEFAULT_TIMEOUT)

    # Call the MCP tool
    try:
        result = call_mcp_tool(mcp_tool_name, arguments, timeout=timeout)
    except Exception as e:
        print(f"Error calling MCP tool: {e}", file=sys.stderr)
        sys.exit(1)

    # Apply detail level filtering
    detail_level = getattr(args, 'detail', DetailLevel.FULL)
    result = apply_detail_level(result, detail_level)

    format_output(result, format_type)

    # Exit with error code if result indicates failure
    if isinstance(result, dict) and "error" in result:
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        prog="deepwiki",
        description="DeepWiki MCP CLI Wrapper - AI-powered GitHub repository documentation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=True,
        epilog="""
PROGRESSIVE HELP LEVELS:
  Level 1: --help                    Quick overview (~30 tokens)
  Level 2: list                      List all functions
           info FUNCTION             Full documentation (~150 tokens)
  Level 3: example FUNCTION          Working examples (~250 tokens)
  Level 4: FUNCTION [ARGS]           Execute function via MCP

EXAMPLES:
  uv run deepwiki.py --help
  uv run deepwiki.py list
  uv run deepwiki.py info structure
  uv run deepwiki.py example ask
  uv run deepwiki.py structure --repo facebook/react
  uv run deepwiki.py ask --repo anthropics/claude-code --question "How do plugins work?"

DETAIL LEVELS (for token optimization):
  --detail minimal    Success status only (~20 tokens)
  --detail standard   Preview of response, first 1000 chars (~300 tokens)
  --detail full       Complete response (default, varies by content)

OUTPUT FORMATS:
  --format text       Human-readable (default)
  --format json       Machine-readable (pipe to jq for filtering)

SERVER:
  https://mcp.deepwiki.com/mcp (free, no authentication required)
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
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help=f"Request timeout in seconds (default: {DEFAULT_TIMEOUT})"
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
    info_parser.add_argument("function", help="Function name (structure, contents, or ask)")

    # Level 3: example
    example_parser = subparsers.add_parser("example", help="Show working examples")
    example_parser.add_argument("function", help="Function name (structure, contents, or ask)")

    # Level 4: Dynamic function subparsers (actual execution)
    for func_name, func_info in FUNCTION_INFO.items():
        func_parser = subparsers.add_parser(
            func_name,
            help=func_info.get('description', ''),
            add_help=True
        )
        if func_info.get('parameters'):
            for param in func_info['parameters']:
                param_name = param.get('name', '')
                if param_name:
                    func_parser.add_argument(
                        f"--{param_name}",
                        type=str,
                        help=param.get('description', ''),
                        required=param.get('required', False),
                        default=param.get('default'),
                    )

    args = parser.parse_args()

    # Handle --discover flag
    if args.discover:
        try:
            tools = list_mcp_tools(timeout=args.timeout)
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
