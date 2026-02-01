#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "click>=8.0",
#     "httpx>=0.25.0",
#     "rich>=13.0",
#     "python-dotenv>=1.0.0",
# ]
# ///
"""
Perplexity AI CLI Wrapper

Progressive-disclosure CLI for the Perplexity MCP server providing AI-powered
web search, reasoning, and research capabilities through Sonar models.

Usage:
    uv run cli.py --help              # Quick overview
    uv run cli.py list                # All functions
    uv run cli.py info FUNCTION       # Detailed docs
    uv run cli.py example FUNCTION    # Working examples
    uv run cli.py FUNCTION --help     # Full reference
"""

import json
import os
import sys
from typing import Any, Optional

import click
import httpx
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

load_dotenv()

console = Console()

# =============================================================================
# QUICK HELP (Level 1) - ~30 tokens
# =============================================================================
QUICK_HELP = """
Perplexity AI CLI - Web search, reasoning & research via Sonar models

Available functions:
  ask        General-purpose AI with web search (sonar-pro)
  research   Deep comprehensive research (sonar-deep-research)
  reason     Advanced reasoning & analysis (sonar-reasoning-pro)
  search     Direct web search with ranked results

Quick start:
  uv run cli.py ask "What is the latest news on AI?"
  uv run cli.py search "Python 3.12 new features"
  uv run cli.py research "Compare REST vs GraphQL"

Next steps:
  uv run cli.py list              # See all functions
  uv run cli.py info ask          # Detailed docs for 'ask'
  uv run cli.py example search    # Working examples

Requires: PERPLEXITY_API_KEY environment variable
"""

# =============================================================================
# FUNCTION INFO (Level 2) - ~150 tokens each
# =============================================================================
FUNCTION_INFO = {
    "ask": """
## perplexity_ask

General-purpose conversational AI with real-time web search.

**Model**: sonar-pro
**Best for**: Quick questions, everyday searches, current information

### Parameters

| Name     | Type   | Required | Description                           |
|----------|--------|----------|---------------------------------------|
| query    | string | Yes      | Your question or search query         |
| system   | string | No       | System prompt to guide behavior       |
| context  | string | No       | Additional context for the query      |

### Returns
JSON object with:
- `response`: The AI-generated answer with citations
- `success`: Boolean indicating operation status

### Related Functions
- `research`: For deeper, more comprehensive analysis
- `reason`: For complex analytical and reasoning tasks
- `search`: For direct web search results without AI synthesis
""",
    "research": """
## perplexity_research

Deep, comprehensive research using the sonar-deep-research model.

**Model**: sonar-deep-research
**Best for**: Thorough analysis, detailed reports, academic research

### Parameters

| Name           | Type    | Required | Description                                    |
|----------------|---------|----------|------------------------------------------------|
| query          | string  | Yes      | Research topic or question                     |
| system         | string  | No       | System prompt to guide research focus          |
| context        | string  | No       | Additional context or constraints              |
| strip_thinking | boolean | No       | Remove <think> tags to save tokens (default: false) |

### Returns
JSON object with:
- `response`: Comprehensive research response with citations
- `success`: Boolean indicating operation status

### Notes
- May take longer than `ask` due to deep research
- Increase PERPLEXITY_TIMEOUT_MS for very long queries
- Use `strip_thinking=true` to reduce response size

### Related Functions
- `ask`: For quicker, lighter queries
- `reason`: For analytical and logical reasoning
""",
    "reason": """
## perplexity_reason

Advanced reasoning and problem-solving using sonar-reasoning-pro.

**Model**: sonar-reasoning-pro
**Best for**: Complex analysis, logical reasoning, problem-solving

### Parameters

| Name           | Type    | Required | Description                                    |
|----------------|---------|----------|------------------------------------------------|
| query          | string  | Yes      | Problem or question requiring reasoning        |
| system         | string  | No       | System prompt to guide reasoning approach      |
| context        | string  | No       | Additional context or constraints              |
| strip_thinking | boolean | No       | Remove <think> tags to save tokens (default: false) |

### Returns
JSON object with:
- `response`: Reasoned response with step-by-step analysis
- `success`: Boolean indicating operation status

### Notes
- Best for problems requiring logical deduction
- Shows reasoning process in <think> tags (unless stripped)
- Use for comparative analysis, decision-making, debugging

### Related Functions
- `ask`: For simpler queries not requiring deep reasoning
- `research`: For comprehensive information gathering
""",
    "search": """
## perplexity_search

Direct web search using the Perplexity Search API.

**Best for**: Finding current information, news, specific facts

### Parameters

| Name               | Type    | Required | Description                                    |
|--------------------|---------|----------|------------------------------------------------|
| query              | string  | Yes      | Search query string                            |
| max_results        | integer | No       | Number of results (1-20, default: 10)          |
| max_tokens_per_page| integer | No       | Tokens per webpage (256-2048, default: 1024)   |
| country            | string  | No       | ISO country code for regional results (e.g., US) |

### Returns
JSON object with:
- `results`: Formatted search results with titles, URLs, snippets
- `success`: Boolean indicating operation status

### Notes
- Returns raw search results, not AI-synthesized answers
- Use `country` parameter for localized results
- Adjust `max_tokens_per_page` for more/less content per result

### Related Functions
- `ask`: For AI-synthesized answers from search results
- `research`: For deep analysis of search topics
""",
    "list": """
## list

Display all available functions in this CLI wrapper.

### Usage
```bash
uv run cli.py list
```

### Output
Table showing all functions with brief descriptions.
""",
    "info": """
## info

Get detailed documentation for a specific function.

### Usage
```bash
uv run cli.py info FUNCTION_NAME
```

### Parameters
| Name     | Type   | Required | Description              |
|----------|--------|----------|--------------------------|
| function | string | Yes      | Name of function to describe |

### Output
Detailed markdown documentation including parameters, returns, and notes.
""",
    "example": """
## example

Show working examples for a specific function.

### Usage
```bash
uv run cli.py example FUNCTION_NAME
```

### Parameters
| Name     | Type   | Required | Description              |
|----------|--------|----------|--------------------------|
| function | string | Yes      | Name of function to show examples for |

### Output
2-3 real, copy-paste ready examples with expected output.
""",
}

