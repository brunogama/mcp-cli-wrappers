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
CLI Wrapper for Sequential Thinking MCP
Production-ready wrapper with 4-level progressive disclosure.

Run with: uv run cli.py [COMMAND] [ARGS]

Levels:
  1. --help              Quick overview (~30 tokens)
  2. list / info TOOL    Detailed documentation (~150 tokens)
  3. example TOOL        Working examples (~200 tokens)
  4. TOOL --help         Complete reference (~500 tokens)

Sequential Thinking enables multi-step reasoning for complex problems,
breaking down analysis into structured thought chains with revision support.
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

NPX_PACKAGE = "@anthropics/sequential-thinking-mcp"
NPX_ARGS: list[str] = []

_transport = NpxStdioTransport(
    package=NPX_PACKAGE,
    args=NPX_ARGS,
    env_vars={
        "DEBUG": os.environ.get("DEBUG", "false"),
    },
)


def get_client() -> Client:
    """Get MCP client for npx transport."""
    return Client(_transport)


# ===== LEVEL 1: QUICK HELP =====

QUICK_HELP = """Sequential Thinking MCP - Multi-step reasoning for complex problems

Available functions:
  sequentialthinking    Run sequential thinking process with thought chains

Use:
  uv run cli.py list                          # List all functions
  uv run cli.py info sequentialthinking       # Detailed documentation
  uv run cli.py example sequentialthinking    # Working examples
  uv run cli.py sequentialthinking [ARGS]     # Execute function

Options:
  --format json|text    Output format (default: text)
  --verbose             Enable verbose output
  --discover            Live introspection of MCP tools
"""

# ===== LEVEL 2: FUNCTION INFO =====

FUNCTION_INFO = {
    "sequentialthinking": {
        "description": "Run sequential thinking process with structured thought chains",
        "long_description": """
Sequential Thinking enables systematic problem-solving through structured thought chains.

Key Features:
- Break complex problems into discrete, manageable thoughts
- Each thought builds on previous reasoning
- Support for revision and branching of thought chains
- Hypothesis formation and validation
- Multi-step analysis with clear progression

Use Cases:
- Complex code analysis and debugging
- Architecture design decisions
- Root cause analysis
- Multi-factor decision making
- Research synthesis
        """.strip(),
        "parameters": [
            {
                "name": "thought",
                "type": "string",
                "required": True,
                "description": "The current thought or reasoning step in the chain"
            },
            {
                "name": "thoughtNumber",
                "type": "integer",
                "required": True,
                "description": "Current position in the thought sequence (1-indexed)"
            },
            {
                "name": "totalThoughts",
                "type": "integer",
                "required": True,
                "description": "Estimated total thoughts needed (can be revised)"
            },
            {
                "name": "nextThoughtNeeded",
                "type": "boolean",
                "required": True,
                "description": "Whether another thought step is required"
            },
            {
                "name": "isRevision",
                "type": "boolean",
                "required": False,
                "default": False,
                "description": "Whether this revises a previous thought"
            },
            {
                "name": "revisesThought",
                "type": "integer",
                "required": False,
                "description": "Which thought number this revises (if isRevision=true)"
            },
            {
                "name": "branchFromThought",
                "type": "integer",
                "required": False,
                "description": "Create alternative branch from this thought number"
            },
            {
                "name": "branchId",
                "type": "string",
                "required": False,
                "description": "Identifier for the current branch"
            },
            {
                "name": "needsMoreThoughts",
                "type": "boolean",
                "required": False,
                "default": False,
                "description": "Signal that more thoughts are needed than estimated"
            }
        ],
        "returns": "Dict with thoughtNumber, totalThoughts, nextThoughtNeeded, and optional branch/revision info",
        "related": []
    }
}

# ===== LEVEL 3: EXAMPLES =====

