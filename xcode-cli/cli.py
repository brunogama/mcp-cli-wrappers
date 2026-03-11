#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "click>=8.1.0",
#     "rich>=13.0.0",
#     "httpx>=0.27.0",
#     "pydantic>=2.0.0",
#     "python-dotenv>=1.0.0",
# ]
# ///
"""
XcodeMCP CLI Wrapper - Control Xcode through Model Context Protocol

A progressive-disclosure CLI for XcodeMCP server providing project management,
build operations, testing, and XCResult analysis capabilities.

MCP Server: https://github.com/lapfelix/XcodeMCP
"""

import json
import os
import subprocess
import sys
from typing import Any, Optional

import click
from dotenv import load_dotenv
from rich.console import Console

# Load environment variables from script directory (.env first, then .env.local overrides)
_script_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(_script_dir, ".env"))
load_dotenv(os.path.join(_script_dir, ".env.local"), override=True)
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()

# =============================================================================
# FUNCTION DEFINITIONS
# =============================================================================

FUNCTION_INFO = {
    # Project Management
    "xcode_open_project": {
        "description": "Opens an Xcode project or workspace",
        "category": "Project Management",
        "parameters": {
            "xcodeproj": {"type": "string", "required": True, "description": "Absolute path to the .xcodeproj or .xcworkspace file"}
        },
        "returns": "Confirmation of project opening",
        "related": ["xcode_close_project", "xcode_refresh_project", "xcode_get_workspace_info"]
    },
    "xcode_close_project": {
        "description": "Closes the currently active Xcode project or workspace",
        "category": "Project Management",
        "parameters": {
            "xcodeproj": {"type": "string", "required": True, "description": "Absolute path to the .xcodeproj or .xcworkspace file"}
        },
        "returns": "Confirmation of project closure",
        "related": ["xcode_open_project", "xcode_refresh_project"]
    },
    "xcode_get_workspace_info": {
        "description": "Retrieves status and details of the workspace",
        "category": "Project Management",
        "parameters": {
            "xcodeproj": {"type": "string", "required": True, "description": "Absolute path to the .xcodeproj or .xcworkspace file"}
        },
        "returns": "Workspace details including projects, schemes, and status",
        "related": ["xcode_get_projects", "xcode_get_schemes"]
    },
    "xcode_get_projects": {
        "description": "Lists projects within a workspace",
        "category": "Project Management",
        "parameters": {
            "xcodeproj": {"type": "string", "required": True, "description": "Absolute path to the .xcodeproj or .xcworkspace file"}
        },
        "returns": "List of projects in the workspace",
        "related": ["xcode_get_workspace_info", "xcode_get_schemes"]
    },
    "xcode_open_file": {
        "description": "Opens a file in Xcode at an optional line number",
        "category": "Project Management",
        "parameters": {
            "file_path": {"type": "string", "required": True, "description": "Absolute path to the file"},
            "line_number": {"type": "number", "required": False, "description": "Line number to navigate to"}
        },
        "returns": "Confirmation of file opening",
        "related": ["xcode_open_project"]
    },
    "xcode_refresh_project": {
        "description": "Closes and reopens a project to refresh it",
        "category": "Project Management",
        "parameters": {
            "xcodeproj": {"type": "string", "required": True, "description": "Absolute path to the .xcodeproj or .xcworkspace file"}
        },
        "returns": "Confirmation of project refresh",
        "related": ["xcode_open_project", "xcode_close_project"]
    },
    # Build Operations
    "xcode_build": {
        "description": "Builds a specific Xcode project or workspace with a specified scheme",
        "category": "Build Operations",
        "parameters": {
            "xcodeproj": {"type": "string", "required": True, "description": "Absolute path to the .xcodeproj or .xcworkspace file"},
            "scheme": {"type": "string", "required": True, "description": "Name of the scheme to build"},
            "destination": {"type": "string", "required": False, "description": "Build destination (e.g., simulator, device)"}
        },
        "returns": "Build result including success/failure and any errors",
        "related": ["xcode_clean", "xcode_build_and_run", "xcode_get_schemes"]
    },
    "xcode_clean": {
        "description": "Cleans the build directory for a project",
        "category": "Build Operations",
        "parameters": {
            "xcodeproj": {"type": "string", "required": True, "description": "Absolute path to the .xcodeproj or .xcworkspace file"}
        },
        "returns": "Confirmation of clean operation",
        "related": ["xcode_build"]
    },
    "xcode_test": {
        "description": "Runs tests for a project with optional arguments",
        "category": "Build Operations",
        "parameters": {
            "xcodeproj": {"type": "string", "required": True, "description": "Absolute path to the .xcodeproj or .xcworkspace file"},
            "destination": {"type": "string", "required": True, "description": "Simulator/device name"},
            "command_line_arguments": {"type": "array", "required": False, "description": "Additional command line arguments"},
            "test_plan_path": {"type": "string", "required": False, "description": "Path to test plan"},
            "selected_tests": {"type": "array", "required": False, "description": "Specific tests to run"},
            "selected_test_classes": {"type": "array", "required": False, "description": "Specific test classes to run"},
            "test_target_identifier": {"type": "string", "required": False, "description": "Test target identifier"},
            "test_target_name": {"type": "string", "required": False, "description": "Test target name"}
        },
        "returns": "Test results including pass/fail counts",
        "related": ["xcode_get_test_targets", "find_xcresults", "xcresult_summary"]
    },
    "xcode_build_and_run": {
        "description": "Builds and runs the active scheme",
        "category": "Build Operations",
        "parameters": {
            "xcodeproj": {"type": "string", "required": True, "description": "Absolute path to the .xcodeproj or .xcworkspace file"},
            "scheme": {"type": "string", "required": True, "description": "Build scheme name"},
            "command_line_arguments": {"type": "array", "required": False, "description": "Additional command line arguments"}
        },
        "returns": "Build and run status",
        "related": ["xcode_build", "xcode_debug", "xcode_stop"]
    },
    "xcode_debug": {
        "description": "Starts a debugging session",
        "category": "Build Operations",
        "parameters": {
            "xcodeproj": {"type": "string", "required": True, "description": "Absolute path to the .xcodeproj or .xcworkspace file"},
            "scheme": {"type": "string", "required": True, "description": "Build scheme name"},
            "skip_building": {"type": "boolean", "required": False, "description": "Whether to skip building"}
        },
        "returns": "Debug session status",
        "related": ["xcode_build_and_run", "xcode_stop"]
    },
    "xcode_stop": {
        "description": "Stops the current operation",
        "category": "Build Operations",
        "parameters": {
            "xcodeproj": {"type": "string", "required": True, "description": "Absolute path to the .xcodeproj or .xcworkspace file"}
        },
        "returns": "Confirmation of stop operation",
        "related": ["xcode_build_and_run", "xcode_debug"]
    },
    "find_xcresults": {
        "description": "Finds all XCResult files for a project",
        "category": "Build Operations",
        "parameters": {
            "xcodeproj": {"type": "string", "required": True, "description": "Absolute path to the .xcodeproj or .xcworkspace file"}
        },
        "returns": "List of XCResult file paths",
        "related": ["xcresult_summary", "xcresult_browse"]
    },
    # Configuration
    "xcode_get_schemes": {
        "description": "Lists available schemes for a project",
        "category": "Configuration",
        "parameters": {
            "xcodeproj": {"type": "string", "required": True, "description": "Absolute path to the .xcodeproj or .xcworkspace file"}
        },
        "returns": "List of available schemes",
        "related": ["xcode_set_active_scheme", "xcode_build"]
    },
    "xcode_set_active_scheme": {
        "description": "Switches the active scheme for a project",
        "category": "Configuration",
        "parameters": {
            "xcodeproj": {"type": "string", "required": True, "description": "Absolute path to the .xcodeproj or .xcworkspace file"},
            "scheme_name": {"type": "string", "required": True, "description": "Name of the scheme to activate"}
        },
        "returns": "Confirmation of scheme change",
        "related": ["xcode_get_schemes"]
    },
    "xcode_get_run_destinations": {
        "description": "Lists available simulators and devices",
        "category": "Configuration",
        "parameters": {
            "xcodeproj": {"type": "string", "required": True, "description": "Absolute path to the .xcodeproj or .xcworkspace file"}
        },
        "returns": "List of available run destinations",
        "related": ["xcode_build", "xcode_test"]
    },
    "xcode_get_test_targets": {
        "description": "Gets information about test targets in a project",
        "category": "Configuration",
        "parameters": {
            "xcodeproj": {"type": "string", "required": True, "description": "Absolute path to the .xcodeproj or .xcworkspace file"}
        },
        "returns": "List of test targets with details",
        "related": ["xcode_test"]
    },
    # XCResult Analysis
    "xcresult_browse": {
        "description": "Browses test results and analyzes failures",
        "category": "XCResult Analysis",
        "parameters": {
            "xcresult_path": {"type": "string", "required": True, "description": "Absolute path to the .xcresult file"},
            "test_id": {"type": "string", "required": False, "description": "Test ID or index number"},
            "include_console": {"type": "boolean", "required": False, "description": "Whether to include console output"}
        },
        "returns": "Test results with optional failure details",
        "related": ["xcresult_summary", "xcresult_browser_get_console"]
    },
    "xcresult_browser_get_console": {
        "description": "Gets console output for specific tests",
        "category": "XCResult Analysis",
        "parameters": {
            "xcresult_path": {"type": "string", "required": True, "description": "Absolute path to the .xcresult file"},
            "test_id": {"type": "string", "required": True, "description": "Test ID or index number"}
        },
        "returns": "Console output for the specified test",
        "related": ["xcresult_browse"]
    },
    "xcresult_summary": {
        "description": "Provides a quick overview of test results",
        "category": "XCResult Analysis",
        "parameters": {
            "xcresult_path": {"type": "string", "required": True, "description": "Absolute path to the .xcresult file"}
        },
        "returns": "Summary including pass/fail counts and duration",
        "related": ["xcresult_browse", "find_xcresults"]
    },
    "xcresult_get_screenshot": {
        "description": "Extracts screenshots from test failures",
        "category": "XCResult Analysis",
        "parameters": {
            "xcresult_path": {"type": "string", "required": True, "description": "Absolute path to the .xcresult file"},
            "test_id": {"type": "string", "required": True, "description": "Test ID or index number"},
            "timestamp": {"type": "number", "required": True, "description": "Seconds offset in test"}
        },
        "returns": "Screenshot data or file path",
        "related": ["xcresult_list_attachments", "xcresult_export_attachment"]
    },
    "xcresult_get_ui_hierarchy": {
        "description": "Gets UI hierarchy as AI-readable JSON",
        "category": "XCResult Analysis",
        "parameters": {
            "xcresult_path": {"type": "string", "required": True, "description": "Absolute path to the .xcresult file"},
            "test_id": {"type": "string", "required": True, "description": "Test ID or index number"},
            "timestamp": {"type": "number", "required": False, "description": "Seconds offset in test"},
            "full_hierarchy": {"type": "boolean", "required": False, "description": "Include full hierarchy"},
            "raw_format": {"type": "boolean", "required": False, "description": "Use raw format"}
        },
        "returns": "UI hierarchy in JSON format",
        "related": ["xcresult_get_ui_element"]
    },
    "xcresult_get_ui_element": {
        "description": "Gets detailed properties of specific UI elements by index",
        "category": "XCResult Analysis",
        "parameters": {
            "hierarchy_json_path": {"type": "string", "required": True, "description": "Absolute path to the UI hierarchy JSON file"},
            "element_index": {"type": "number", "required": True, "description": "Index of the element"},
            "include_children": {"type": "boolean", "required": False, "description": "Whether to include children"}
        },
        "returns": "UI element details",
        "related": ["xcresult_get_ui_hierarchy"]
    },
    "xcresult_list_attachments": {
        "description": "Lists all attachments for a test",
        "category": "XCResult Analysis",
        "parameters": {
            "xcresult_path": {"type": "string", "required": True, "description": "Absolute path to the .xcresult file"},
            "test_id": {"type": "string", "required": True, "description": "Test ID or index number"}
        },
        "returns": "List of attachments with metadata",
        "related": ["xcresult_export_attachment", "xcresult_get_screenshot"]
    },
    "xcresult_export_attachment": {
        "description": "Exports specific attachments from test results",
        "category": "XCResult Analysis",
        "parameters": {
            "xcresult_path": {"type": "string", "required": True, "description": "Absolute path to the .xcresult file"},
            "test_id": {"type": "string", "required": True, "description": "Test ID or index number"},
            "attachment_id": {"type": "string", "required": True, "description": "Attachment ID to export"},
            "output_path": {"type": "string", "required": False, "description": "Output file path"}
        },
        "returns": "Exported file path",
        "related": ["xcresult_list_attachments"]
    },
}