# =============================================================================
# FUNCTION EXAMPLES (Level 3) - ~200 tokens each
# =============================================================================
FUNCTION_EXAMPLES = {
    "ask": """
## Examples: ask

### Basic Question
```bash
uv run cli.py ask "What is the current weather in New York?"
```

### With System Prompt
```bash
uv run cli.py ask "Explain quantum computing" --system "You are a teacher explaining to a 10-year-old"
```

### With Context
```bash
uv run cli.py ask "What are the alternatives?" --context "I'm evaluating PostgreSQL for a new project"
```

### JSON Output for Piping
```bash
uv run cli.py ask "Latest Python version" --format json | jq '.response'
```
""",
    "research": """
## Examples: research

### Basic Research
```bash
uv run cli.py research "Compare REST API vs GraphQL for mobile applications"
```

### With Strip Thinking (Saves Tokens)
```bash
uv run cli.py research "History of machine learning" --strip-thinking
```

### Focused Research with System Prompt
```bash
uv run cli.py research "Best practices for API security" \\
    --system "Focus on practical implementation for startups"
```

### Save Research to File
```bash
uv run cli.py research "State of AI in healthcare 2025" --format text > research.md
```
""",
    "reason": """
## Examples: reason

### Problem Solving
```bash
uv run cli.py reason "Should I use microservices or monolith for a startup MVP?"
```

### Code Analysis
```bash
uv run cli.py reason "Why might this function be slow?" \\
    --context "def fib(n): return fib(n-1) + fib(n-2) if n > 1 else n"
```

### Decision Making
```bash
uv run cli.py reason "PostgreSQL vs MongoDB for an e-commerce platform" \\
    --system "Consider scalability, development speed, and team expertise"
```

### With Strip Thinking
```bash
uv run cli.py reason "Debug this error: CORS policy blocked" --strip-thinking
```
""",
    "search": """
## Examples: search

### Basic Search
```bash
uv run cli.py search "Python 3.12 new features"
```

### Limited Results
```bash
uv run cli.py search "Claude AI announcements" --max-results 5
```

### Regional Search
```bash
uv run cli.py search "local news" --country US
```

### More Content Per Result
```bash
uv run cli.py search "FastAPI tutorial" --max-tokens-per-page 2048
```

### Pipe to jq for Processing
```bash
uv run cli.py search "MCP servers" --format json | jq '.results'
```
""",
    "list": """
## Examples: list

### Show All Functions
```bash
uv run cli.py list
```
""",
    "info": """
## Examples: info

### Get Function Details
```bash
uv run cli.py info ask
uv run cli.py info research
uv run cli.py info search
```
""",
    "example": """
## Examples: example

### Show Function Examples
```bash
uv run cli.py example ask
uv run cli.py example search
```
""",
}


