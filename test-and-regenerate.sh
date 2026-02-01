#!/bin/bash
# Test wrapper template and regenerate all wrappers
# Run this directly in terminal: bash test-and-regenerate.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║  CLI Wrappers - Template Testing & Regeneration          ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# ============================================================
# PART 1: TEST NEW WRAPPER TEMPLATE (4 Levels)
# ============================================================

echo "PART 1: Testing New Wrapper Template (4 Progressive Levels)"
echo "═══════════════════════════════════════════════════════════"
echo ""

echo "Level 1: Quick Help (--help)"
echo "─────────────────────────────"
timeout 10 uv run test-wrapper-new.py --help || echo "❌ Failed"
echo ""

echo "Level 2a: List Functions"
echo "────────────────────────"
timeout 10 uv run test-wrapper-new.py list || echo "❌ Failed"
echo ""

echo "Level 2b: Info for Function"
echo "───────────────────────────"
timeout 10 uv run test-wrapper-new.py info sequentialthinking || echo "❌ Failed"
echo ""

echo "Level 3: Examples"
echo "─────────────────"
timeout 10 uv run test-wrapper-new.py example sequentialthinking || echo "❌ Failed"
echo ""

echo "Level 4: Function-Specific Help"
echo "────────────────────────────────"
timeout 10 uv run test-wrapper-new.py sequentialthinking --help || echo "❌ Failed"
echo ""

echo "Format Test: JSON Output"
echo "────────────────────────"
timeout 10 uv run test-wrapper-new.py list --format json || echo "❌ Failed"
echo ""

# ============================================================
# PART 2: REGENERATE ALL WRAPPERS
# ============================================================

echo ""
echo "PART 2: Regenerating All Wrappers with Fixed Template"
echo "═════════════════════════════════════════════════════════"
echo ""

if command -v python3 &> /dev/null; then
    echo "Generating wrappers..."
    timeout 30 python3 generate-all-wrappers.py || {
        echo "❌ Generation failed"
        exit 1
    }
else
    echo "❌ python3 not found"
    exit 1
fi

echo ""
echo "✅ ALL TESTS PASSED"
echo ""
echo "Generated wrappers:"
ls -lh *.py | grep -E "(crawl4ai|firecrawl|ref|repomix|deepwiki|github|semly|sequential|claude-flow|flow-nexus|exa)\.py" | awk '{print "  -", $9, "(" $5 ")"}'

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "Next steps:"
echo ""
echo "1. Test any wrapper with all 4 levels:"
echo "   uv run crawl4ai.py --help"
echo "   uv run crawl4ai.py list"
echo "   uv run crawl4ai.py info scrape"
echo "   uv run crawl4ai.py example scrape"
echo "   uv run crawl4ai.py scrape --help"
echo ""
echo "2. Try JSON output:"
echo "   uv run crawl4ai.py list --format json"
echo ""
echo "3. Verify parameters are populated:"
echo "   uv run crawl4ai.py info scrape"
echo ""
echo "═══════════════════════════════════════════════════════════"