FUNCTION_EXAMPLES = {
    "xcode_open_project": [
        {
            "description": "Open an Xcode project",
            "command": 'uv run cli.py xcode_open_project --xcodeproj /path/to/MyApp.xcodeproj',
            "output": '{"success": true, "message": "Project opened successfully"}'
        },
        {
            "description": "Open an Xcode workspace",
            "command": 'uv run cli.py xcode_open_project --xcodeproj /path/to/MyApp.xcworkspace',
            "output": '{"success": true, "message": "Workspace opened successfully"}'
        }
    ],
    "xcode_build": [
        {
            "description": "Build a scheme",
            "command": 'uv run cli.py xcode_build --xcodeproj /path/to/MyApp.xcodeproj --scheme "MyApp"',
            "output": '{"success": true, "build_time": 45.2, "warnings": 0, "errors": 0}'
        },
        {
            "description": "Build for a specific simulator",
            "command": 'uv run cli.py xcode_build --xcodeproj /path/to/MyApp.xcodeproj --scheme "MyApp" --destination "iPhone 15 Pro"',
            "output": '{"success": true, "build_time": 52.1, "destination": "iPhone 15 Pro"}'
        }
    ],
    "xcode_test": [
        {
            "description": "Run all tests",
            "command": 'uv run cli.py xcode_test --xcodeproj /path/to/MyApp.xcodeproj --destination "iPhone 15 Pro"',
            "output": '{"success": true, "passed": 42, "failed": 0, "skipped": 2}'
        },
        {
            "description": "Run specific test class",
            "command": 'uv run cli.py xcode_test --xcodeproj /path/to/MyApp.xcodeproj --destination "iPhone 15" --selected-test-classes "MyAppTests.LoginTests"',
            "output": '{"success": true, "passed": 8, "failed": 0}'
        }
    ],
    "xcode_get_schemes": [
        {
            "description": "List all schemes",
            "command": 'uv run cli.py xcode_get_schemes --xcodeproj /path/to/MyApp.xcodeproj',
            "output": '{"schemes": ["MyApp", "MyAppTests", "MyAppUITests"]}'
        }
    ],
    "xcresult_summary": [
        {
            "description": "Get test result summary",
            "command": 'uv run cli.py xcresult_summary --xcresult-path /path/to/Test.xcresult',
            "output": '{"total": 50, "passed": 48, "failed": 2, "duration": 120.5}'
        }
    ],
    "xcresult_browse": [
        {
            "description": "Browse test results",
            "command": 'uv run cli.py xcresult_browse --xcresult-path /path/to/Test.xcresult',
            "output": '{"tests": [{"name": "testLogin", "status": "passed"}, ...]}'
        },
        {
            "description": "Get specific test with console output",
            "command": 'uv run cli.py xcresult_browse --xcresult-path /path/to/Test.xcresult --test-id 0 --include-console',
            "output": '{"name": "testLogin", "status": "failed", "console": "..."}'
        }
    ],
    "find_xcresults": [
        {
            "description": "Find all test results",
            "command": 'uv run cli.py find_xcresults --xcodeproj /path/to/MyApp.xcodeproj',
            "output": '{"xcresults": ["/path/to/DerivedData/MyApp/Logs/Test/Test-2024.xcresult"]}'
        }
    ],
    "xcode_get_run_destinations": [
        {
            "description": "List available simulators and devices",
            "command": 'uv run cli.py xcode_get_run_destinations --xcodeproj /path/to/MyApp.xcodeproj',
            "output": '{"destinations": [{"name": "iPhone 15 Pro", "type": "simulator"}, ...]}'
        }
    ],
}

