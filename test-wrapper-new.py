#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "httpx>=0.24.0",
#     "pydantic>=2.0",
#     "click>=8.0",
#     "rich>=13.0",
# ]
# ///
"""
CLI Wrapper for Sequential Thinking MCP
Auto-generated wrapper with 4-level progressive disclosure.

Run with: uv run test-wrapper-new.py [COMMAND] [ARGS]

Levels:
  1. --help              Quick overview
  2. info TOOL          Detailed documentation
  3. example TOOL       Working examples
  4. TOOL --help        Complete reference (Level 4)
"""

import argparse
import json
import os
import sys
from typing import Dict, Any

# ===== LEVEL 1: QUICK HELP =====

QUICK_HELP = """Sequential Thinking MCP

Available functions:
  sequentialthinking     Run sequential thinking process

Use:
  uv run test-wrapper-new.py list
  uv run test-wrapper-new.py info FUNCTION_NAME
  uv run test-wrapper-new.py example FUNCTION_NAME
  uv run test-wrapper-new.py FUNCTION_NAME --help

Options:
  --format json|text|table  Output format (default: text)
"""

# ===== LEVEL 2: FUNCTION INFO =====

FUNCTION_INFO = {
    "sequentialthinking": {
        "description": "Run sequential thinking process",
        "parameters": [],
        "returns": "Dict[str, Any]"
    }
}

# ===== LEVEL 3: EXAMPLES =====

FUNCTION_EXAMPLES = {
    "sequentialthinking": [
        {
            "title": "Example",
            "command": "uv run test-wrapper-new.py sequentialthinking"
        }
    ]
}

# ===== UTILITIES =====

def format_output(data: Any, format_type: str = "text") -> None:
    """Format and print output based on requested format."""
    if format_type == "json":
        try:
            print(json.dumps(data, indent=2))
        except (TypeError, ValueError) as e:
            print(json.dumps({"error": f"JSON serialization failed: {str(e)}"}, indent=2), file=sys.stderr)
            sys.exit(1)
    else:  # text format
        if isinstance(data, dict):
            for key, value in data.items():
                print(f"{key}: {value}")
        elif isinstance(data, list):
            for item in data:
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
            "title": "Sequential Thinking MCP",
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
            print(f"✗ {error_msg}")
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
                print(f"  {param_name:25} ({param_type})")

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
            print(f"✗ {error_msg}")
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

def show_function_help(func_name: str):
    """Level 4: FUNCTION --help (complete reference)"""
    if func_name not in FUNCTION_INFO:
        print(f"✗ Unknown function: {func_name}", file=sys.stderr)
        sys.exit(1)

    info = FUNCTION_INFO[func_name]
    print(f"\n{'='*60}")
    print(f"Function: {func_name}")
    print(f"{'='*60}")
    print(f"\nDescription:\n  {info.get('description', 'N/A')}")

    if info.get('parameters'):
        print(f"\nParameters:")
        for param in info['parameters']:
            name = param.get('name', 'unknown')
            ptype = param.get('type', 'Any')
            desc = param.get('description', '')
            print(f"  --{name}")
            print(f"    Type: {ptype}")
            if desc:
                print(f"    {desc}")

    print(f"\nReturns:\n  {info.get('returns', 'Dict[str, Any]')}")

    if func_name in FUNCTION_EXAMPLES:
        print(f"\nExamples:")
        for i, example in enumerate(FUNCTION_EXAMPLES[func_name], 1):
            print(f"  {i}. {example.get('command', 'N/A')}")

    print()

def main():
    parser = argparse.ArgumentParser(
        prog="test-wrapper-new",
        description="Sequential Thinking MCP Wrapper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=True,
        epilog="""
PROGRESSIVE HELP LEVELS:
  Level 1: --help                    Quick overview
  Level 2: list                      List all functions
           info FUNCTION              Full documentation
           example FUNCTION           Working examples
  Level 3: FUNCTION --help           Complete reference (LEVEL 4)

EXAMPLES:
  uv run test-wrapper-new.py --help
  uv run test-wrapper-new.py list
  uv run test-wrapper-new.py info sequentialthinking
  uv run test-wrapper-new.py example sequentialthinking
  uv run test-wrapper-new.py sequentialthinking --help

OUTPUT FORMATS:
  --format text                      Human-readable (default)
  --format json                      Machine-readable
  --format table                     Table format (when applicable)
        """
    )

    # Global options
    parser.add_argument(
        "--format",
        choices=["text", "json", "table"],
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

    # Level 2/3: example
    example_parser = subparsers.add_parser("example", help="Show examples")
    example_parser.add_argument("function", help="Function name")

    # Level 4: Dynamic function subparsers
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
                        required=param.get('required', False)
                    )

    args = parser.parse_args()

    # Validate credentials
    if not validate_credentials() and args.command and args.command not in ["list", "info", "example", "help"]:
        print("✗ Error: Required credentials not configured", file=sys.stderr)
        print("Please set required environment variables", file=sys.stderr)
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
            # Level 4: function-specific execution
            show_function_help(args.command)
        else:
            parser.print_help()
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n✗ Interrupted", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"✗ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
