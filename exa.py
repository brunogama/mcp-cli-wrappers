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
Exa AI Search CLI Wrapper

A comprehensive CLI for the Exa AI search engine - the first meaning-based web
search API powered by embeddings, designed for AI applications.

Run with: uv run exa.py [COMMAND] [ARGS]

4-Level Progressive Disclosure:
  Level 1: --help              Quick overview (~30 tokens)
  Level 2: list                All functions
           info FUNCTION       Detailed docs (~150 tokens)
  Level 3: example FUNCTION    Working examples (~200 tokens)
  Level 4: FUNCTION --help     Complete reference (~500 tokens)
"""

import argparse
import json
import os
import sys
import traceback
from datetime import datetime
from typing import Any, Dict, List, Optional

try:
    import httpx
    from dotenv import load_dotenv
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.syntax import Syntax
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Run: uv run exa.py --help")
    sys.exit(1)

# Load environment variables from script directory (.env first, then .env.local overrides)
_script_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(_script_dir, ".env"))
load_dotenv(os.path.join(_script_dir, ".env.local"), override=True)

console = Console()

# ===== CONFIGURATION =====

EXA_API_KEY = os.environ.get("EXA_API_KEY", "")
EXA_API_URL = os.environ.get("EXA_API_URL", "https://api.exa.ai")
DEFAULT_TIMEOUT = int(os.environ.get("EXA_TIMEOUT", "60"))

# ===== LEVEL 1: QUICK HELP =====

QUICK_HELP = """Exa AI Search CLI

AI-powered neural search engine for semantic web discovery.

Available functions:
  search              Neural search with embeddings (best for semantic queries)
  deep-search         Comprehensive search with query expansion
  research            Agentic research with multi-step reasoning (NEW!)
  code-search         Search for code examples and documentation
  company-research    Research companies with business intelligence
  find-similar        Find content similar to a given URL

  get-contents        Extract full content from URLs
  config              Show current configuration
  version             Display version information

Quick start:
  uv run exa.py list                        # See all functions
  uv run exa.py info search                 # Detailed docs for search
  uv run exa.py example research            # Working examples for research
  uv run exa.py search "machine learning"   # Execute search
  uv run exa.py research "What are the latest AI breakthroughs?"

Options:
  --format json|text    Output format (default: text)
  --verbose             Enable verbose output