QUICK_HELP = """
XcodeMCP CLI - Control Xcode through Model Context Protocol

USAGE:
  uv run cli.py COMMAND [OPTIONS]
  uv run cli.py --help              Quick overview (this)
  uv run cli.py list                List all functions
  uv run cli.py info FUNCTION       Detailed function docs
  uv run cli.py example FUNCTION    Working examples

CATEGORIES:
  Project Management    Open, close, refresh projects
  Build Operations      Build, test, debug, run
  Configuration         Schemes, destinations, targets
  XCResult Analysis     Browse and analyze test results

QUICK START:
  # List schemes in a project
  uv run cli.py xcode_get_schemes --xcodeproj /path/to/MyApp.xcodeproj

  # Build a project
  uv run cli.py xcode_build --xcodeproj /path/to/MyApp.xcodeproj --scheme MyApp

  # Run tests
  uv run cli.py xcode_test --xcodeproj /path/to/MyApp.xcodeproj --destination "iPhone 15"

  # Get test results summary
  uv run cli.py xcresult_summary --xcresult-path /path/to/Test.xcresult

For detailed function docs: uv run cli.py info FUNCTION_NAME
"""

# =============================================================================
# MCP COMMUNICATION
# =============================================================================

def call_mcp_tool(tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    """Call an MCP tool via the XcodeMCP server."""
    # Filter out None values from arguments
    arguments = {k: v for k, v in arguments.items() if v is not None}

    # Build the MCP call
    mcp_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        }
    }

    try:
        # Use claude mcp call to invoke the tool
        result = subprocess.run(
            ["claude", "mcp", "call", "xcode-mcp", tool_name, json.dumps(arguments)],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout for long builds
        )

        if result.returncode != 0:
            return {
                "success": False,
                "error": result.stderr or "MCP call failed",
                "tool": tool_name
            }

        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return {
                "success": True,
                "result": result.stdout
            }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Operation timed out after 300 seconds",
            "tool": tool_name
        }
    except FileNotFoundError:
        return {
            "success": False,
            "error": "Claude CLI not found. Ensure 'claude' is installed and in PATH.",
            "tool": tool_name
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "tool": tool_name
        }