# =============================================================================
# API CLIENT
# =============================================================================
class PerplexityClient:
    """HTTP client for Perplexity API."""

    def __init__(self):
        self.api_key = os.getenv("PERPLEXITY_API_KEY")
        self.base_url = os.getenv("PERPLEXITY_BASE_URL", "https://api.perplexity.ai")
        self.timeout = int(os.getenv("PERPLEXITY_TIMEOUT_MS", "300000")) / 1000  # Convert to seconds
        self.proxy = os.getenv("PERPLEXITY_PROXY") or os.getenv("HTTPS_PROXY") or os.getenv("HTTP_PROXY")

    def _check_api_key(self) -> None:
        """Validate API key is set."""
        if not self.api_key:
            console.print("[red]Error: PERPLEXITY_API_KEY environment variable is required[/red]")
            console.print("\nSet it with:")
            console.print("  export PERPLEXITY_API_KEY='your_key_here'")
            console.print("\nGet your API key at: https://www.perplexity.ai/account/api/group")
            sys.exit(1)

    def _get_client(self) -> httpx.Client:
        """Create HTTP client with optional proxy."""
        kwargs = {"timeout": self.timeout}
        if self.proxy:
            kwargs["proxies"] = {"https://": self.proxy, "http://": self.proxy}
        return httpx.Client(**kwargs)

    def _strip_thinking(self, content: str) -> str:
        """Remove <think>...</think> tags from response."""
        import re
        return re.sub(r'<think>[\s\S]*?</think>', '', content).strip()

    def chat_completion(
        self,
        messages: list[dict],
        model: str = "sonar-pro",
        strip_thinking: bool = False,
    ) -> dict[str, Any]:
        """Perform chat completion with Perplexity API."""
        self._check_api_key()

        url = f"{self.base_url}/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        body = {"model": model, "messages": messages}

        try:
            with self._get_client() as client:
                response = client.post(url, headers=headers, json=body)
                response.raise_for_status()
                data = response.json()

                content = data["choices"][0]["message"]["content"]
                if strip_thinking:
                    content = self._strip_thinking(content)

                # Append citations if present
                if "citations" in data and data["citations"]:
                    content += "\n\nCitations:\n"
                    for i, citation in enumerate(data["citations"], 1):
                        content += f"[{i}] {citation}\n"

                return {"success": True, "response": content}
        except httpx.TimeoutException:
            return {
                "success": False,
                "error": f"Request timeout after {self.timeout}s. Consider increasing PERPLEXITY_TIMEOUT_MS.",
            }
        except httpx.HTTPStatusError as e:
            return {"success": False, "error": f"API error: {e.response.status_code} - {e.response.text}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def search(
        self,
        query: str,
        max_results: int = 10,
        max_tokens_per_page: int = 1024,
        country: Optional[str] = None,
    ) -> dict[str, Any]:
        """Perform web search with Perplexity Search API."""
        self._check_api_key()

        url = f"{self.base_url}/search"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        body = {
            "query": query,
            "max_results": max_results,
            "max_tokens_per_page": max_tokens_per_page,
        }
        if country:
            body["country"] = country

        try:
            with self._get_client() as client:
                response = client.post(url, headers=headers, json=body)
                response.raise_for_status()
                data = response.json()

                results = data.get("results", [])
                formatted = f"Found {len(results)} search results:\n\n"
                for i, result in enumerate(results, 1):
                    formatted += f"{i}. **{result.get('title', 'No title')}**\n"
                    formatted += f"   URL: {result.get('url', 'N/A')}\n"
                    if result.get("snippet"):
                        formatted += f"   {result['snippet']}\n"
                    if result.get("date"):
                        formatted += f"   Date: {result['date']}\n"
                    formatted += "\n"

                return {"success": True, "results": formatted, "raw": results}
        except httpx.TimeoutException:
            return {
                "success": False,
                "error": f"Request timeout after {self.timeout}s. Consider increasing PERPLEXITY_TIMEOUT_MS.",
            }
        except httpx.HTTPStatusError as e:
            return {"success": False, "error": f"API error: {e.response.status_code} - {e.response.text}"}
        except Exception as e:
            return {"success": False, "error": str(e)}


