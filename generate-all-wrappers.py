#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "jinja2>=3.0",
# ]
# ///
"""
Master script to generate CLI wrappers from MCP definitions.
Uses Jinja2 templates for flexible code generation.

Usage:
  uv run generate-all-wrappers.py

Environment Variables:
  WRAPPERS_OUTPUT_DIR - Output directory for generated wrappers (default: script directory)
"""

import json
import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

MCP_DEFINITIONS = {
    "crawl4ai": {
        "command": "uv --directory /Users/bruno/Developer/crawl4ai-mcp run main.py",
        "type": "stdio",
        "functions": [
            {"name": "scrape", "description": "Scrape a single webpage"},
            {"name": "crawl", "description": "Crawl multiple pages on website"},
            {"name": "extract", "description": "Extract structured data"}
        ]
    },
    "ref": {
        "command": "https://api.ref.tools/mcp?apiKey=ref-fb8a5211ed4144376a89",
        "type": "http",
        "functions": [
            {"name": "search_documentation", "description": "Search documentation"},
            {"name": "read_url", "description": "Read documentation content"}
        ]
    },
    "repomix": {
        "command": "npx -y repomix --mcp",
        "type": "stdio",
        "functions": [
            {"name": "pack_codebase", "description": "Pack local codebase"},
            {"name": "pack_remote_repository", "description": "Pack GitHub repository"},
            {"name": "generate_skill", "description": "Generate Claude skill"},
            {"name": "attach_packed_output", "description": "Attach packed output"},
            {"name": "grep_repomix_output", "description": "Search content"}
        ]
    },
    "deepwiki": {
        "command": "https://mcp.deepwiki.com/mcp",
        "type": "http",
        "functions": [
            {"name": "read_wiki_structure", "description": "Get documentation topics"},
            {"name": "read_wiki_contents", "description": "Read full documentation"},
            {"name": "ask_question", "description": "Ask about repository"}
        ]
    },
    "firecrawl": {
        "command": "npx -y firecrawl-mcp",
        "type": "stdio",
        "functions": [
            {"name": "scrape", "description": "Scrape webpage"},
            {"name": "crawl", "description": "Crawl website"},
            {"name": "extract", "description": "Extract structured data"},
            {"name": "map", "description": "Map site URLs"},
            {"name": "search", "description": "Search web"}
        ]
    },
    "sequential-thinking": {
        "command": "bunx @modelcontextprotocol/server-sequential-thinking",
        "type": "stdio",
        "functions": [
            {"name": "sequentialthinking", "description": "Run sequential thinking process"}
        ]
    },
    "github": {
        "command": "bunx @modelcontextprotocol/server-github",
        "type": "stdio",
        "functions": [
            {"name": "create_pull_request", "description": "Create GitHub PR"},
            {"name": "create_issue", "description": "Create GitHub issue"},
            {"name": "search_repositories", "description": "Search repositories"},
            {"name": "list_issues", "description": "List issues"},
            {"name": "list_commits", "description": "List commits"},
            {"name": "create_or_update_file", "description": "Create/update files"},
            {"name": "push_files", "description": "Push files to repo"}
        ]
    },
    "semly": {
        "command": "semly mcp",
        "type": "stdio",
        "functions": [
            {"name": "outline", "description": "Generate code outline"},
            {"name": "explain", "description": "Explain code"},
            {"name": "list_indexed_projects", "description": "List projects"},
            {"name": "retrieve", "description": "Retrieve code chunks"},
            {"name": "locate", "description": "Find code"}
        ]
    },
    "claude-flow": {
        "command": "npx claude-flow@alpha mcp start",
        "type": "stdio",
        "functions": [
            {"name": "swarm_init", "description": "Initialize swarm"},
            {"name": "agent_spawn", "description": "Spawn agents"},
            {"name": "task_orchestrate", "description": "Orchestrate tasks"}
        ]
    },
    "flow-nexus": {
        "command": "npx flow-nexus@latest mcp start",
        "type": "stdio",
        "functions": [
            {"name": "swarm_init", "description": "Initialize swarm"},
            {"name": "swarm_scale", "description": "Scale swarm"},
            {"name": "agent_spawn", "description": "Spawn agents"},
            {"name": "sandbox_create", "description": "Create sandbox"},
            {"name": "sandbox_execute", "description": "Execute in sandbox"}
        ]
    }
}