def format_output(data: Any, output_format: str) -> None:
    """Format and print output based on format preference."""
    if output_format == "json":
        console.print_json(json.dumps(data, indent=2, default=str))
    elif output_format == "table" and isinstance(data, (list, dict)):
        if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
            table = Table()
            for key in data[0].keys():
                table.add_column(key)
            for item in data:
                table.add_row(*[str(v) for v in item.values()])
            console.print(table)
        elif isinstance(data, dict):
            table = Table(show_header=False)
            table.add_column("Key", style="cyan")
            table.add_column("Value")
            for k, v in data.items():
                table.add_row(str(k), str(v))
            console.print(table)
        else:
            console.print(data)
    else:
        console.print(data)


# =============================================================================
# CLI COMMANDS
# =============================================================================

@click.group(invoke_without_command=True)
@click.option('--format', 'output_format', type=click.Choice(['json', 'text', 'table']), default='json', help='Output format')
@click.option('--verbose', is_flag=True, help='Verbose output')
@click.pass_context
def cli(ctx, output_format, verbose):
    """XcodeMCP CLI - Control Xcode through Model Context Protocol

    Run 'uv run cli.py list' to see all available functions.
    Run 'uv run cli.py info FUNCTION' for detailed documentation.
    Run 'uv run cli.py example FUNCTION' for working examples.
    """
    ctx.ensure_object(dict)
    ctx.obj['format'] = output_format
    ctx.obj['verbose'] = verbose

    if ctx.invoked_subcommand is None:
        console.print(QUICK_HELP)