Environment:
  EXA_API_KEY           API key for authentication (required)
  EXA_API_URL           API endpoint (default: https://api.exa.ai)
  EXA_TIMEOUT           Request timeout in seconds (default: 60)

Get started: https://exa.ai/
"""

# ===== LEVEL 2: FUNCTION INFO =====

FUNCTION_INFO: Dict[str, Dict[str, Any]] = {
    "search": {
        "name": "search",
        "description": "Neural search using embeddings for semantic understanding",
        "long_description": """
Perform intelligent neural search using Exa's embeddings-based engine.
Understands meaning and context, not just keyword matching.
Best for semantic queries and natural language searches.

Search types:
- auto (default): Intelligently combines neural and keyword methods
- neural: Pure embeddings-based semantic search
- fast: Streamlined search with lower latency
        """.strip(),
        "parameters": [
            {
                "name": "query",
                "type": "string",
                "required": True,
                "description": "Search query (natural language or semantic)"
            },
            {
                "name": "num_results",
                "type": "integer",
                "required": False,
                "default": 10,
                "description": "Number of results (1-100)"
            },
            {
                "name": "type",
                "type": "string",
                "required": False,
                "default": "auto",
                "description": "Search type: auto, neural, fast"
            },
            {
                "name": "category",
                "type": "string",
                "required": False,
                "description": "Filter by: company, research_paper, news, tweet, personal_site, financial_report, people"
            },
            {
                "name": "include_domains",
                "type": "array",
                "required": False,
                "description": "Only search these domains (max 1200)"
            },
            {
                "name": "exclude_domains",
                "type": "array",
                "required": False,
                "description": "Exclude these domains (max 1200)"
            },
            {
                "name": "start_published_date",
                "type": "string",
                "required": False,
                "description": "ISO 8601 date (e.g., 2024-01-01)"
            },
            {
                "name": "end_published_date",
                "type": "string",
                "required": False,
                "description": "ISO 8601 date (e.g., 2024-12-31)"
            },
            {
                "name": "include_text",
                "type": "boolean",
                "required": False,
                "default": False,
                "description": "Include full page text in results"
            },
            {
                "name": "include_highlights",
                "type": "boolean",
                "required": False,
                "default": True,
                "description": "Include relevant snippets"
            },
            {
                "name": "include_summary",
                "type": "boolean",
                "required": False,
                "default": False,
                "description": "Include LLM-generated summary"
            }
        ],
        "returns": "List of search results with titles, URLs, snippets, and metadata",
        "related": ["deep-search", "code-search", "find-similar"]
    },
    "deep-search": {
        "name": "deep-search",
        "description": "Comprehensive search with automatic query expansion",
        "long_description": """
Perform deep research using Exa's advanced search with query expansion.
Automatically explores multiple query variations for comprehensive results.
Best for thorough research and discovery.

Note: Higher cost than regular search (~3x), but provides more comprehensive coverage.
        """.strip(),
        "parameters": [
            {
                "name": "query",
                "type": "string",
                "required": True,
                "description": "Primary search query"
            },
            {
                "name": "additional_queries",
                "type": "array",
                "required": False,
                "description": "Extra query variations to explore"
            },
            {
                "name": "num_results",
                "type": "integer",
                "required": False,
                "default": 10,
                "description": "Results per query (1-100)"
            },
            {
                "name": "include_text",
                "type": "boolean",
                "required": False,
                "default": False,
                "description": "Include full page text"
            },
            {
                "name": "include_summary",
                "type": "boolean",
                "required": False,
                "default": True,
                "description": "Include AI-generated summaries"
            }
        ],
        "returns": "Comprehensive search results with expanded query coverage",
        "related": ["search", "research", "company-research"]
    },
    "research": {
        "name": "research",
        "description": "Agentic research with multi-step reasoning and citations",
        "long_description": """
Execute complex research tasks using Exa's agentic Research API.
The system plans, searches, extracts, and reasons across sources
to synthesize comprehensive answers with citations.

Models available:
- exa-research (default): Adaptive compute, 45-90s, most tasks
- exa-research-pro: Maximum quality, 90-180s, complex multi-step tasks

Pricing (per successful task):
- Search: $5/1k queries
- Page read: $5-10/1k pages (model dependent)
- Reasoning: $5/1M tokens

Best for:
- Complex research questions requiring synthesis
- Multi-step analysis across sources
- Tasks needing structured output with citations
- Questions that benefit from agentic reasoning
        """.strip(),
        "parameters": [
            {
                "name": "instructions",
                "type": "string",
                "required": True,
                "description": "Natural language research task (max 4096 chars)"
            },
            {
                "name": "model",
                "type": "string",
                "required": False,
                "default": "exa-research",
                "description": "Model: exa-research (faster) or exa-research-pro (higher quality)"
            },
            {
                "name": "output_schema",
                "type": "object",
                "required": False,
                "description": "JSON Schema for structured output (max 8 root fields, 5 levels deep)"
            }
        ],
        "returns": "Structured research report with citations and reasoning",
        "related": ["deep-search", "search"]
    },
    "code-search": {
        "name": "code-search",
        "description": "Search for code examples and technical documentation",
        "long_description": """
Search specifically for code examples, documentation, and programming resources.
Targets GitHub, Stack Overflow, official docs, and technical blogs.
Model specifically trained on high-accuracy code referencing.

Best for:
- Finding implementation examples
- Discovering API documentation
- Locating troubleshooting guides
- Research programming patterns
        """.strip(),
        "parameters": [
            {
                "name": "query",
                "type": "string",
                "required": True,
                "description": "Code-related query (e.g., 'async Python example')"
            },
            {
                "name": "num_results",
                "type": "integer",
                "required": False,
                "default": 10,
                "description": "Number of results (1-100)"
            },
            {
                "name": "include_domains",
                "type": "array",
                "required": False,
                "description": "Focus on specific domains (github.com, stackoverflow.com, etc.)"
            },
            {
                "name": "include_text",
                "type": "boolean",
                "required": False,
                "default": True,
                "description": "Include code snippets and documentation text"
            },
            {
                "name": "include_highlights",
                "type": "boolean",
                "required": False,
                "default": True,
                "description": "Extract relevant code snippets"
            }
        ],
        "returns": "Code examples and documentation with relevant snippets",
        "related": ["search", "get-contents"]
    },
    "company-research": {
        "name": "company-research",
        "description": "Research companies with business intelligence and news",
        "long_description": """
Gather comprehensive information about companies including:
- Business information and profiles
- Recent news and announcements
- Financial insights
- Industry analysis
- Company updates

Automatically filters to company-related content.
        """.strip(),
        "parameters": [
            {
                "name": "company_name",
                "type": "string",
                "required": True,
                "description": "Company name or identifier"
            },
            {
                "name": "num_results",
                "type": "integer",
                "required": False,
                "default": 20,
                "description": "Number of results (1-100)"
            },
            {
                "name": "include_news",
                "type": "boolean",
                "required": False,
                "default": True,
                "description": "Include recent news articles"
            },
            {
                "name": "start_date",
                "type": "string",
                "required": False,
                "description": "Start date for news (ISO 8601)"
            },
            {
                "name": "include_summary",
                "type": "boolean",
                "required": False,
                "default": True,
                "description": "Include AI summaries"
            }
        ],
        "returns": "Company information, news, and business intelligence",
        "related": ["search", "deep-search"]
    },
    "find-similar": {
        "name": "find-similar",
        "description": "Find content similar to a given URL",
        "long_description": """
Discover content semantically similar to a reference URL.
Uses embeddings to understand content meaning and find related pages.

Best for:
- Finding related articles
- Discovering similar research
- Competitive analysis
- Content discovery
        """.strip(),
        "parameters": [
            {
                "name": "url",
                "type": "string",
                "required": True,
                "description": "Reference URL to find similar content"
            },
            {
                "name": "num_results",
                "type": "integer",
                "required": False,
                "default": 10,
                "description": "Number of similar results (1-100)"
            },
            {
                "name": "exclude_source_domain",
                "type": "boolean",
                "required": False,
                "default": True,
                "description": "Exclude results from same domain"
            },
            {
                "name": "include_text",
                "type": "boolean",
                "required": False,
                "default": False,
                "description": "Include full page text"
            }
        ],
        "returns": "List of semantically similar URLs with relevance scores",
        "related": ["search"]
    },
    "get-contents": {
        "name": "get-contents",
        "description": "Extract full content from specific URLs",
        "long_description": """
Fetch and extract clean, parsed content from one or more URLs.
Returns structured text, metadata, and optional highlights.

Features:
- Clean text extraction
- Metadata parsing (title, author, date)
- HTML tag preservation (optional)
- Custom highlight extraction
- Livecrawl for fresh content

Best for:
- Content extraction
- Archiving web pages
- Data gathering
- Research documentation
        """.strip(),
        "parameters": [
            {
                "name": "urls",
                "type": "array",
                "required": True,
                "description": "List of URLs to extract content from"
            },
            {
                "name": "include_html_tags",
                "type": "boolean",
                "required": False,
                "default": False,
                "description": "Preserve HTML formatting tags"
            },
            {
                "name": "text_verbosity",
                "type": "string",
                "required": False,
                "default": "standard",
                "description": "Text detail: compact, standard, or full"
            },
            {
                "name": "max_characters",
                "type": "integer",
                "required": False,
                "description": "Limit text length (default: no limit)"
            },
            {
                "name": "max_age_hours",
                "type": "integer",
                "required": False,
                "description": "Max content age in hours (0=always livecrawl, -1=cache only)"
            }
        ],
        "returns": "Structured content with text, metadata, and optional highlights",
        "related": ["search", "code-search"]
    },
    "config": {
        "name": "config",
        "description": "Show current configuration and API key status",
        "long_description": "Display current Exa CLI configuration including API endpoint, timeout settings, and API key validation status (masked for security).",
        "parameters": [],
        "returns": "Current configuration settings",
        "related": []
    },
    "version": {
        "name": "version",
        "description": "Display CLI version and API information",
        "long_description": "Show Exa CLI wrapper version, Python version, and API endpoint information.",
        "parameters": [],
        "returns": "Version information",
        "related": ["config"]
    }
}

# ===== LEVEL 3: FUNCTION EXAMPLES =====

FUNCTION_EXAMPLES: Dict[str, List[Dict[str, str]]] = {
    "search": [
        {
            "title": "Basic semantic search",
            "command": 'uv run exa.py search "machine learning best practices"',
            "description": "Search for ML best practices using semantic understanding"
        },
        {
            "title": "Search with date filter",
            "command": 'uv run exa.py search "AI breakthroughs" --start-published-date 2024-01-01 --num-results 20',
            "description": "Find recent AI breakthroughs from 2024 onwards"
        },
        {
            "title": "Domain-specific search with full text",
            "command": 'uv run exa.py search "React performance" --include-domains github.com,reactjs.org --include-text',
            "description": "Search React docs and GitHub with full content extraction"
        }
    ],
    "deep-search": [
        {
            "title": "Comprehensive research",
            "command": 'uv run exa.py deep-search "quantum computing applications"',
            "description": "Deep research with automatic query expansion"
        },
        {
            "title": "Multi-angle exploration",
            "command": 'uv run exa.py deep-search "climate change" --additional-queries "global warming" "carbon emissions"',
            "description": "Explore multiple related queries for comprehensive coverage"
        }
    ],
    "research": [
        {
            "title": "Basic research question",
            "command": 'uv run exa.py research "What are the latest breakthroughs in AI agents?"',
            "description": "Agentic research with multi-step reasoning and citations"
        },
        {
            "title": "Complex multi-step research",
            "command": 'uv run exa.py research "Compare the architectures of GPT-4, Claude, and Gemini" --model exa-research-pro',
            "description": "High-quality research using the pro model for complex tasks"
        },
        {
            "title": "Research with structured output",
            "command": 'uv run exa.py research "What are the top 5 Python web frameworks in 2024?" --format json',
            "description": "Get structured JSON output for programmatic use"
        }
    ],
    "code-search": [
        {
            "title": "Find implementation examples",
            "command": 'uv run exa.py code-search "async await Python examples"',
            "description": "Find code examples for async/await in Python"
        },
        {
            "title": "GitHub-focused search",
            "command": 'uv run exa.py code-search "React hooks" --include-domains github.com --num-results 15',
            "description": "Search GitHub specifically for React hooks examples"
        }
    ],
    "company-research": [
        {
            "title": "Company profile and news",
            "command": 'uv run exa.py company-research "Anthropic"',
            "description": "Research Anthropic with recent news and business info"
        },
        {
            "title": "Time-filtered company research",
            "command": 'uv run exa.py company-research "OpenAI" --start-date 2024-01-01 --num-results 30',
            "description": "Get OpenAI news and updates from 2024"
        }
    ],
    "find-similar": [
        {
            "title": "Find related articles",
            "command": 'uv run exa.py find-similar "https://arxiv.org/abs/2103.03404" --num-results 10',
            "description": "Find papers similar to a specific arXiv paper"
        }
    ],
    "get-contents": [
        {
            "title": "Extract article content",
            "command": 'uv run exa.py get-contents "https://example.com/article"',
            "description": "Extract clean text from a web article"
        },
        {
            "title": "Multiple URLs with fresh content",
            "command": 'uv run exa.py get-contents "https://site1.com" "https://site2.com" --max-age-hours 0',
            "description": "Extract fresh content (livecrawl) from multiple URLs"
        },
        {
            "title": "Content with age limit",
            "command": 'uv run exa.py get-contents "https://news.site.com" --max-age-hours 24',
            "description": "Extract content no older than 24 hours"
        }
    ]
}

# ===== CORE FUNCTIONALITY =====

class ExaClient:
    """Exa API client"""

    def __init__(self, api_key: str, api_url: str = EXA_API_URL, timeout: int = DEFAULT_TIMEOUT):
        self.api_key = api_key
        self.api_url = api_url.rstrip('/')
        self.timeout = timeout
        self.client = httpx.Client(timeout=timeout)

    def _headers(self) -> Dict[str, str]:
        return {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }

    def search(
        self,
        query: str,
        num_results: int = 10,
        search_type: str = "auto",
        category: Optional[str] = None,
        include_domains: Optional[List[str]] = None,
        exclude_domains: Optional[List[str]] = None,
        start_published_date: Optional[str] = None,
        end_published_date: Optional[str] = None,
        include_text: bool = False,
        include_highlights: bool = True,
        include_summary: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """Execute neural search"""
        payload = {
            "query": query,
            "numResults": num_results,
            "type": search_type
        }

        if category:
            payload["category"] = category
        if include_domains:
            payload["includeDomains"] = include_domains
        if exclude_domains:
            payload["excludeDomains"] = exclude_domains
        if start_published_date:
            payload["startPublishedDate"] = start_published_date
        if end_published_date:
            payload["endPublishedDate"] = end_published_date

        # Content options
        if include_text:
            payload["text"] = True
        if include_highlights:
            payload["highlights"] = True
        if include_summary:
            payload["summary"] = True

        response = self.client.post(
            f"{self.api_url}/search",
            json=payload,
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json()

    def deep_search(
        self,
        query: str,
        additional_queries: Optional[List[str]] = None,
        num_results: int = 10,
        include_text: bool = False,
        include_summary: bool = True,
        **kwargs
    ) -> Dict[str, Any]:
        """Execute deep search with query expansion"""
        payload = {
            "query": query,
            "numResults": num_results,
            "type": "deep",
            "summary": include_summary
        }

        if additional_queries:
            payload["additionalQueries"] = additional_queries
        if include_text:
            payload["text"] = True

        response = self.client.post(
            f"{self.api_url}/search",
            json=payload,
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json()

    def get_contents(
        self,
        urls: List[str],
        include_html_tags: bool = False,
        text_verbosity: str = "standard",
        max_characters: Optional[int] = None,
        max_age_hours: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Extract content from URLs"""
        payload = {
            "urls": urls,
            "text": {
                "includeHtmlTags": include_html_tags,
                "verbosity": text_verbosity
            }
        }

        if max_characters:
            payload["text"]["maxCharacters"] = max_characters
        if max_age_hours is not None:
            payload["maxAgeHours"] = max_age_hours

        response = self.client.post(
            f"{self.api_url}/contents",
            json=payload,
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json()

    def research(
        self,
        instructions: str,
        model: str = "exa-research",
        output_schema: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Execute agentic research task"""
        payload = {
            "instructions": instructions,
            "model": model
        }

        if output_schema:
            payload["outputSchema"] = output_schema

        # Research API uses a different endpoint
        response = self.client.post(
            f"{self.api_url}/research/v1",
            json=payload,
            headers=self._headers(),
            timeout=180  # Research can take longer (up to 180s for pro)
        )
        response.raise_for_status()
        return response.json()

# ===== OUTPUT FORMATTING =====

def format_output(data: Any, format_type: str = "text", verbose: bool = False) -> None:
    """Format and display output"""
    if format_type == "json":
        console.print_json(json.dumps(data, indent=2))
        return

    # Text formatting for different data types
    if isinstance(data, dict):
        if "results" in data:
            format_search_results(data, verbose)
        elif "content" in data or "contents" in data:
            format_contents(data, verbose)
        elif "researchId" in data or "answer" in data or "report" in data:
            format_research_results(data, verbose)
        else:
            console.print_json(json.dumps(data, indent=2))
    else:
        console.print(data)

def format_search_results(data: Dict[str, Any], verbose: bool = False) -> None:
    """Format search results as rich output"""
    results = data.get("results", [])

    # Summary panel
    search_type = data.get("searchType", "unknown")
    cost = data.get("costDollars", {}).get("total", 0)

    summary = f"[cyan]Search Type:[/cyan] {search_type}\n"
    summary += f"[cyan]Results:[/cyan] {len(results)}\n"
    summary += f"[cyan]Cost:[/cyan] ${cost:.4f}"

    console.print(Panel(summary, title="Search Summary", border_style="cyan"))
    console.print()

    # Results table
    for idx, result in enumerate(results, 1):
        # Title and URL
        title = result.get("title", "No title")
        url = result.get("url", "")

        console.print(f"\n[bold cyan]{idx}. {title}[/bold cyan]")
        console.print(f"[dim]{url}[/dim]")

        # Metadata
        if published := result.get("publishedDate"):
            console.print(f"[yellow]Published:[/yellow] {published[:10]}")
        if author := result.get("author"):
            console.print(f"[yellow]Author:[/yellow] {author}")

        # Highlights
        if highlights := result.get("highlights"):
            console.print("\n[green]Highlights:[/green]")
            for highlight in highlights[:3]:  # Show top 3
                console.print(f"  • {highlight}")

        # Summary
        if summary := result.get("summary"):
            console.print(f"\n[blue]Summary:[/blue] {summary}")

        # Text (if verbose)
        if verbose and (text := result.get("text")):
            console.print("\n[magenta]Full Text:[/magenta]")
            console.print(Panel(text[:500] + "..." if len(text) > 500 else text))

def format_contents(data: Dict[str, Any], verbose: bool = False) -> None:
    """Format extracted contents"""
    contents = data.get("contents", [data.get("content", {})])

    for idx, content in enumerate(contents, 1):
        url = content.get("url", "Unknown URL")
        title = content.get("title", "No title")

        console.print(f"\n[bold cyan]{idx}. {title}[/bold cyan]")
        console.print(f"[dim]{url}[/dim]\n")

        if text := content.get("text"):
            # Show preview or full text
            preview_length = 1000 if not verbose else len(text)
            preview = text[:preview_length]
            if len(text) > preview_length:
                preview += "\n..."

            console.print(Panel(preview, title="Content", border_style="green"))

def format_research_results(data: Dict[str, Any], verbose: bool = False) -> None:
    """Format research results"""
    # Summary panel
    research_id = data.get("researchId", "unknown")
    model = data.get("model", "exa-research")
    status = data.get("status", "completed")
    cost = data.get("costDollars", {})

    summary = f"[cyan]Research ID:[/cyan] {research_id}\n"
    summary += f"[cyan]Model:[/cyan] {model}\n"
    summary += f"[cyan]Status:[/cyan] {status}"

    if cost:
        total_cost = cost.get("total", 0)
        summary += f"\n[cyan]Cost:[/cyan] ${total_cost:.4f}"

    console.print(Panel(summary, title="Research Summary", border_style="cyan"))
    console.print()

    # Answer/Report
    if answer := data.get("answer"):
        console.print(Panel(answer, title="Answer", border_style="green"))
    elif report := data.get("report"):
        console.print(Panel(report, title="Research Report", border_style="green"))

    # Citations
    if citations := data.get("citations", []):
        console.print("\n[yellow]Citations:[/yellow]")
        for idx, citation in enumerate(citations, 1):
            url = citation.get("url", "")
            title = citation.get("title", "")
            console.print(f"  [{idx}] {title}")
            console.print(f"      [dim]{url}[/dim]")

    # Structured output (if present)
    if structured := data.get("structuredOutput"):
        console.print("\n[magenta]Structured Output:[/magenta]")
        console.print_json(json.dumps(structured, indent=2))

def validate_credentials() -> bool:
    """Validate API credentials"""
    if not EXA_API_KEY:
        console.print(Panel(
            "[red]EXA_API_KEY environment variable not set[/red]\n\n"
            "Get your API key at: https://exa.ai/\n"
            "Then: export EXA_API_KEY='your-key-here'",
            title="Error: Missing API Key",
            border_style="red"
        ))
        return False
    return True

# ===== CLI COMMANDS =====

def cmd_list(args: argparse.Namespace) -> None:
    """List all available functions"""
    table = Table(title="Exa CLI Functions", show_header=True, header_style="bold cyan")
    table.add_column("Function", style="cyan", width=20)
    table.add_column("Description", width=60)

    for func_name, func_info in FUNCTION_INFO.items():
        table.add_row(func_name, func_info["description"])

    console.print(table)
    console.print("\n[dim]For detailed docs: uv run exa.py info FUNCTION[/dim]")
    console.print("[dim]For examples: uv run exa.py example FUNCTION[/dim]")

def cmd_info(args: argparse.Namespace) -> None:
    """Show detailed function information"""
    func_name = args.function

    if func_name not in FUNCTION_INFO:
        console.print(f"[red]Unknown function: {func_name}[/red]")
        console.print("Run 'uv run exa.py list' to see available functions")
        sys.exit(1)

    info = FUNCTION_INFO[func_name]

    # Build info panel
    content = f"[bold]{info['description']}[/bold]\n\n"
    content += f"{info['long_description']}\n\n"

    # Parameters
    if info['parameters']:
        content += "[cyan]Parameters:[/cyan]\n"
        for param in info['parameters']:
            required = "required" if param.get('required') else "optional"
            default = f" (default: {param.get('default')})" if 'default' in param else ""
            content += f"  • [yellow]{param['name']}[/yellow] ({param['type']}, {required}){default}\n"
            content += f"    {param['description']}\n"

    content += f"\n[cyan]Returns:[/cyan] {info['returns']}"

    if info['related']:
        content += f"\n\n[cyan]Related:[/cyan] {', '.join(info['related'])}"

    console.print(Panel(content, title=f"Function: {func_name}", border_style="cyan"))
    console.print("\n[dim]For examples: uv run exa.py example " + func_name + "[/dim]")

def cmd_example(args: argparse.Namespace) -> None:
    """Show function examples"""
    func_name = args.function

    if func_name not in FUNCTION_EXAMPLES:
        console.print(f"[red]No examples for: {func_name}[/red]")
        sys.exit(1)

    examples = FUNCTION_EXAMPLES[func_name]

    console.print(Panel(f"Examples for [cyan]{func_name}[/cyan]", border_style="cyan"))

    for idx, example in enumerate(examples, 1):
        console.print(f"\n[bold yellow]{idx}. {example['title']}[/bold yellow]")
        console.print(f"[dim]{example['description']}[/dim]\n")
        console.print(Syntax(example['command'], "bash", theme="monokai"))

def cmd_config(args: argparse.Namespace) -> None:
    """Show current configuration"""
    config_data = {
        "API URL": EXA_API_URL,
        "Timeout": f"{DEFAULT_TIMEOUT}s",
        "API Key": f"{'✓ Set' if EXA_API_KEY else '✗ Not set'} ({EXA_API_KEY[:8]}...)" if EXA_API_KEY else "✗ Not set"
    }

    table = Table(title="Exa CLI Configuration", show_header=True)
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="yellow")

    for key, value in config_data.items():
        table.add_row(key, value)

    console.print(table)

def cmd_version(args: argparse.Namespace) -> None:
    """Show version information"""
    version_info = {
        "Exa CLI": "1.1.0",
        "Python": sys.version.split()[0],
        "API Endpoint": EXA_API_URL,
        "Features": "Research API, maxAgeHours"
    }

    console.print(Panel(
        "\n".join(f"[cyan]{k}:[/cyan] {v}" for k, v in version_info.items()),
        title="Version Information",
        border_style="cyan"
    ))

def cmd_search(args: argparse.Namespace) -> None:
    """Execute search command"""
    if not validate_credentials():
        sys.exit(1)

    try:
        client = ExaClient(EXA_API_KEY)

        # Parse domains if provided
        include_domains = args.include_domains.split(',') if args.include_domains else None
        exclude_domains = args.exclude_domains.split(',') if args.exclude_domains else None

        result = client.search(
            query=args.query,
            num_results=args.num_results,
            search_type=args.type,
            category=args.category,
            include_domains=include_domains,
            exclude_domains=exclude_domains,
            start_published_date=args.start_published_date,
            end_published_date=args.end_published_date,
            include_text=args.include_text,
            include_highlights=args.include_highlights,
            include_summary=args.include_summary
        )

        format_output(result, args.format, args.verbose)

    except httpx.HTTPStatusError as e:
        console.print(f"[red]HTTP Error {e.response.status_code}:[/red] {e.response.text}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        if args.verbose:
            traceback.print_exc()
        console.print(f"[red]Error:[/red] {e}", file=sys.stderr)
        sys.exit(1)

def cmd_deep_search(args: argparse.Namespace) -> None:
    """Execute deep search command"""
    if not validate_credentials():
        sys.exit(1)

    try:
        client = ExaClient(EXA_API_KEY)

        additional_queries = args.additional_queries.split(',') if args.additional_queries else None

        result = client.deep_search(
            query=args.query,
            additional_queries=additional_queries,
            num_results=args.num_results,
            include_text=args.include_text,
            include_summary=args.include_summary
        )

        format_output(result, args.format, args.verbose)

    except Exception as e:
        if args.verbose:
            traceback.print_exc()
        console.print(f"[red]Error:[/red] {e}", file=sys.stderr)
        sys.exit(1)

def cmd_code_search(args: argparse.Namespace) -> None:
    """Execute code search command"""
    if not validate_credentials():
        sys.exit(1)

    try:
        client = ExaClient(EXA_API_KEY)

        include_domains = args.include_domains.split(',') if args.include_domains else None

        result = client.search(
            query=args.query,
            num_results=args.num_results,
            search_type="neural",
            include_domains=include_domains or ["github.com", "stackoverflow.com", "docs.python.org"],
            include_text=args.include_text,
            include_highlights=args.include_highlights
        )

        format_output(result, args.format, args.verbose)

    except Exception as e:
        if args.verbose:
            traceback.print_exc()
        console.print(f"[red]Error:[/red] {e}", file=sys.stderr)
        sys.exit(1)

def cmd_company_research(args: argparse.Namespace) -> None:
    """Execute company research command"""
    if not validate_credentials():
        sys.exit(1)

    try:
        client = ExaClient(EXA_API_KEY)

        result = client.search(
            query=args.company_name,
            num_results=args.num_results,
            category="company",
            start_published_date=args.start_date,
            include_highlights=args.include_news,
            include_summary=args.include_summary
        )

        format_output(result, args.format, args.verbose)

    except Exception as e:
        if args.verbose:
            traceback.print_exc()
        console.print(f"[red]Error:[/red] {e}", file=sys.stderr)
        sys.exit(1)

def cmd_find_similar(args: argparse.Namespace) -> None:
    """Execute find similar command"""
    if not validate_credentials():
        sys.exit(1)

    try:
        client = ExaClient(EXA_API_KEY)

        # For find-similar, we'd use a different endpoint or special query
        # For now, using search with the URL as context
        result = client.search(
            query=f"similar to {args.url}",
            num_results=args.num_results,
            include_text=args.include_text
        )

        format_output(result, args.format, args.verbose)

    except Exception as e:
        if args.verbose:
            traceback.print_exc()
        console.print(f"[red]Error:[/red] {e}", file=sys.stderr)
        sys.exit(1)

def cmd_research(args: argparse.Namespace) -> None:
    """Execute agentic research command"""
    if not validate_credentials():
        sys.exit(1)

    try:
        client = ExaClient(EXA_API_KEY)

        console.print(f"[cyan]Starting research task...[/cyan]")
        console.print(f"[dim]Model: {args.model}[/dim]")
        console.print(f"[dim]This may take 45-180 seconds...[/dim]\n")

        result = client.research(
            instructions=args.instructions,
            model=args.model
        )

        format_output(result, args.format, args.verbose)

    except httpx.HTTPStatusError as e:
        console.print(f"[red]HTTP Error {e.response.status_code}:[/red] {e.response.text}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        if args.verbose:
            traceback.print_exc()
        console.print(f"[red]Error:[/red] {e}", file=sys.stderr)
        sys.exit(1)

def cmd_get_contents(args: argparse.Namespace) -> None:
    """Execute get contents command"""
    if not validate_credentials():
        sys.exit(1)

    try:
        client = ExaClient(EXA_API_KEY)

        result = client.get_contents(
            urls=args.urls,
            include_html_tags=args.include_html_tags,
            text_verbosity=args.text_verbosity,
            max_characters=args.max_characters,
            max_age_hours=args.max_age_hours
        )

        format_output(result, args.format, args.verbose)

    except Exception as e:
        if args.verbose:
            traceback.print_exc()
        console.print(f"[red]Error:[/red] {e}", file=sys.stderr)
        sys.exit(1)

# ===== MAIN =====

def main():
    parser = argparse.ArgumentParser(
        description="Exa AI Search CLI - Neural search powered by embeddings",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=QUICK_HELP
    )

    parser.add_argument('--format', choices=['json', 'text'], default='text', help='Output format')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Meta commands
    subparsers.add_parser('list', help='List all functions')

    info_parser = subparsers.add_parser('info', help='Show function details')
    info_parser.add_argument('function', help='Function name')

    example_parser = subparsers.add_parser('example', help='Show function examples')
    example_parser.add_argument('function', help='Function name')

    subparsers.add_parser('config', help='Show configuration')
    subparsers.add_parser('version', help='Show version')

    # Search command
    search_parser = subparsers.add_parser('search', help='Neural search')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--num-results', type=int, default=10, help='Number of results')
    search_parser.add_argument('--type', choices=['auto', 'neural', 'fast'], default='auto', help='Search type')
    search_parser.add_argument('--category', help='Filter by category')
    search_parser.add_argument('--include-domains', help='Comma-separated domains to include')
    search_parser.add_argument('--exclude-domains', help='Comma-separated domains to exclude')
    search_parser.add_argument('--start-published-date', help='Start date (ISO 8601)')
    search_parser.add_argument('--end-published-date', help='End date (ISO 8601)')
    search_parser.add_argument('--include-text', action='store_true', help='Include full text')
    search_parser.add_argument('--include-highlights', action='store_true', default=True, help='Include highlights')
    search_parser.add_argument('--include-summary', action='store_true', help='Include AI summary')

    # Deep search command
    deep_parser = subparsers.add_parser('deep-search', help='Deep search with expansion')
    deep_parser.add_argument('query', help='Primary query')
    deep_parser.add_argument('--additional-queries', help='Comma-separated additional queries')
    deep_parser.add_argument('--num-results', type=int, default=10, help='Results per query')
    deep_parser.add_argument('--include-text', action='store_true', help='Include full text')
    deep_parser.add_argument('--include-summary', action='store_true', default=True, help='Include summaries')

    # Research command (NEW - Agentic Research API)
    research_parser = subparsers.add_parser('research', help='Agentic research with reasoning')
    research_parser.add_argument('instructions', help='Research instructions (natural language)')
    research_parser.add_argument('--model', choices=['exa-research', 'exa-research-pro'], default='exa-research',
                                 help='Model: exa-research (faster) or exa-research-pro (higher quality)')

    # Code search command
    code_parser = subparsers.add_parser('code-search', help='Search for code')
    code_parser.add_argument('query', help='Code query')
    code_parser.add_argument('--num-results', type=int, default=10, help='Number of results')
    code_parser.add_argument('--include-domains', help='Comma-separated domains')
    code_parser.add_argument('--include-text', action='store_true', default=True, help='Include code text')
    code_parser.add_argument('--include-highlights', action='store_true', default=True, help='Include snippets')

    # Company research command
    company_parser = subparsers.add_parser('company-research', help='Research companies')
    company_parser.add_argument('company_name', help='Company name')
    company_parser.add_argument('--num-results', type=int, default=20, help='Number of results')
    company_parser.add_argument('--include-news', action='store_true', default=True, help='Include news')
    company_parser.add_argument('--start-date', help='Start date for news')
    company_parser.add_argument('--include-summary', action='store_true', default=True, help='Include summaries')

    # Find similar command
    similar_parser = subparsers.add_parser('find-similar', help='Find similar content')
    similar_parser.add_argument('url', help='Reference URL')
    similar_parser.add_argument('--num-results', type=int, default=10, help='Number of results')
    similar_parser.add_argument('--include-text', action='store_true', help='Include full text')

    # Get contents command
    contents_parser = subparsers.add_parser('get-contents', help='Extract URL content')
    contents_parser.add_argument('urls', nargs='+', help='URLs to extract')
    contents_parser.add_argument('--include-html-tags', action='store_true', help='Preserve HTML tags')
    contents_parser.add_argument('--text-verbosity', choices=['compact', 'standard', 'full'], default='standard')
    contents_parser.add_argument('--max-characters', type=int, help='Limit text length')
    contents_parser.add_argument('--max-age-hours', type=int, help='Max content age (0=livecrawl, -1=cache only)')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    # Route to command handlers
    commands = {
        'list': cmd_list,
        'info': cmd_info,
        'example': cmd_example,
        'config': cmd_config,
        'version': cmd_version,
        'search': cmd_search,
        'deep-search': cmd_deep_search,
        'research': cmd_research,
        'code-search': cmd_code_search,
        'company-research': cmd_company_research,
        'find-similar': cmd_find_similar,
        'get-contents': cmd_get_contents
    }

    handler = commands.get(args.command)
    if handler:
        handler(args)
    else:
        console.print(f"[red]Unknown command: {args.command}[/red]")
        sys.exit(1)

if __name__ == "__main__":
    main()
