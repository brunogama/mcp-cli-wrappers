#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "httpx>=0.27.0",
#     "click>=8.1.0",
#     "rich>=13.0.0",
#     "pydantic>=2.0.0",
#     "python-dotenv>=1.0.0",
# ]
# ///
"""
Brave Search CLI - Progressive disclosure CLI wrapper for Brave Search MCP Server.

A token-efficient CLI that wraps Brave Search API tools with 4-level help system.

Environment Variables:
    BRAVE_API_KEY: Brave Search API key (required)

Usage:
    uv run cli.py --help              # Level 1: Quick overview
    uv run cli.py list                # Level 2: All functions
    uv run cli.py info web_search     # Level 2: Detailed docs
    uv run cli.py example web_search  # Level 3: Working examples
    uv run cli.py web_search --help   # Level 4: Full reference
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any, Literal

import click
import httpx
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Load environment variables from script directory (.env first, then .env.local overrides)
_script_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(_script_dir, ".env"))
load_dotenv(os.path.join(_script_dir, ".env.local"), override=True)

console = Console()

# ============================================================================
# Configuration
# ============================================================================

BRAVE_API_KEY = os.getenv("BRAVE_API_KEY", "")
BRAVE_API_BASE = "https://api.search.brave.com/res/v1"

# Country codes for API
COUNTRY_CODES = [
    "ALL", "AR", "AU", "AT", "BE", "BR", "CA", "CL", "DK", "FI", "FR", "DE",
    "HK", "IN", "ID", "IT", "JP", "KR", "MY", "MX", "NL", "NZ", "NO", "CN",
    "PL", "PT", "PH", "RU", "SA", "ZA", "ES", "SE", "CH", "TW", "TR", "GB", "US"
]

# Safe search options
SAFESEARCH_OPTIONS = ["off", "moderate", "strict"]

# Freshness options
FRESHNESS_OPTIONS = ["pd", "pw", "pm", "py"]  # day, week, month, year

# Result filter options
RESULT_FILTER_OPTIONS = [
    "discussions", "faq", "infobox", "news", "query",
    "summarizer", "videos", "web", "locations", "rich"
]

# ============================================================================
# Help Text (4-Level Progressive Disclosure)
# ============================================================================

QUICK_HELP = """
Brave Search CLI - Search the web with Brave's privacy-focused API

FUNCTIONS:
  web_search      Comprehensive web search with rich results
  local_search    Find local businesses and places (Pro plan)
  video_search    Search for videos with metadata
  image_search    Find images with filtering options
  news_search     Search current news articles
  summarizer      Generate AI summaries from search results

USAGE:
  uv run cli.py web_search "python tutorials"
  uv run cli.py image_search "sunset beach" --count 5
  uv run cli.py news_search "AI developments" --freshness pw

SETUP:
  export BRAVE_API_KEY="your_api_key_here"

MORE INFO:
  uv run cli.py list                 # See all functions
  uv run cli.py info FUNCTION        # Detailed docs
  uv run cli.py example FUNCTION     # Working examples