@cli.command()
def list():
    """List all available functions organized by category."""
    categories = {}
    for func_name, info in FUNCTION_INFO.items():
        cat = info.get("category", "Other")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append((func_name, info["description"]))

    console.print("\n[bold]Available Functions[/bold]\n")

    for category, functions in categories.items():
        console.print(f"[bold cyan]{category}[/bold cyan]")
        for name, desc in sorted(functions):
            console.print(f"  [green]{name}[/green] - {desc}")
        console.print()

    console.print("[dim]Use 'uv run cli.py info FUNCTION' for detailed documentation[/dim]")
    console.print("[dim]Use 'uv run cli.py example FUNCTION' for working examples[/dim]")


@cli.command()
@click.argument('function_name')
def info(function_name):
    """Get detailed information about a function."""
    if function_name not in FUNCTION_INFO:
        console.print(f"[red]Unknown function: {function_name}[/red]")
        console.print(f"Run 'uv run cli.py list' to see available functions")
        sys.exit(1)

    func = FUNCTION_INFO[function_name]

    console.print(f"\n[bold cyan]{function_name}[/bold cyan]")
    console.print(f"[dim]{func['category']}[/dim]\n")
    console.print(f"{func['description']}\n")

    console.print("[bold]Parameters:[/bold]")
    for param, details in func["parameters"].items():
        req = "[red]*[/red]" if details.get("required") else ""
        console.print(f"  --{param.replace('_', '-')} {req}")
        console.print(f"    Type: {details['type']}")
        console.print(f"    {details['description']}")

    console.print(f"\n[bold]Returns:[/bold] {func['returns']}")

    if func.get("related"):
        console.print(f"\n[bold]Related:[/bold] {', '.join(func['related'])}")

    console.print(f"\n[dim]Use 'uv run cli.py example {function_name}' for examples[/dim]")


@cli.command()
@click.argument('function_name')
def example(function_name):
    """Show working examples for a function."""
    if function_name not in FUNCTION_EXAMPLES:
        console.print(f"[yellow]No examples available for: {function_name}[/yellow]")
        if function_name in FUNCTION_INFO:
            console.print(f"Run 'uv run cli.py info {function_name}' for documentation")
        else:
            console.print("Run 'uv run cli.py list' to see available functions")
        sys.exit(1)

    examples = FUNCTION_EXAMPLES[function_name]

    console.print(f"\n[bold cyan]Examples: {function_name}[/bold cyan]\n")

    for i, ex in enumerate(examples, 1):
        console.print(f"[bold]Example {i}:[/bold] {ex['description']}")
        console.print(f"[green]$ {ex['command']}[/green]")
        console.print(f"[dim]{ex['output']}[/dim]\n")