FUNCTION_EXAMPLES = {
    "sequentialthinking": [
        {
            "title": "Start a new reasoning chain",
            "description": "Begin analyzing a problem with the first thought",
            "command": 'uv run cli.py sequentialthinking --thought "Let me analyze the authentication flow. First, I need to understand how tokens are validated." --thoughtNumber 1 --totalThoughts 5 --nextThoughtNeeded true',
            "output": '{"thoughtNumber": 1, "totalThoughts": 5, "nextThoughtNeeded": true}'
        },
        {
            "title": "Continue the chain",
            "description": "Add subsequent thoughts building on previous analysis",
            "command": 'uv run cli.py sequentialthinking --thought "The token validation uses JWT with RS256. I should check the key rotation policy next." --thoughtNumber 2 --totalThoughts 5 --nextThoughtNeeded true',
            "output": '{"thoughtNumber": 2, "totalThoughts": 5, "nextThoughtNeeded": true}'
        },
        {
            "title": "Revise a previous thought",
            "description": "Correct or update an earlier conclusion",
            "command": 'uv run cli.py sequentialthinking --thought "Actually, reviewing the code again, the validation uses HS256 not RS256." --thoughtNumber 3 --totalThoughts 5 --nextThoughtNeeded true --isRevision true --revisesThought 2',
            "output": '{"thoughtNumber": 3, "totalThoughts": 5, "nextThoughtNeeded": true, "isRevision": true, "revisesThought": 2}'
        },
        {
            "title": "Create a branch for alternative analysis",
            "description": "Explore an alternative hypothesis",
            "command": 'uv run cli.py sequentialthinking --thought "What if the issue is not in validation but in token generation?" --thoughtNumber 3 --totalThoughts 4 --nextThoughtNeeded true --branchFromThought 2 --branchId "alt-generation"',
            "output": '{"thoughtNumber": 3, "totalThoughts": 4, "nextThoughtNeeded": true, "branchId": "alt-generation"}'
        },
        {
            "title": "Complete the chain",
            "description": "Final thought concluding the analysis",
            "command": 'uv run cli.py sequentialthinking --thought "In conclusion, the vulnerability is in the token refresh logic where the old token is not invalidated." --thoughtNumber 5 --totalThoughts 5 --nextThoughtNeeded false',
            "output": '{"thoughtNumber": 5, "totalThoughts": 5, "nextThoughtNeeded": false}'
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


# ===== UTILITIES =====


def format_output(data: Any, format_type: str = "text") -> None:
    """Format and print output based on requested format."""
    if format_type == "json":
        try:
            print(json.dumps(data, indent=2, default=str))
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
    # Sequential thinking doesn't require API keys
    return True


def show_help(format_type: str = "text") -> None:
    """Level 1: --help"""
    if format_type == "json":
        format_output({
            "title": "Sequential Thinking MCP",
            "description": "Multi-step reasoning for complex problems",
            "commands": ["list", "info", "example"],
            "functions": list(FUNCTION_INFO.keys())
        }, "json")
    else:
        print(QUICK_HELP)


def show_function_list(format_type: str = "text") -> None:
    """Level 2: list all functions"""
    if format_type == "json":
        format_output({
            "functions": [
                {"name": name, "description": info.get("description", "")}
                for name, info in FUNCTION_INFO.items()
            ],
            "count": len(FUNCTION_INFO)
        }, "json")
    else:
        print("Available Functions:")
        print("=" * 60)
        for name, info in FUNCTION_INFO.items():
            print(f"\n  {name}")
            print(f"    {info.get('description', 'N/A')}")
        print("\nUse 'info FUNCTION' for detailed documentation.")
        print("Use 'example FUNCTION' for working examples.")


def show_function_info(func_name: str, format_type: str = "text") -> None:
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
        print(f"\n{'=' * 60}")
        print(f"Function: {func_name}")
        print(f"{'=' * 60}")
        print(f"\nDescription: {info.get('description', 'N/A')}")

        if info.get('long_description'):
            print(f"\n{info['long_description']}")

        if info.get('parameters'):
            print("\nParameters:")
            for param in info['parameters']:
                param_name = param.get('name', 'unknown')
                param_type = param.get('type', 'Any')
                required = "required" if param.get('required') else "optional"
                default = param.get('default')
                desc = param.get('description', '')
                default_str = f", default={default}" if default is not None else ""
                print(f"  --{param_name:20} ({param_type}, {required}{default_str})")
                if desc:
                    print(f"      {desc}")

        if info.get('returns'):
            print(f"\nReturns: {info['returns']}")

        if info.get('related'):
            print(f"\nRelated: {', '.join(info['related'])}")
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
        format_output({
            "function": func_name,
            "examples": examples,
            "count": len(examples)
        }, "json")
    else:
        print(f"\n{'=' * 60}")
        print(f"Examples for: {func_name}")
        print(f"{'=' * 60}\n")
        for i, example in enumerate(examples, 1):
            print(f"Example {i}: {example.get('title', 'Untitled')}")
            if example.get('description'):
                print(f"  {example['description']}")
            print(f"\n  Command:")
            print(f"    {example.get('command', 'N/A')}")
            if example.get('output'):
                print(f"\n  Output:")
                print(f"    {example['output']}")
            print()


def execute_function(func_name: str, args: argparse.Namespace, format_type: str = "text") -> None:
    """Level 4: Execute the function via MCP tool call."""
    if func_name not in FUNCTION_INFO:
        print(f"Error: Unknown function: {func_name}", file=sys.stderr)
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
                    arguments[param_name] = value
                elif param.get('required'):
                    print(f"Error: Missing required argument: --{param_name}", file=sys.stderr)
                    sys.exit(1)

    # Call the MCP tool
    result = run_tool(func_name, arguments)
    format_output(result, format_type)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="sequential-thinking",
        description="Sequential Thinking MCP - Multi-step reasoning for complex problems",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=True,
        epilog="""
PROGRESSIVE HELP LEVELS:
  Level 1: --help                    Quick overview (~30 tokens)
  Level 2: list                      List all functions
           info FUNCTION             Full documentation (~150 tokens)
  Level 3: example FUNCTION          Working examples (~200 tokens)
  Level 4: FUNCTION --help           Complete reference (~500 tokens)

EXAMPLES:
  uv run cli.py --help
  uv run cli.py list
  uv run cli.py info sequentialthinking
  uv run cli.py example sequentialthinking
  uv run cli.py sequentialthinking --thought "First step" --thoughtNumber 1 --totalThoughts 3 --nextThoughtNeeded true

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
                    param_type = param.get('type', 'string')
                    # Map types to argparse types
                    type_map = {
                        'string': str,
                        'integer': int,
                        'boolean': lambda x: x.lower() in ('true', '1', 'yes'),
                        'number': float,
                    }
                    arg_type = type_map.get(param_type, str)

                    func_parser.add_argument(
                        f"--{param_name}",
                        help=param.get('description', ''),
                        required=param.get('required', False),
                        default=param.get('default'),
                        type=arg_type,
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
        print(f"Error: {e!s}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