"""

FUNCTION_INFO = {
    "web_search": {
        "name": "web_search",
        "description": "Performs comprehensive web searches with rich result types and advanced filtering options.",
        "parameters": {
            "query": {"type": "str", "required": True, "description": "Search query (max 400 chars, 50 words)"},
            "country": {"type": "str", "default": "US", "description": "Country code for results origin"},
            "count": {"type": "int", "default": 10, "description": "Number of results (1-20)"},
            "offset": {"type": "int", "default": 0, "description": "Pagination offset (0-9)"},
            "safesearch": {"type": "str", "default": "moderate", "description": "Content filter: off, moderate, strict"},
            "freshness": {"type": "str", "default": None, "description": "Time filter: pd (day), pw (week), pm (month), py (year)"},
            "result_filter": {"type": "list", "default": ["web", "query"], "description": "Result types to include"},
            "extra_snippets": {"type": "bool", "default": False, "description": "Include additional excerpts"},
            "summary": {"type": "bool", "default": False, "description": "Enable AI summary generation"},
        },
        "returns": "JSON with web results, FAQs, discussions, news, and videos",
        "related": ["news_search", "summarizer"],
    },
    "local_search": {
        "name": "local_search",
        "description": "Searches for local businesses and places with ratings, hours, and contact info. Requires Pro plan.",
        "parameters": {
            "query": {"type": "str", "required": True, "description": "Search query (e.g., 'coffee shops near me')"},
            "country": {"type": "str", "default": "US", "description": "Country code for location context"},
            "count": {"type": "int", "default": 10, "description": "Number of results (1-20)"},
        },
        "returns": "JSON with business names, addresses, ratings, phone numbers, and hours",
        "related": ["web_search"],
    },
    "video_search": {
        "name": "video_search",
        "description": "Searches for videos with metadata including duration, thumbnails, and view counts.",
        "parameters": {
            "query": {"type": "str", "required": True, "description": "Video search query"},
            "country": {"type": "str", "default": "US", "description": "Country code for results"},
            "count": {"type": "int", "default": 10, "description": "Number of results (1-20)"},
            "safesearch": {"type": "str", "default": "moderate", "description": "Content filter"},
            "freshness": {"type": "str", "default": None, "description": "Time filter"},
        },
        "returns": "JSON with video URLs, titles, descriptions, durations, and thumbnails",
        "related": ["web_search", "image_search"],
    },
    "image_search": {
        "name": "image_search",
        "description": "Searches for images with filtering options for art, photos, and graphics.",
        "parameters": {
            "query": {"type": "str", "required": True, "description": "Image search query"},
            "country": {"type": "str", "default": "US", "description": "Country code for results"},
            "count": {"type": "int", "default": 10, "description": "Number of results (1-20)"},
            "safesearch": {"type": "str", "default": "moderate", "description": "Content filter"},
        },
        "returns": "JSON with image URLs, dimensions, and source information",
        "related": ["video_search", "web_search"],
    },
    "news_search": {
        "name": "news_search",
        "description": "Searches for current news articles with freshness controls and breaking news indicators.",
        "parameters": {
            "query": {"type": "str", "required": True, "description": "News search query"},
            "country": {"type": "str", "default": "US", "description": "Country code for results"},
            "count": {"type": "int", "default": 10, "description": "Number of results (1-20)"},
            "freshness": {"type": "str", "default": None, "description": "Time filter: pd (day), pw (week), pm (month)"},
            "safesearch": {"type": "str", "default": "moderate", "description": "Content filter"},
        },
        "returns": "JSON with article titles, URLs, sources, publish dates, and thumbnails",
        "related": ["web_search", "summarizer"],
    },
    "summarizer": {
        "name": "summarizer",
        "description": "Generates AI summaries from web search results. Requires Pro AI subscription and prior web_search with summary=true.",
        "parameters": {
            "key": {"type": "str", "required": True, "description": "Summary key from web_search results (when summary=true)"},
        },
        "returns": "JSON with AI-generated summary text and source references",
        "related": ["web_search"],
    },
}

FUNCTION_EXAMPLES = {
    "web_search": [
        {
            "description": "Basic web search",
            "command": 'uv run cli.py web_search "python async programming"',
            "output": '{"results": [{"title": "Async IO in Python", "url": "...", "description": "..."}]}',
        },
        {
            "description": "Search with country filter",
            "command": 'uv run cli.py web_search "local news" --country GB --count 5',
            "output": '{"results": [...], "count": 5}',
        },
        {
            "description": "Search with freshness filter",
            "command": 'uv run cli.py web_search "AI news" --freshness pw --summary',
            "output": '{"results": [...], "summary_key": "..."}',
        },
    ],
    "local_search": [
        {
            "description": "Find local restaurants",
            "command": 'uv run cli.py local_search "italian restaurants near me"',
            "output": '{"locations": [{"name": "...", "address": "...", "rating": 4.5}]}',
        },
        {
            "description": "Search in specific country",
            "command": 'uv run cli.py local_search "coffee shops" --country AU',
            "output": '{"locations": [...]}',
        },
    ],
    "video_search": [
        {
            "description": "Search for tutorial videos",
            "command": 'uv run cli.py video_search "python machine learning tutorial"',
            "output": '{"videos": [{"title": "...", "url": "...", "duration": "15:30"}]}',
        },
        {
            "description": "Recent video search",
            "command": 'uv run cli.py video_search "tech news" --freshness pd',
            "output": '{"videos": [...]}',
        },
    ],
    "image_search": [
        {
            "description": "Search for images",
            "command": 'uv run cli.py image_search "mountain landscape"',
            "output": '{"images": [{"url": "...", "width": 1920, "height": 1080}]}',
        },
        {
            "description": "Safe image search",
            "command": 'uv run cli.py image_search "nature photography" --safesearch strict',
            "output": '{"images": [...], "might_be_offensive": false}',
        },
    ],
    "news_search": [
        {
            "description": "Search recent news",
            "command": 'uv run cli.py news_search "AI developments" --freshness pd',
            "output": '{"articles": [{"title": "...", "source": "...", "age": "2 hours"}]}',
        },
        {
            "description": "Technology news",
            "command": 'uv run cli.py news_search "technology startup" --count 10',
            "output": '{"articles": [...]}',
        },
    ],
    "summarizer": [
        {
            "description": "Get AI summary (requires prior web_search with summary=true)",
            "command": 'uv run cli.py summarizer "summary_key_from_web_search"',
            "output": '{"summary": "AI-generated summary text...", "references": [...]}',
        },
    ],
}

# ============================================================================
# API Client
# ============================================================================


def check_api_key() -> bool:
    """Check if API key is configured."""
    if not BRAVE_API_KEY:
        console.print(
            "[red]Error:[/red] BRAVE_API_KEY environment variable not set.\n"
            "Get your API key at: https://brave.com/search/api/\n"
            "Then run: export BRAVE_API_KEY='your_key_here'"
        )
        return False
    return True


def make_request(
    endpoint: str,
    params: dict[str, Any],
    timeout: float = 30.0,
) -> dict[str, Any]:
    """Make authenticated request to Brave Search API."""
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": BRAVE_API_KEY,
    }

    # Filter out None values
    params = {k: v for k, v in params.items() if v is not None}

    url = f"{BRAVE_API_BASE}/{endpoint}"

    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        return {"error": f"HTTP {e.response.status_code}: {e.response.text}"}
    except httpx.RequestError as e:
        return {"error": f"Request failed: {str(e)}"}


# ============================================================================
# Search Functions
# ============================================================================


def web_search(
    query: str,
    country: str = "US",
    count: int = 10,
    offset: int = 0,
    safesearch: str = "moderate",
    freshness: str | None = None,
    result_filter: list[str] | None = None,
    extra_snippets: bool = False,
    summary: bool = False,
) -> dict[str, Any]:
    """Perform comprehensive web search."""
    params = {
        "q": query,
        "country": country,
        "count": min(max(count, 1), 20),
        "offset": min(max(offset, 0), 9),
        "safesearch": safesearch,
        "freshness": freshness,
        "extra_snippets": extra_snippets,
        "summary": summary,
    }

    if result_filter:
        params["result_filter"] = ",".join(result_filter)

    return make_request("web/search", params)


def local_search(
    query: str,
    country: str = "US",
    count: int = 10,
) -> dict[str, Any]:
    """Search for local businesses and places."""
    params = {
        "q": query,
        "country": country,
        "count": min(max(count, 1), 20),
        "result_filter": "locations",
    }

    return make_request("web/search", params)


def video_search(
    query: str,
    country: str = "US",
    count: int = 10,
    safesearch: str = "moderate",
    freshness: str | None = None,
) -> dict[str, Any]:
    """Search for videos."""
    params = {
        "q": query,
        "country": country,
        "count": min(max(count, 1), 20),
        "safesearch": safesearch,
        "freshness": freshness,
    }

    return make_request("videos/search", params)


def image_search(
    query: str,
    country: str = "US",
    count: int = 10,
    safesearch: str = "moderate",
) -> dict[str, Any]:
    """Search for images."""
    params = {
        "q": query,
        "country": country,
        "count": min(max(count, 1), 20),
        "safesearch": safesearch,
    }

    return make_request("images/search", params)


def news_search(
    query: str,
    country: str = "US",
    count: int = 10,
    freshness: str | None = None,
    safesearch: str = "moderate",
) -> dict[str, Any]:
    """Search for news articles."""
    params = {
        "q": query,
        "country": country,
        "count": min(max(count, 1), 20),
        "freshness": freshness,
        "safesearch": safesearch,
    }

    return make_request("news/search", params)


def get_summary(key: str) -> dict[str, Any]:
    """Get AI summary for a search result."""
    params = {"key": key}
    return make_request("summarizer/search", params)


# ============================================================================
# Output Formatting
# ============================================================================


def format_output(data: dict[str, Any], output_format: str = "json") -> None:
    """Format and display output."""
    if output_format == "json":
        console.print_json(json.dumps(data, indent=2))
    elif output_format == "text":
        if "error" in data:
            console.print(f"[red]Error:[/red] {data['error']}")
        elif "web" in data and "results" in data["web"]:
            for i, result in enumerate(data["web"]["results"], 1):
                console.print(f"\n[bold]{i}. {result.get('title', 'No title')}[/bold]")
                console.print(f"   [dim]{result.get('url', '')}[/dim]")
                console.print(f"   {result.get('description', '')}")
        elif "results" in data:
            for i, result in enumerate(data["results"], 1):
                console.print(f"\n[bold]{i}. {result.get('title', 'No title')}[/bold]")
                console.print(f"   [dim]{result.get('url', '')}[/dim]")
                if "description" in result:
                    console.print(f"   {result['description']}")
        else:
            console.print(data)
    elif output_format == "table":
        table = Table(show_header=True, header_style="bold magenta")

        if "web" in data and "results" in data["web"]:
            results = data["web"]["results"]
        elif "results" in data:
            results = data["results"]
        else:
            console.print_json(json.dumps(data, indent=2))
            return

        if results:
            table.add_column("#", style="dim", width=3)
            table.add_column("Title", style="cyan", max_width=50)
            table.add_column("URL", style="dim", max_width=40)

            for i, result in enumerate(results[:10], 1):
                table.add_row(
                    str(i),
                    result.get("title", "")[:50],
                    result.get("url", "")[:40],
                )

            console.print(table)
        else:
            console.print("[yellow]No results found.[/yellow]")


# ============================================================================
# CLI Commands
# ============================================================================


@click.group(invoke_without_command=True)
@click.option("--help", "-h", is_flag=True, help="Show help message")
@click.pass_context
def cli(ctx: click.Context, help: bool) -> None:
    """Brave Search CLI - Privacy-focused web search from the command line."""
    if help or ctx.invoked_subcommand is None:
        console.print(Panel(QUICK_HELP.strip(), title="Brave Search CLI", border_style="blue"))


@cli.command()
def list() -> None:
    """List all available functions."""
    table = Table(title="Available Functions", show_header=True, header_style="bold cyan")
    table.add_column("Function", style="green")
    table.add_column("Description", style="white")

    for name, info in FUNCTION_INFO.items():
        table.add_row(name, info["description"][:60] + "..." if len(info["description"]) > 60 else info["description"])

    console.print(table)
    console.print("\n[dim]Use 'uv run cli.py info FUNCTION' for detailed documentation[/dim]")


@cli.command()
@click.argument("function_name")
def info(function_name: str) -> None:
    """Show detailed information about a function."""
    if function_name not in FUNCTION_INFO:
        console.print(f"[red]Unknown function: {function_name}[/red]")
        console.print(f"Available: {', '.join(FUNCTION_INFO.keys())}")
        return

    func = FUNCTION_INFO[function_name]

    console.print(Panel(f"[bold cyan]{func['name']}[/bold cyan]", border_style="blue"))
    console.print(f"\n[bold]Description:[/bold]\n{func['description']}\n")

    console.print("[bold]Parameters:[/bold]")
    for param, details in func["parameters"].items():
        required = "[red]*[/red]" if details.get("required") else ""
        default = f" [dim](default: {details.get('default')})[/dim]" if "default" in details else ""
        console.print(f"  {required}{param}: {details['type']}{default}")
        console.print(f"    [dim]{details['description']}[/dim]")

    console.print(f"\n[bold]Returns:[/bold]\n  {func['returns']}")

    if func.get("related"):
        console.print(f"\n[bold]Related:[/bold] {', '.join(func['related'])}")

    console.print(f"\n[dim]Use 'uv run cli.py example {function_name}' for examples[/dim]")


@cli.command()
@click.argument("function_name")
def example(function_name: str) -> None:
    """Show usage examples for a function."""
    if function_name not in FUNCTION_EXAMPLES:
        console.print(f"[red]No examples for: {function_name}[/red]")
        console.print(f"Available: {', '.join(FUNCTION_EXAMPLES.keys())}")
        return

    console.print(Panel(f"[bold cyan]Examples: {function_name}[/bold cyan]", border_style="blue"))

    for i, ex in enumerate(FUNCTION_EXAMPLES[function_name], 1):
        console.print(f"\n[bold]Example {i}:[/bold] {ex['description']}")
        console.print(f"[green]$ {ex['command']}[/green]")
        console.print(f"[dim]{ex['output']}[/dim]")


# Search commands
@cli.command()
@click.argument("query")
@click.option("--country", "-c", default="US", help="Country code (e.g., US, GB, DE)")
@click.option("--count", "-n", default=10, type=int, help="Number of results (1-20)")
@click.option("--offset", "-o", default=0, type=int, help="Pagination offset (0-9)")
@click.option("--safesearch", "-s", default="moderate", type=click.Choice(SAFESEARCH_OPTIONS), help="Content filter")
@click.option("--freshness", "-f", type=click.Choice(FRESHNESS_OPTIONS), help="Time filter: pd=day, pw=week, pm=month, py=year")
@click.option("--extra-snippets", is_flag=True, help="Include additional excerpts")
@click.option("--summary", is_flag=True, help="Enable AI summary generation")
@click.option("--format", "output_format", default="json", type=click.Choice(["json", "text", "table"]), help="Output format")
def web_search_cmd(
    query: str,
    country: str,
    count: int,
    offset: int,
    safesearch: str,
    freshness: str | None,
    extra_snippets: bool,
    summary: bool,
    output_format: str,
) -> None:
    """Perform comprehensive web search.

    QUERY: Search terms (max 400 chars, 50 words)

    Examples:
        uv run cli.py web_search "python tutorials"
        uv run cli.py web_search "AI news" --freshness pw --format text
    """
    if not check_api_key():
        sys.exit(1)

    result = web_search(
        query=query,
        country=country,
        count=count,
        offset=offset,
        safesearch=safesearch,
        freshness=freshness,
        extra_snippets=extra_snippets,
        summary=summary,
    )
    format_output(result, output_format)


# Alias for web_search
cli.add_command(web_search_cmd, name="web_search")
cli.add_command(web_search_cmd, name="search")


@cli.command()
@click.argument("query")
@click.option("--country", "-c", default="US", help="Country code")
@click.option("--count", "-n", default=10, type=int, help="Number of results (1-20)")
@click.option("--format", "output_format", default="json", type=click.Choice(["json", "text", "table"]), help="Output format")
def local_search_cmd(
    query: str,
    country: str,
    count: int,
    output_format: str,
) -> None:
    """Search for local businesses and places.

    Requires Brave Search Pro plan for full functionality.

    QUERY: Location-based search (e.g., 'coffee shops near me')

    Examples:
        uv run cli.py local_search "restaurants near me"
        uv run cli.py local_search "hotels in paris" --country FR
    """
    if not check_api_key():
        sys.exit(1)

    result = local_search(query=query, country=country, count=count)
    format_output(result, output_format)


cli.add_command(local_search_cmd, name="local_search")
cli.add_command(local_search_cmd, name="local")


@cli.command()
@click.argument("query")
@click.option("--country", "-c", default="US", help="Country code")
@click.option("--count", "-n", default=10, type=int, help="Number of results (1-20)")
@click.option("--safesearch", "-s", default="moderate", type=click.Choice(SAFESEARCH_OPTIONS), help="Content filter")
@click.option("--freshness", "-f", type=click.Choice(FRESHNESS_OPTIONS), help="Time filter")
@click.option("--format", "output_format", default="json", type=click.Choice(["json", "text", "table"]), help="Output format")
def video_search_cmd(
    query: str,
    country: str,
    count: int,
    safesearch: str,
    freshness: str | None,
    output_format: str,
) -> None:
    """Search for videos with metadata.

    QUERY: Video search terms

    Examples:
        uv run cli.py video_search "python machine learning"
        uv run cli.py video_search "tech reviews" --freshness pd
    """
    if not check_api_key():
        sys.exit(1)

    result = video_search(
        query=query,
        country=country,
        count=count,
        safesearch=safesearch,
        freshness=freshness,
    )
    format_output(result, output_format)


cli.add_command(video_search_cmd, name="video_search")
cli.add_command(video_search_cmd, name="videos")


@cli.command()
@click.argument("query")
@click.option("--country", "-c", default="US", help="Country code")
@click.option("--count", "-n", default=10, type=int, help="Number of results (1-20)")
@click.option("--safesearch", "-s", default="moderate", type=click.Choice(SAFESEARCH_OPTIONS), help="Content filter")
@click.option("--format", "output_format", default="json", type=click.Choice(["json", "text", "table"]), help="Output format")
def image_search_cmd(
    query: str,
    country: str,
    count: int,
    safesearch: str,
    output_format: str,
) -> None:
    """Search for images.

    QUERY: Image search terms

    Examples:
        uv run cli.py image_search "mountain landscape"
        uv run cli.py image_search "abstract art" --safesearch strict
    """
    if not check_api_key():
        sys.exit(1)

    result = image_search(
        query=query,
        country=country,
        count=count,
        safesearch=safesearch,
    )
    format_output(result, output_format)


cli.add_command(image_search_cmd, name="image_search")
cli.add_command(image_search_cmd, name="images")


@cli.command()
@click.argument("query")
@click.option("--country", "-c", default="US", help="Country code")
@click.option("--count", "-n", default=10, type=int, help="Number of results (1-20)")
@click.option("--freshness", "-f", type=click.Choice(FRESHNESS_OPTIONS), help="Time filter")
@click.option("--safesearch", "-s", default="moderate", type=click.Choice(SAFESEARCH_OPTIONS), help="Content filter")
@click.option("--format", "output_format", default="json", type=click.Choice(["json", "text", "table"]), help="Output format")
def news_search_cmd(
    query: str,
    country: str,
    count: int,
    freshness: str | None,
    safesearch: str,
    output_format: str,
) -> None:
    """Search for news articles.

    QUERY: News search terms

    Examples:
        uv run cli.py news_search "AI developments"
        uv run cli.py news_search "technology" --freshness pd --format text
    """
    if not check_api_key():
        sys.exit(1)

    result = news_search(
        query=query,
        country=country,
        count=count,
        freshness=freshness,
        safesearch=safesearch,
    )
    format_output(result, output_format)


cli.add_command(news_search_cmd, name="news_search")
cli.add_command(news_search_cmd, name="news")


@cli.command()
@click.argument("key")
@click.option("--format", "output_format", default="json", type=click.Choice(["json", "text"]), help="Output format")
def summarizer_cmd(key: str, output_format: str) -> None:
    """Get AI summary from search results.

    Requires Pro AI subscription. First run web_search with --summary flag
    to get the summary key.

    KEY: Summary key from web_search results

    Example workflow:
        1. uv run cli.py web_search "topic" --summary
        2. Copy the summary_key from results
        3. uv run cli.py summarizer "summary_key_here"
    """
    if not check_api_key():
        sys.exit(1)

    result = get_summary(key)
    format_output(result, output_format)


cli.add_command(summarizer_cmd, name="summarizer")
cli.add_command(summarizer_cmd, name="summary")


if __name__ == "__main__":
    cli()