# =============================================================================
# PROJECT MANAGEMENT COMMANDS
# =============================================================================

@cli.command()
@click.option('--xcodeproj', required=True, help='Absolute path to .xcodeproj or .xcworkspace')
@click.pass_context
def xcode_open_project(ctx, xcodeproj):
    """Open an Xcode project or workspace."""
    result = call_mcp_tool("xcode_open_project", {"xcodeproj": xcodeproj})
    format_output(result, ctx.obj['format'])


@cli.command()
@click.option('--xcodeproj', required=True, help='Absolute path to .xcodeproj or .xcworkspace')
@click.pass_context
def xcode_close_project(ctx, xcodeproj):
    """Close the currently active Xcode project."""
    result = call_mcp_tool("xcode_close_project", {"xcodeproj": xcodeproj})
    format_output(result, ctx.obj['format'])


@cli.command()
@click.option('--xcodeproj', required=True, help='Absolute path to .xcodeproj or .xcworkspace')
@click.pass_context
def xcode_get_workspace_info(ctx, xcodeproj):
    """Get workspace status and details."""
    result = call_mcp_tool("xcode_get_workspace_info", {"xcodeproj": xcodeproj})
    format_output(result, ctx.obj['format'])


@cli.command()
@click.option('--xcodeproj', required=True, help='Absolute path to .xcodeproj or .xcworkspace')
@click.pass_context
def xcode_get_projects(ctx, xcodeproj):
    """List projects within a workspace."""
    result = call_mcp_tool("xcode_get_projects", {"xcodeproj": xcodeproj})
    format_output(result, ctx.obj['format'])


@cli.command()
@click.option('--file-path', required=True, help='Absolute path to the file')
@click.option('--line-number', type=int, help='Line number to navigate to')
@click.pass_context
def xcode_open_file(ctx, file_path, line_number):
    """Open a file in Xcode."""
    result = call_mcp_tool("xcode_open_file", {
        "file_path": file_path,
        "line_number": line_number
    })
    format_output(result, ctx.obj['format'])


@cli.command()
@click.option('--xcodeproj', required=True, help='Absolute path to .xcodeproj or .xcworkspace')
@click.pass_context
def xcode_refresh_project(ctx, xcodeproj):
    """Close and reopen a project to refresh it."""
    result = call_mcp_tool("xcode_refresh_project", {"xcodeproj": xcodeproj})
    format_output(result, ctx.obj['format'])


# =============================================================================
# BUILD OPERATIONS COMMANDS
# =============================================================================

@cli.command()
@click.option('--xcodeproj', required=True, help='Absolute path to .xcodeproj or .xcworkspace')
@click.option('--scheme', required=True, help='Name of the scheme to build')
@click.option('--destination', help='Build destination (e.g., simulator, device)')
@click.pass_context
def xcode_build(ctx, xcodeproj, scheme, destination):
    """Build a specific Xcode project or workspace."""
    result = call_mcp_tool("xcode_build", {
        "xcodeproj": xcodeproj,
        "scheme": scheme,
        "destination": destination
    })
    format_output(result, ctx.obj['format'])


@cli.command()
@click.option('--xcodeproj', required=True, help='Absolute path to .xcodeproj or .xcworkspace')
@click.pass_context
def xcode_clean(ctx, xcodeproj):
    """Clean the build directory for a project."""
    result = call_mcp_tool("xcode_clean", {"xcodeproj": xcodeproj})
    format_output(result, ctx.obj['format'])


@cli.command()
@click.option('--xcodeproj', required=True, help='Absolute path to .xcodeproj or .xcworkspace')
@click.option('--destination', required=True, help='Simulator/device name')
@click.option('--command-line-arguments', multiple=True, help='Additional command line arguments')
@click.option('--test-plan-path', help='Path to test plan')
@click.option('--selected-tests', multiple=True, help='Specific tests to run')
@click.option('--selected-test-classes', multiple=True, help='Specific test classes to run')
@click.option('--test-target-identifier', help='Test target identifier')
@click.option('--test-target-name', help='Test target name')
@click.pass_context
def xcode_test(ctx, xcodeproj, destination, command_line_arguments, test_plan_path,
               selected_tests, selected_test_classes, test_target_identifier, test_target_name):
    """Run tests for a project."""
    result = call_mcp_tool("xcode_test", {
        "xcodeproj": xcodeproj,
        "destination": destination,
        "command_line_arguments": list(command_line_arguments) if command_line_arguments else None,
        "test_plan_path": test_plan_path,
        "selected_tests": list(selected_tests) if selected_tests else None,
        "selected_test_classes": list(selected_test_classes) if selected_test_classes else None,
        "test_target_identifier": test_target_identifier,
        "test_target_name": test_target_name
    })
    format_output(result, ctx.obj['format'])