def build_function_info(functions: list) -> str:
    """Build function info dictionary as Python code."""
    lines = []
    for func in functions:
        params = func.get('parameters', [])
        params_str = json.dumps(params) if params else "[]"
        lines.append(f'''    "{func['name']}": {{
        "description": "{func['description']}",
        "parameters": {params_str},
        "returns": {json.dumps(func.get('returns', 'Dict[str, Any]'))}
    }},''')
    return "\n".join(lines).rstrip(",")


def build_function_examples(functions: list) -> str:
    """Build function examples dictionary as Python code."""
    lines = []
    for func in functions:
        lines.append(f'''    "{func['name']}": [
        {{
            "title": "Example",
            "command": "uv run WRAPPER.py {func['name']}"
        }}
    ],''')
    return "\n".join(lines).rstrip(",")


def build_functions_list(functions: list) -> str:
    """Build formatted function list for help text."""
    lines = []
    for func in functions:
        lines.append(f"  {func['name']:30} {func['description']}")
    return "\n".join(lines)


def setup_jinja_environment():
    """Initialize Jinja2 environment with proper settings."""
    templates_dir = Path(__file__).parent / "templates"

    # Create templates directory if it doesn't exist
    templates_dir.mkdir(exist_ok=True)

    env = Environment(
        loader=FileSystemLoader(templates_dir),
        autoescape=False,  # Disabled: generating Python code, not HTML
        trim_blocks=True,
        lstrip_blocks=True
    )

    return env


def generate_wrapper(env, mcp_name: str, mcp_config: dict, output_dir: Path) -> None:
    """Generate a single wrapper using Jinja2 template."""
    filename = f"{mcp_name}.py"
    filepath = output_dir / filename

    title = mcp_name.replace("-", " ").title()
    functions = mcp_config.get("functions", [])

    # Prepare template context
    context = {
        "title": title,
        "filename": filename,
        "functions_list": build_functions_list(functions),
        "function_info": build_function_info(functions),
        "function_examples": build_function_examples(functions),
    }

    # Render template
    template = env.get_template("wrapper.jinja2")
    content = template.render(**context)

    # Write wrapper
    with open(filepath, "w") as f:
        f.write(content)

    # Make executable
    os.chmod(filepath, 0o755)

    print(f"✓ Generated: {filename}")


def main():
    """Main generator function."""
    # Get output directory
    output_dir_env = os.getenv("WRAPPERS_OUTPUT_DIR")
    output_dir = Path(output_dir_env) if output_dir_env else Path(__file__).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    # Setup Jinja2 environment
    try:
        env = setup_jinja_environment()
    except Exception as e:
        print(f"✗ Error setting up Jinja2 environment: {e}")
        return

    # Generate wrappers
    total = len(MCP_DEFINITIONS)
    for i, (mcp_name, mcp_config) in enumerate(MCP_DEFINITIONS.items(), 1):
        try:
            generate_wrapper(env, mcp_name, mcp_config, output_dir)
        except Exception as e:
            print(f"✗ Error generating {mcp_name}.py: {e}")

    print(f"\n✓ All {total} wrappers generated in {output_dir}")
    print(f"\nQuick start:")
    print(f"  cd {output_dir}")
    print(f"  uv run crawl4ai.py --help")
    print(f"\nEnvironment Variables:")
    print(f"  WRAPPERS_OUTPUT_DIR - Override output directory")


if __name__ == "__main__":
    main()
