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
CLI Wrapper for Repomix MCP
Auto-generated wrapper with 4-level progressive disclosure.

Run with: uv run repomix.py [COMMAND] [ARGS]

Levels:
  1. --help              Quick overview
  2. info TOOL          Detailed documentation
  3. example TOOL       Working examples
  4. TOOL --help        Complete reference (Level 4)
"""

import argparse
import asyncio
import json
import os
import sys
from typing import Dict, Any, Optional

from fastmcp import Client

# ===== MCP CLIENT CONFIGURATION =====

# Default: HTTP-based MCP server
MCP_SERVER_URL = os.environ.get("MCP_SERVER_URL", "http://localhost:8080")

def get_client():
    """Get MCP client."""
    return Client(MCP_SERVER_URL)

# ===== LEVEL 1: QUICK HELP =====

QUICK_HELP = """Repomix MCP

Available functions:
  pack_codebase                  Pack local codebase
  pack_remote_repository         Pack GitHub repository
  generate_skill                 Generate Claude skill
  attach_packed_output           Attach packed output
  grep_repomix_output            Search content

Use:
  uv run repomix.py list
  uv run repomix.py info FUNCTION_NAME
  uv run repomix.py example FUNCTION_NAME
  uv run repomix.py FUNCTION_NAME [ARGS]

Options:
  --format json|text|table  Output format (default: text)
"""

# ===== LEVEL 2: FUNCTION INFO =====

FUNCTION_INFO = {
    "pack_codebase": {
        "description": "Pack local codebase",
        "parameters": [],
        "returns": "Dict[str, Any]"
    },
    "pack_remote_repository": {
        "description": "Pack GitHub repository",
        "parameters": [],
        "returns": "Dict[str, Any]"
    },
    "generate_skill": {
        "description": "Generate Claude skill",
        "parameters": [],
        "returns": "Dict[str, Any]"
    },
    "attach_packed_output": {
        "description": "Attach packed output",
        "parameters": [],
        "returns": "Dict[str, Any]"
    },
    "grep_repomix_output": {
        "description": "Search content",
        "parameters": [],
        "returns": "Dict[str, Any]"
    }
}

# ===== LEVEL 3: EXAMPLES =====

FUNCTION_EXAMPLES = {
    "pack_codebase": [
        {
            "title": "Example",
            "command": "uv run WRAPPER.py pack_codebase"
        }
    ],
    "pack_remote_repository": [
        {
            "title": "Example",
            "command": "uv run WRAPPER.py pack_remote_repository"
        }
    ],
    "generate_skill": [
        {
            "title": "Example",
            "command": "uv run WRAPPER.py generate_skill"
        }
    ],
    "attach_packed_output": [
        {
            "title": "Example",
            "command": "uv run WRAPPER.py attach_packed_output"
        }
    ],
    "grep_repomix_output": [
        {
            "title": "Example",
            "command": "uv run WRAPPER.py grep_repomix_output"
        }
    ]
}

# ===== MCP TOOL CALLING =====

async def call_mcp_tool(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
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
    return True

def show_help(format_type: str = "text"):
    """Level 1: --help"""
    if format_type == "json":
        format_output({
            "title": "Repomix MCP",
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
        prog="repomix",
        description="Repomix MCP Wrapper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=True,
        epilog="""
PROGRESSIVE HELP LEVELS:
  Level 1: --help                    Quick overview
  Level 2: list                      List all functions
           info FUNCTION              Full documentation
           example FUNCTION           Working examples
  Level 3: FUNCTION [ARGS]           Execute function via MCP

EXAMPLES:
  uv run repomix.py --help
  uv run repomix.py list
  uv run repomix.py info my_function
  uv run repomix.py example my_function
  uv run repomix.py my_function --arg value

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
        try:
            tools = discover_tools()
            format_output({"tools": tools, "count": len(tools)}, args.format)
        except Exception as e:
            print(f"Error discovering tools: {e}", file=sys.stderr)
            sys.exit(1)
        return

    # Validate credentials for function execution
    if args.command and args.command in FUNCTION_INFO:
        if not validate_credentials():
            sys.exit(1)

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