@cli.command()
@click.option('--xcodeproj', required=True, help='Absolute path to .xcodeproj or .xcworkspace')
@click.option('--scheme', required=True, help='Build scheme name')
@click.option('--command-line-arguments', multiple=True, help='Additional command line arguments')
@click.pass_context
def xcode_build_and_run(ctx, xcodeproj, scheme, command_line_arguments):
    """Build and run the active scheme."""
    result = call_mcp_tool("xcode_build_and_run", {
        "xcodeproj": xcodeproj,
        "scheme": scheme,
        "command_line_arguments": list(command_line_arguments) if command_line_arguments else None
    })
    format_output(result, ctx.obj['format'])


@cli.command()
@click.option('--xcodeproj', required=True, help='Absolute path to .xcodeproj or .xcworkspace')
@click.option('--scheme', required=True, help='Build scheme name')
@click.option('--skip-building', is_flag=True, help='Skip building before debugging')
@click.pass_context
def xcode_debug(ctx, xcodeproj, scheme, skip_building):
    """Start a debugging session."""
    result = call_mcp_tool("xcode_debug", {
        "xcodeproj": xcodeproj,
        "scheme": scheme,
        "skip_building": skip_building if skip_building else None
    })
    format_output(result, ctx.obj['format'])


@cli.command()
@click.option('--xcodeproj', required=True, help='Absolute path to .xcodeproj or .xcworkspace')
@click.pass_context
def xcode_stop(ctx, xcodeproj):
    """Stop the current operation."""
    result = call_mcp_tool("xcode_stop", {"xcodeproj": xcodeproj})
    format_output(result, ctx.obj['format'])


@cli.command()
@click.option('--xcodeproj', required=True, help='Absolute path to .xcodeproj or .xcworkspace')
@click.pass_context
def find_xcresults(ctx, xcodeproj):
    """Find all XCResult files for a project."""
    result = call_mcp_tool("find_xcresults", {"xcodeproj": xcodeproj})
    format_output(result, ctx.obj['format'])


# =============================================================================
# CONFIGURATION COMMANDS
# =============================================================================

@cli.command()
@click.option('--xcodeproj', required=True, help='Absolute path to .xcodeproj or .xcworkspace')
@click.pass_context
def xcode_get_schemes(ctx, xcodeproj):
    """List available schemes for a project."""
    result = call_mcp_tool("xcode_get_schemes", {"xcodeproj": xcodeproj})
    format_output(result, ctx.obj['format'])


@cli.command()
@click.option('--xcodeproj', required=True, help='Absolute path to .xcodeproj or .xcworkspace')
@click.option('--scheme-name', required=True, help='Name of the scheme to activate')
@click.pass_context
def xcode_set_active_scheme(ctx, xcodeproj, scheme_name):
    """Switch the active scheme for a project."""
    result = call_mcp_tool("xcode_set_active_scheme", {
        "xcodeproj": xcodeproj,
        "scheme_name": scheme_name
    })
    format_output(result, ctx.obj['format'])


@cli.command()
@click.option('--xcodeproj', required=True, help='Absolute path to .xcodeproj or .xcworkspace')
@click.pass_context
def xcode_get_run_destinations(ctx, xcodeproj):
    """List available simulators and devices."""
    result = call_mcp_tool("xcode_get_run_destinations", {"xcodeproj": xcodeproj})
    format_output(result, ctx.obj['format'])


@cli.command()
@click.option('--xcodeproj', required=True, help='Absolute path to .xcodeproj or .xcworkspace')
@click.pass_context
def xcode_get_test_targets(ctx, xcodeproj):
    """Get information about test targets in a project."""
    result = call_mcp_tool("xcode_get_test_targets", {"xcodeproj": xcodeproj})
    format_output(result, ctx.obj['format'])


# =============================================================================
# XCRESULT ANALYSIS COMMANDS
# =============================================================================