# =============================================================================
# OUTPUT FORMATTING
# =============================================================================
def output_result(result: dict[str, Any], format_type: str = "text") -> None:
    """Format and output result based on format type."""
    if format_type == "json":
        print(json.dumps(result, indent=2))
    elif format_type == "text":
        if result.get("success"):
            if "response" in result:
                console.print(Markdown(result["response"]))
            elif "results" in result:
                console.print(Markdown(result["results"]))
        else:
            console.print(f"[red]Error: {result.get('error', 'Unknown error')}[/red]")
    else:
        # Table format (mainly for search results)
        if result.get("success") and "raw" in result:
            table = Table(title="Search Results")
            table.add_column("#", style="cyan", width=3)
            table.add_column("Title", style="green")
            table.add_column("URL", style="blue")
            for i, r in enumerate(result["raw"], 1):
                table.add_row(str(i), r.get("title", "N/A")[:50], r.get("url", "N/A")[:60])
            console.print(table)
        else:
            output_result(result, "text")


# =============================================================================
# CLI COMMANDS
# =============================================================================
@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Perplexity AI CLI - Web search, reasoning & research via Sonar models."""
    if ctx.invoked_subcommand is None:
        console.print(Panel(QUICK_HELP.strip(), title="Perplexity AI CLI", border_style="blue"))


@cli.command("list")
def list_functions():
    """List all available functions."""
    table = Table(title="Available Functions")
    table.add_column("Function", style="cyan", width=12)
    table.add_column("Description", style="white")
    table.add_column("Model", style="green", width=22)

    functions = [
        ("ask", "General-purpose AI with web search", "sonar-pro"),
        ("research", "Deep comprehensive research", "sonar-deep-research"),
        ("reason", "Advanced reasoning & analysis", "sonar-reasoning-pro"),
        ("search", "Direct web search results", "Search API"),
        ("list", "Show all functions", "-"),
        ("info", "Detailed function docs", "-"),
        ("example", "Working examples", "-"),
    ]

    for name, desc, model in functions:
        table.add_row(name, desc, model)

    console.print(table)
    console.print("\nNext: [cyan]uv run cli.py info FUNCTION[/cyan] for detailed docs")


@cli.command("info")
@click.argument("function_name")
def info(function_name: str):
    """Get detailed documentation for a function."""
    if function_name not in FUNCTION_INFO:
        console.print(f"[red]Unknown function: {function_name}[/red]")
        console.print(f"Available: {', '.join(FUNCTION_INFO.keys())}")
        sys.exit(1)

    console.print(Markdown(FUNCTION_INFO[function_name]))
    console.print(f"\nNext: [cyan]uv run cli.py example {function_name}[/cyan] for working examples")


@cli.command("example")
@click.argument("function_name")
def example(function_name: str):
    """Show working examples for a function."""
    if function_name not in FUNCTION_EXAMPLES:
        console.print(f"[red]Unknown function: {function_name}[/red]")
        console.print(f"Available: {', '.join(FUNCTION_EXAMPLES.keys())}")
        sys.exit(1)

    console.print(Markdown(FUNCTION_EXAMPLES[function_name]))


@cli.command("ask")
@click.argument("query")
@click.option("--system", "-s", help="System prompt to guide behavior")
@click.option("--context", "-c", help="Additional context for the query")
@click.option("--format", "-f", "format_type", type=click.Choice(["text", "json", "table"]), default="text", help="Output format")
def ask(query: str, system: Optional[str], context: Optional[str], format_type: str):
    """General-purpose AI with real-time web search (sonar-pro)."""
    client = PerplexityClient()

    messages = []
    if system:
        messages.append({"role": "system", "content": system})

    user_content = query
    if context:
        user_content = f"{context}\n\n{query}"
    messages.append({"role": "user", "content": user_content})

    result = client.chat_completion(messages, model="sonar-pro")
    output_result(result, format_type)


@cli.command("research")
@click.argument("query")
@click.option("--system", "-s", help="System prompt to guide research focus")
@click.option("--context", "-c", help="Additional context or constraints")
@click.option("--strip-thinking", is_flag=True, help="Remove <think> tags to save tokens")
@click.option("--format", "-f", "format_type", type=click.Choice(["text", "json", "table"]), default="text", help="Output format")
def research(query: str, system: Optional[str], context: Optional[str], strip_thinking: bool, format_type: str):
    """Deep comprehensive research (sonar-deep-research)."""
    client = PerplexityClient()

    messages = []
    if system:
        messages.append({"role": "system", "content": system})

    user_content = query
    if context:
        user_content = f"{context}\n\n{query}"
    messages.append({"role": "user", "content": user_content})

    result = client.chat_completion(messages, model="sonar-deep-research", strip_thinking=strip_thinking)
    output_result(result, format_type)


@cli.command("reason")
@click.argument("query")
@click.option("--system", "-s", help="System prompt to guide reasoning approach")
@click.option("--context", "-c", help="Additional context or constraints")
@click.option("--strip-thinking", is_flag=True, help="Remove <think> tags to save tokens")
@click.option("--format", "-f", "format_type", type=click.Choice(["text", "json", "table"]), default="text", help="Output format")
def reason(query: str, system: Optional[str], context: Optional[str], strip_thinking: bool, format_type: str):
    """Advanced reasoning and analysis (sonar-reasoning-pro)."""
    client = PerplexityClient()

    messages = []
    if system:
        messages.append({"role": "system", "content": system})

    user_content = query
    if context:
        user_content = f"{context}\n\n{query}"
    messages.append({"role": "user", "content": user_content})

    result = client.chat_completion(messages, model="sonar-reasoning-pro", strip_thinking=strip_thinking)
    output_result(result, format_type)


@cli.command("search")
@click.argument("query")
@click.option("--max-results", "-n", type=click.IntRange(1, 20), default=10, help="Number of results (1-20)")
@click.option("--max-tokens-per-page", "-t", type=click.IntRange(256, 2048), default=1024, help="Tokens per page (256-2048)")
@click.option("--country", help="ISO country code for regional results (e.g., US, GB)")
@click.option("--format", "-f", "format_type", type=click.Choice(["text", "json", "table"]), default="text", help="Output format")
def search(query: str, max_results: int, max_tokens_per_page: int, country: Optional[str], format_type: str):
    """Direct web search with ranked results."""
    client = PerplexityClient()

    result = client.search(query, max_results, max_tokens_per_page, country)
    output_result(result, format_type)


if __name__ == "__main__":
    cli()