@cli.command()
@click.option('--xcresult-path', required=True, help='Absolute path to .xcresult file')
@click.option('--test-id', help='Test ID or index number')
@click.option('--include-console', is_flag=True, help='Include console output')
@click.pass_context
def xcresult_browse(ctx, xcresult_path, test_id, include_console):
    """Browse test results and analyze failures."""
    result = call_mcp_tool("xcresult_browse", {
        "xcresult_path": xcresult_path,
        "test_id": test_id,
        "include_console": include_console if include_console else None
    })
    format_output(result, ctx.obj['format'])


@cli.command()
@click.option('--xcresult-path', required=True, help='Absolute path to .xcresult file')
@click.option('--test-id', required=True, help='Test ID or index number')
@click.pass_context
def xcresult_browser_get_console(ctx, xcresult_path, test_id):
    """Get console output for specific tests."""
    result = call_mcp_tool("xcresult_browser_get_console", {
        "xcresult_path": xcresult_path,
        "test_id": test_id
    })
    format_output(result, ctx.obj['format'])


@cli.command()
@click.option('--xcresult-path', required=True, help='Absolute path to .xcresult file')
@click.pass_context
def xcresult_summary(ctx, xcresult_path):
    """Get a quick overview of test results."""
    result = call_mcp_tool("xcresult_summary", {"xcresult_path": xcresult_path})
    format_output(result, ctx.obj['format'])


@cli.command()
@click.option('--xcresult-path', required=True, help='Absolute path to .xcresult file')
@click.option('--test-id', required=True, help='Test ID or index number')
@click.option('--timestamp', required=True, type=float, help='Seconds offset in test')
@click.pass_context
def xcresult_get_screenshot(ctx, xcresult_path, test_id, timestamp):
    """Extract screenshots from test failures."""
    result = call_mcp_tool("xcresult_get_screenshot", {
        "xcresult_path": xcresult_path,
        "test_id": test_id,
        "timestamp": timestamp
    })
    format_output(result, ctx.obj['format'])


@cli.command()
@click.option('--xcresult-path', required=True, help='Absolute path to .xcresult file')
@click.option('--test-id', required=True, help='Test ID or index number')
@click.option('--timestamp', type=float, help='Seconds offset in test')
@click.option('--full-hierarchy', is_flag=True, help='Include full hierarchy')
@click.option('--raw-format', is_flag=True, help='Use raw format')
@click.pass_context
def xcresult_get_ui_hierarchy(ctx, xcresult_path, test_id, timestamp, full_hierarchy, raw_format):
    """Get UI hierarchy as AI-readable JSON."""
    result = call_mcp_tool("xcresult_get_ui_hierarchy", {
        "xcresult_path": xcresult_path,
        "test_id": test_id,
        "timestamp": timestamp,
        "full_hierarchy": full_hierarchy if full_hierarchy else None,
        "raw_format": raw_format if raw_format else None
    })
    format_output(result, ctx.obj['format'])


@cli.command()
@click.option('--hierarchy-json-path', required=True, help='Absolute path to UI hierarchy JSON file')
@click.option('--element-index', required=True, type=int, help='Index of the element')
@click.option('--include-children', is_flag=True, help='Include children')
@click.pass_context
def xcresult_get_ui_element(ctx, hierarchy_json_path, element_index, include_children):
    """Get detailed properties of specific UI elements."""
    result = call_mcp_tool("xcresult_get_ui_element", {
        "hierarchy_json_path": hierarchy_json_path,
        "element_index": element_index,
        "include_children": include_children if include_children else None
    })
    format_output(result, ctx.obj['format'])


@cli.command()
@click.option('--xcresult-path', required=True, help='Absolute path to .xcresult file')
@click.option('--test-id', required=True, help='Test ID or index number')
@click.pass_context
def xcresult_list_attachments(ctx, xcresult_path, test_id):
    """List all attachments for a test."""
    result = call_mcp_tool("xcresult_list_attachments", {
        "xcresult_path": xcresult_path,
        "test_id": test_id
    })
    format_output(result, ctx.obj['format'])


@cli.command()
@click.option('--xcresult-path', required=True, help='Absolute path to .xcresult file')
@click.option('--test-id', required=True, help='Test ID or index number')
@click.option('--attachment-id', required=True, help='Attachment ID to export')
@click.option('--output-path', help='Output file path')
@click.pass_context
def xcresult_export_attachment(ctx, xcresult_path, test_id, attachment_id, output_path):
    """Export specific attachments from test results."""
    result = call_mcp_tool("xcresult_export_attachment", {
        "xcresult_path": xcresult_path,
        "test_id": test_id,
        "attachment_id": attachment_id,
        "output_path": output_path
    })
    format_output(result, ctx.obj['format'])


if __name__ == "__main__":
    cli()
